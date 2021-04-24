import queue

from constants import *


class ReorderElementConnectivity:
    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)

        self.mesh_data = None
        self.count_reorder_pattern_used = None
        pass

    def reorder(self, mesh_data):
        """
        要素内の節点順序の並び替えと、
        要素へのフラグの設定を行う。
        """
        self.logger.info(f'start reorder()')

        # num_elements
        self.mesh_data = mesh_data
        num_elements = mesh_data.get_num_elements()

        self.count_reorder_pattern_used = [0] * len(ORDERED_NODES)

        is_ordered = [False] * num_elements
        queue_elements = queue.LifoQueue()

        start_element_index = 0
        queue_elements.put(start_element_index)
        element_flag = [ELEMENT_FLAG_UNDETERMINED] * num_elements
        element_flag[start_element_index] = ELEMENT_FLAG_INITIAL

        neighbor_element = mesh_data.get_neighbor_element()

        count_reorder_success = 0
        count_reorder_fail = 0
        count_loop = 0
        count_ordered = 0
        while not queue_elements.empty():
            count_loop += 1
            if count_loop > 0 and count_loop % LOGGER_INTERVAL == 0:
                self.logger.info(f'reorder : count_loop={count_loop}, count_ordered={count_ordered}, '
                                 f'queue_size={queue_elements.qsize()}')

            element_index = queue_elements.get()
            if is_ordered[element_index]:
                continue
            else:
                is_ordered[element_index] = True
                count_ordered += 1
            
            for i_face in range(NUM_FACES_OF_ELEMENT):
                neighbor_element_index = neighbor_element[element_index][i_face]
                if neighbor_element_index == INVALID:
                    continue
                if not is_ordered[neighbor_element_index]:
                    continue
                
                if element_flag[neighbor_element_index] == element_flag[element_index]:
                    self.logger.warning(f'error: flag mismatched, element={element_index}, face={i_face}, '
                                        f'neighbor_element={neighbor_element_index}')
                    self.logger.warning(f'error: flag mismatched, element_flag={element_flag}')
                else:
                    reorder_success = self.reorder_connectivity(element_index, neighbor_element_index)
                    if reorder_success:
                        count_reorder_success += 1
                    else:
                        count_reorder_fail += 1
                    break

            for i_face in range(NUM_FACES_OF_ELEMENT):
                neighbor_element_index = neighbor_element[element_index][i_face]
                if neighbor_element_index != INVALID and not is_ordered[neighbor_element_index]:
                    if element_flag[element_index] == ELEMENT_FLAG_A:
                        element_flag[neighbor_element_index] = ELEMENT_FLAG_B
                    elif element_flag[element_index] == ELEMENT_FLAG_B:
                        element_flag[neighbor_element_index] = ELEMENT_FLAG_A
                    queue_elements.put(neighbor_element_index)

        mesh_data.set_element_flag(element_flag)

        self.check_after_reorder()

        self.logger.info(f'count_reorder_pattern_used={self.count_reorder_pattern_used}')
        self.logger.info(f'reorder count : success={count_reorder_success}, fail={count_reorder_fail}')

        self.logger.info(f'finish reorder()')
        pass

    def reorder_connectivity(self, element_index_1, element_index_2):
        """
        1つの要素の節点順序の並び替えを行う。
        element_index_1が並び替え対象の要素であり、
        element_index_2は、並び替えの基準とする要素である。
        """
        mesh_data = self.mesh_data
        elements_df = mesh_data.get_elements_df()
        neighbor_element = mesh_data.get_neighbor_element()
        neighbor_face = mesh_data.get_neighbor_face()

        nodes = [elements_df[COLUMN_NODE_0].values, elements_df[COLUMN_NODE_1].values, elements_df[COLUMN_NODE_2].values,
                 elements_df[COLUMN_NODE_3].values, elements_df[COLUMN_NODE_4].values, elements_df[COLUMN_NODE_5].values,
                 elements_df[COLUMN_NODE_6].values, elements_df[COLUMN_NODE_7]]

        nodes_1_before = [
            nodes[0][element_index_1],
            nodes[1][element_index_1],
            nodes[2][element_index_1],
            nodes[3][element_index_1],
            nodes[4][element_index_1],
            nodes[5][element_index_1],
            nodes[6][element_index_1],
            nodes[7][element_index_1]
            ]

        neighbor_element_1 = neighbor_element[element_index_1]
        neighbor_element_2 = neighbor_element[element_index_2]
        neighbor_face_1 = neighbor_face[element_index_1]
        neighbor_face_2 = neighbor_face[element_index_2]

        face_1 = INVALID
        face_2 = INVALID
        flag_hit_1 = False
        flag_hit_2 = False
        for face_1 in range(NUM_FACES_OF_ELEMENT):
            if element_index_2 == neighbor_element_1[face_1]:
                flag_hit_1 = True
                break

        for face_2 in range(NUM_FACES_OF_ELEMENT):
            if element_index_1 == neighbor_element_2[face_2]:
                flag_hit_2 = True
                break
        
        if not flag_hit_1 or not flag_hit_2:
            self.logger.info(f'not neighbor element element_1={element_index_1}, element_2={element_index_2}')
            return False

        if neighbor_face_1[face_1] != face_2:
            self.logger.info(f'#a face id mismatch : element_1={element_index_1}, face_1={face_1}, '
                             f'element_2={element_index_2}, face_2={face_2}')
        if neighbor_face_2[face_2] != face_1:
            self.logger.info(f'#b face id mismatch : element_1={element_index_1}, face_1={face_1}, '
                             f'element_2={element_index_2}, face_2={face_2}')

        face_1_correct = FACE_RELATION_ARRAY[face_2]

        temp_local_nodes_1 = NODES_OF_FACE[face_1_correct]
        local_node_1_0_temp = temp_local_nodes_1[0]
        local_node_1_1_temp = temp_local_nodes_1[1]
        local_node_1_2_temp = temp_local_nodes_1[2]
        local_node_1_3_temp = temp_local_nodes_1[3]

        temp_local_nodes_2 = NODES_OF_FACE_REVERSE[face_2]
        local_node_2_0 = temp_local_nodes_2[0]
        local_node_2_1 = temp_local_nodes_2[1]
        local_node_2_2 = temp_local_nodes_2[2]
        local_node_2_3 = temp_local_nodes_2[3]
        p_2_0 = nodes[local_node_2_0][element_index_2]
        p_2_1 = nodes[local_node_2_1][element_index_2]
        p_2_2 = nodes[local_node_2_2][element_index_2]
        p_2_3 = nodes[local_node_2_3][element_index_2]
        list_2 = [p_2_0, p_2_1, p_2_2, p_2_3]

        reorder_pattern_id = INVALID
        flg_reordered = False
        for reorder_pattern_id in range(len(ORDERED_NODES)):
            ordered_nodes = ORDERED_NODES[reorder_pattern_id]
            # after reorder
            local_node_1_0 = ordered_nodes[local_node_1_0_temp]
            local_node_1_1 = ordered_nodes[local_node_1_1_temp]
            local_node_1_2 = ordered_nodes[local_node_1_2_temp]
            local_node_1_3 = ordered_nodes[local_node_1_3_temp]
            # local to global
            p_1_0 = nodes_1_before[local_node_1_0]
            p_1_1 = nodes_1_before[local_node_1_1]
            p_1_2 = nodes_1_before[local_node_1_2]
            p_1_3 = nodes_1_before[local_node_1_3]
            list_1 = [p_1_0, p_1_1, p_1_2, p_1_3]

            # self.logger.info(f'list1={list_1}, list2={list_2}')
            if list_1 == list_2:
                flg_reordered = True
                break

        if not flg_reordered:
            self.logger.info(f'reorder failed, '
                             f'element_1={element_index_1}, face_1={face_1}, '
                             f'element_2={element_index_2}, face_2={face_2}')
            return False

        self.count_reorder_pattern_used[reorder_pattern_id] += 1

        # self.logger.info(f'reorder_pattern_id={reorder_pattern_id}, '
        #                  f'element_1={element_index_1}, element_2={element_index_2}')

        neighbor_element_before = [neighbor_element_1[i] for i in range(NUM_FACES_OF_ELEMENT)]
        neighbor_face_before = [neighbor_face_1[i] for i in range(NUM_FACES_OF_ELEMENT)]
        for i_face_new in range(NUM_FACES_OF_ELEMENT):
            face_old = ORDERED_FACE_NUMBER[reorder_pattern_id][i_face_new]
            
            neighbor_element_index = neighbor_element_before[face_old]
            neighbor_face_index = neighbor_face_before[face_old]
            neighbor_element_1[i_face_new] = neighbor_element_index
            neighbor_face_1[i_face_new] = neighbor_face_index

            if neighbor_element_index != INVALID and neighbor_face_index != INVALID:
                if neighbor_face[neighbor_element_index][neighbor_face_index] != face_old:
                    self.logger.warning(f'error : face mismatch : '
                                        f'reorder_pattern_id={reorder_pattern_id}, '
                                        f'element_1={element_index_1}, element_2={element_index_2}')
                neighbor_face[neighbor_element_index][neighbor_face_index] = i_face_new

        for local_node_id in range(NUM_NODES_OF_ELEMENT):
            local_node_id_new = ORDERED_NODES[reorder_pattern_id][local_node_id]
            nodes[local_node_id][element_index_1] = nodes_1_before[local_node_id_new]

        return True

    def check_after_reorder(self):
        self.logger.info(f'start check_after_reorder()')

        mesh_data = self.mesh_data
        num_elements = mesh_data.get_num_elements()
        elements_df = mesh_data.get_elements_df()
        neighbor_element = mesh_data.get_neighbor_element()
        neighbor_face = mesh_data.get_neighbor_face()
        element_flag = mesh_data.get_element_flag()

        flag_error_found = False
        for i_element in range(num_elements):
            element_flag_current = element_flag[i_element]
            if element_flag_current != ELEMENT_FLAG_A and element_flag_current != ELEMENT_FLAG_B:
                flag_error_found = True
                self.logger.warninig(f'error : unknown element flag : '
                                     f'element={i_element}, '
                                     f'element_flag={element_flag_current}')

            for i_face in range(NUM_FACES_OF_ELEMENT):
                neighbor_element_index = neighbor_element[i_element][i_face]
                neighbor_face_index = neighbor_face[i_element][i_face]

                if neighbor_element_index == INVALID and neighbor_face_index == INVALID:
                    pass
                elif neighbor_element_index == INVALID or neighbor_face_index == INVALID:
                    flag_error_found = True
                    self.logger.warninig(f'error : INVALID found : '
                                         f'element={i_element}, face={i_face}, '
                                         f'neighbor_element={neighbor_element_index}, '
                                         f'neighbor_face={neighbor_face_index}')
                else:
                    element_flag_neighbor = element_flag[neighbor_element_index]
                    if element_flag_neighbor != ELEMENT_FLAG_A and element_flag_neighbor != ELEMENT_FLAG_B:
                        flag_error_found = True
                        self.logger.warninig(f'error : unknown element flag : '
                                             f'neighbor_element={neighbor_element_index}, '
                                             f'neighbor_element_flag={element_flag_neighbor}')

                    if element_flag_current == element_flag_neighbor:
                        flag_error_found = True
                        self.logger.warninig(f'error : same element flag contact: '
                                             f'element={i_element}, face={i_face}, '
                                             f'element_flag={element_flag_current}, '
                                             f'neighbor_element={neighbor_element_index}, '
                                             f'neighbor_face={neighbor_face_index}, '
                                             f'neighbor_element_flag={element_flag_neighbor}')

                    if neighbor_face_index != FACE_RELATION_ARRAY[i_face]:
                        flag_error_found = True
                        self.logger.warninig(f'error : face mismatch: element={i_element}, face={i_face}, '
                                             f'neighbor_element_index={neighbor_element_index}, '
                                             f'neighbor_face_index={neighbor_face_index}')

        if not flag_error_found:
            self.logger.info(f'no error found')

        self.logger.info(f'finish check_after_reorder()')
        pass

