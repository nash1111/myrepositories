from constants import *


class NeighborElementChecker:
    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)
        pass

    def check(self, mesh_data):
        """
        要素同士の隣接関係を計算する。
        """
        self.logger.info(f'start check()')

        nodes_dfs = mesh_data.get_nodes_df()
        elements_df = mesh_data.get_elements_df()
        # self.logger.info(elements_df)
        num_nodes = mesh_data.get_num_nodes()
        node_to_element_list = [[] for i in range(num_nodes)]

        nodes = [elements_df[COLUMN_NODE_0].values, elements_df[COLUMN_NODE_1].values,
                 elements_df[COLUMN_NODE_2].values, elements_df[COLUMN_NODE_3].values,
                 elements_df[COLUMN_NODE_4].values, elements_df[COLUMN_NODE_5].values,
                 elements_df[COLUMN_NODE_6].values, elements_df[COLUMN_NODE_7].values
                 ]

        # for elements_df in elements_df:
        num_elements = mesh_data.get_num_elements()
        for i_element in range(num_elements):
            if i_element > 0 and i_element % LOGGER_INTERVAL == 0:
                self.logger.info(f'make node_to_element_list : {i_element} / {num_elements}')
            node0 = nodes[0][i_element]
            node1 = nodes[1][i_element]
            node2 = nodes[2][i_element]
            node3 = nodes[3][i_element]
            node4 = nodes[4][i_element]
            node5 = nodes[5][i_element]
            node6 = nodes[6][i_element]
            node7 = nodes[7][i_element]
            node_to_element_list[node0].append(i_element)
            node_to_element_list[node1].append(i_element)
            node_to_element_list[node2].append(i_element)
            node_to_element_list[node3].append(i_element)
            node_to_element_list[node4].append(i_element)
            node_to_element_list[node5].append(i_element)
            node_to_element_list[node6].append(i_element)
            node_to_element_list[node7].append(i_element)

        neighbor_element = [[INVALID for j in range(NUM_FACES_OF_ELEMENT)] for i in range(num_elements)]
        neighbor_face = [[INVALID for j in range(NUM_FACES_OF_ELEMENT)] for i in range(num_elements)]

        for i_element in range(num_elements):
            if i_element > 0 and i_element % LOGGER_INTERVAL == 0:
                self.logger.info(f'make neighbor : {i_element} / {num_elements}')

            element_a = i_element
            for i_face in range(NUM_FACES_OF_ELEMENT):
                face_a = i_face
                pa0 = nodes[NODES_OF_FACE[face_a][0]][element_a]
                pa1 = nodes[NODES_OF_FACE[face_a][1]][element_a]
                pa2 = nodes[NODES_OF_FACE[face_a][2]][element_a]
                pa3 = nodes[NODES_OF_FACE[face_a][3]][element_a]
                set_pa = {pa0, pa1, pa2, pa3}
                pa0_elements = node_to_element_list[pa0]
                pa1_elements = node_to_element_list[pa1]
                pa2_elements = node_to_element_list[pa2]
                pa3_elements = node_to_element_list[pa3]
                common_element_list = \
                    list(set(pa0_elements) & set(pa1_elements) & set(pa2_elements) & set(pa3_elements))
                nun_common_elements = len(common_element_list)
                element_b = INVALID
                face_b = INVALID
                if nun_common_elements == 1:
                    # self.logger.info('no relation')
                    pass
                elif nun_common_elements == 2:
                    common_element_list.remove(element_a)
                    element_b = common_element_list[0]
                    face_b = INVALID
                    for tmp_face in range(NUM_FACES_OF_ELEMENT):
                        pb0 = nodes[NODES_OF_FACE_REVERSE[tmp_face][0]][element_b]
                        pb1 = nodes[NODES_OF_FACE_REVERSE[tmp_face][1]][element_b]
                        pb2 = nodes[NODES_OF_FACE_REVERSE[tmp_face][2]][element_b]
                        pb3 = nodes[NODES_OF_FACE_REVERSE[tmp_face][3]][element_b]
                        set_pb = {pb0, pb1, pb2, pb3}
                        if set_pa == set_pb:
                            face_b = tmp_face
                            break
                    if face_b == INVALID:
                        self.logger.warning(f'error: no face matched : '
                                            f'element_a={element_a}, face_a={face_a}, '
                                            f'element_b={element_b}, face_b={face_b}')
                elif nun_common_elements >= 3:
                    self.logger.info(f'element={element_a}, face={face_a}, '
                                     f'pa0={pa0}, pa1={pa1}, pa2={pa2}, p3={pa3}, '
                                     f'common_element_list={common_element_list}')
                else:
                    self.logger.info(f'element={element_a}, face={face_a}, '
                                     f'pa0={pa0}, pa1={pa1}, pa2={pa2}, p3={pa3}, '
                                     f'common_element_list: empty')

                if element_b == INVALID or face_b == INVALID:
                    continue

                e_a = neighbor_element[element_a][face_a]
                f_a = neighbor_face[element_a][face_a]
                e_b = neighbor_element[element_b][face_b]
                f_b = neighbor_face[element_b][face_b]
                if e_a == element_b and f_a == face_b and e_b == element_a and f_b == face_a:
                    # self.logger.info('already checked')
                    pass
                elif e_a != INVALID or f_a != INVALID or e_b != INVALID or f_b != INVALID:
                    self.logger.info(f'error: neighbor relation: neighbor_element[{element_a}][{face_a}]={e_a}')
                    self.logger.info(f'error: neighbor relation: neighbor_face[{element_a}][{face_a}]={f_a}')
                    self.logger.info(f'error: neighbor relation: neighbor_element[{element_b}][{face_b}]={e_b}')
                    self.logger.info(f'error: neighbor relation: neighbor_face[{element_b}][{face_b}]={f_b}')
                else:
                    neighbor_element[element_a][face_a] = element_b
                    neighbor_face[element_a][face_a] = face_b
                    neighbor_element[element_b][face_b] = element_a
                    neighbor_face[element_b][face_b] = face_a

        # self.logger.info(f'neighbor_element={neighbor_element}')
        # self.logger.info(f'neighbor_face={neighbor_face}')
        # self.logger.info(f'node_to_element_list={node_to_element_list}')
        mesh_data.set_neighbor(neighbor_element, neighbor_face, num_elements, node_to_element_list)

        self.logger.info(f'finish check()')
        pass

