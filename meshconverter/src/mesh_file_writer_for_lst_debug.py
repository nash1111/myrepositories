import math
import os

from constants import *


class MeshFileWriterForLstDebug:
    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)
        pass

    def write_lst_file(self, mesh_data, output_dir, file_name_lst):
        os.makedirs(output_dir, exist_ok=True)

        file_name_msh = file_name_lst + ".msh"
        file_name_dat_node = file_name_lst + "_node.dat"
        file_name_dat_face = file_name_lst + "_face.dat"
        file_name_dat_element = file_name_lst + "_element.dat"
        file_name_dat_node_id = file_name_lst + "_node_id.dat"
        file_path_lst = os.path.join(output_dir, file_name_lst)
        file_path_msh = os.path.join(output_dir, file_name_msh)
        file_path_dat_node = os.path.join(output_dir, file_name_dat_node)
        file_path_dat_face = os.path.join(output_dir, file_name_dat_face)
        file_path_dat_element = os.path.join(output_dir, file_name_dat_element)
        file_path_dat_node_id = os.path.join(output_dir, file_name_dat_node_id)

        self.logger.info(f'save lst file : {file_path_lst}')
        file_lst = open(file_path_lst, 'w')
        file_lst.write(f'{file_name_msh}\n')
        file_lst.write(f'\n')
        file_lst.write(f'4\n')
        file_lst.write(f'{file_name_dat_node}\n')
        file_lst.write(f'{file_name_dat_face}\n')
        file_lst.write(f'{file_name_dat_element}\n')
        file_lst.write(f'{file_name_dat_node_id}\n')

        file_lst.close()

        self.write_msh_dat_file(mesh_data, file_path_msh,
                                file_path_dat_node, file_path_dat_face,
                                file_path_dat_element, file_path_dat_node_id)
        pass

    def write_msh_dat_file(self, mesh_data, file_path_msh,
                           file_path_dat_node,
                           file_path_dat_face,
                           file_path_dat_element,
                           file_path_dat_node_id
                          ):
        self.logger.info(f'save msh file : {file_path_msh}')
        self.logger.info(f'save dat file : {file_path_dat_node}')
        self.logger.info(f'save dat file : {file_path_dat_face}')
        self.logger.info(f'save dat file : {file_path_dat_element}')
        self.logger.info(f'save dat file : {file_path_dat_node_id}')
        file_msh = open(file_path_msh, 'w')
        file_dat_node = open(file_path_dat_node, 'w')
        file_dat_face = open(file_path_dat_face, 'w')
        file_dat_element = open(file_path_dat_element, 'w')
        file_dat_node_id = open(file_path_dat_node_id, 'w')

        min_coords = mesh_data.get_min_coords()
        max_coords = mesh_data.get_max_coords()
        # set base point at min coords
        coords_base_point = min_coords
        # set base point at center of bounding box
        # coords_base_point = (max_coords[0] - min_coords[0],
        #                      max_coords[1] - min_coords[1],
        #                      max_coords[2] - min_coords[2])

        num_nodes = mesh_data.get_num_nodes()
        nodes_df = mesh_data.get_nodes_df()
        coords_x = nodes_df[COLUMN_X].values
        coords_y = nodes_df[COLUMN_Y].values
        coords_z = nodes_df[COLUMN_Z].values

        elements_df = mesh_data.get_elements_df()
        num_elements = mesh_data.get_num_elements()
        nodes = [elements_df[COLUMN_NODE_0].values, elements_df[COLUMN_NODE_1].values,
                 elements_df[COLUMN_NODE_2].values, elements_df[COLUMN_NODE_3].values,
                 elements_df[COLUMN_NODE_4].values, elements_df[COLUMN_NODE_5].values,
                 elements_df[COLUMN_NODE_6].values, elements_df[COLUMN_NODE_7].values]
        # self.logger.info(f'nodes={nodes}')

        # write elements
        file_msh.write(f'{num_elements}\n')
        for i_element in range(num_elements):
            if i_element > 0 and i_element % LOGGER_INTERVAL == 0:
                self.logger.info(f'save msh connectivity : {i_element} / {num_elements}')

            ix8 = i_element * NUM_NODES_OF_ELEMENT
            line = f'{ix8} {ix8+1} {ix8+3} {ix8+2} {ix8+4} {ix8+5} {ix8+7} {ix8+6}\n'
            file_msh.write(line)

        # write coords
        file_msh.write(f'{num_elements * NUM_NODES_OF_ELEMENT}\n')
        for i_element in range(num_elements):
            if i_element > 0 and i_element % LOGGER_INTERVAL == 0:
                self.logger.info(f'save msh coords : {i_element} / {num_elements}')

            distance = 0
            move_x = 0
            move_y = 0
            move_z = 0
            for node_in_element in range(NUM_NODES_OF_ELEMENT):
                node_index = nodes[node_in_element][i_element]
                # self.logger.info(f'node_index={node_index}')
                x = coords_x[node_index]
                y = coords_y[node_index]
                z = coords_z[node_index]
                diff_x = x - coords_base_point[0]
                diff_y = y - coords_base_point[1]
                diff_z = z - coords_base_point[2]
                tmp_distance = math.sqrt(diff_x*diff_x + diff_y*diff_y + diff_z*diff_z)
                if node_in_element == 0:
                    distance = tmp_distance
                    move_x = diff_x
                    move_y = diff_y
                    move_z = diff_z
                elif distance > tmp_distance:
                    distance = tmp_distance
                    move_x = diff_x
                    move_y = diff_y
                    move_z = diff_z

            move_x *= 1.2
            move_y *= 1.2
            move_z *= 1.2

            for node_in_element in range(NUM_NODES_OF_ELEMENT):
                node_index = nodes[node_in_element][i_element]
                x = coords_x[node_index] + move_x
                y = coords_y[node_index] + move_y
                z = coords_z[node_index] + move_z
                line = f'{x} {y} {z}\n'
                file_msh.write(line)
                # self.logger.info(f'node_index={node_index}, line={line}')

        # write values
        num_items = num_elements * NUM_NODES_OF_ELEMENT
        file_dat_node.write(f'label=node\n')
        file_dat_node.write(f'num_items={num_items}\n')
        file_dat_node.write(f'\n')
        file_dat_face.write(f'label=face\n')
        file_dat_face.write(f'num_items={num_items}\n')
        file_dat_face.write(f'\n')
        file_dat_element.write(f'label=element\n')
        file_dat_element.write(f'num_items={num_items}\n')
        file_dat_element.write(f'\n')
        file_dat_node_id.write(f'label=node_id\n')
        file_dat_node_id.write(f'num_items={num_items}\n')
        file_dat_node_id.write(f'\n')
        for i_element in range(num_elements):
            if i_element > 0 and i_element % LOGGER_INTERVAL == 0:
                self.logger.info(f'save dat : {i_element} / {num_elements}')

            ix8 = i_element * NUM_NODES_OF_ELEMENT

            flag_node_0 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_1 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_2 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_3 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_4 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_5 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_6 = [0] * NUM_NODES_OF_ELEMENT
            flag_node_7 = [0] * NUM_NODES_OF_ELEMENT

            flag_face_0 = [0] * NUM_NODES_OF_ELEMENT
            flag_face_1 = [0] * NUM_NODES_OF_ELEMENT
            flag_face_2 = [0] * NUM_NODES_OF_ELEMENT
            flag_face_3 = [0] * NUM_NODES_OF_ELEMENT
            flag_face_4 = [0] * NUM_NODES_OF_ELEMENT
            flag_face_5 = [0] * NUM_NODES_OF_ELEMENT

            flag_node_0[0] = 1
            flag_node_1[1] = 1
            flag_node_2[2] = 1
            flag_node_3[3] = 1
            flag_node_4[4] = 1
            flag_node_5[5] = 1
            flag_node_6[6] = 1
            flag_node_7[7] = 1

            for node_in_face in range(NUM_NODES_OF_FACE):
                flag_face_0[NODES_OF_FACE[0][node_in_face]] = 1
                flag_face_1[NODES_OF_FACE[1][node_in_face]] = 1
                flag_face_2[NODES_OF_FACE[2][node_in_face]] = 1
                flag_face_3[NODES_OF_FACE[3][node_in_face]] = 1
                flag_face_4[NODES_OF_FACE[4][node_in_face]] = 1
                flag_face_5[NODES_OF_FACE[5][node_in_face]] = 1

            for node_in_element in range(NUM_NODES_OF_ELEMENT):
                line = f'{ix8+node_in_element}: ' \
                       f'{flag_node_0[node_in_element]} {flag_node_1[node_in_element]} ' \
                       f'{flag_node_2[node_in_element]} {flag_node_3[node_in_element]} ' \
                       f'{flag_node_4[node_in_element]} {flag_node_5[node_in_element]} ' \
                       f'{flag_node_6[node_in_element]} {flag_node_7[node_in_element]} ' \
                       f'\n'
                file_dat_node.write(line)

                line = f'{ix8+node_in_element}: ' \
                       f'{flag_face_0[node_in_element]} {flag_face_1[node_in_element]} ' \
                       f'{flag_face_2[node_in_element]} {flag_face_3[node_in_element]} ' \
                       f'{flag_face_4[node_in_element]} {flag_face_5[node_in_element]} ' \
                       f'\n'
                file_dat_face.write(line)

                line = f'{ix8 + node_in_element}: ' \
                       f'{i_element} ' \
                       f'\n'
                file_dat_element.write(line)

                line = f'{ix8 + node_in_element}: ' \
                       f'{nodes[node_in_element][i_element]} ' \
                       f'\n'
                file_dat_node_id.write(line)

        file_msh.close()
        file_dat_node.close()
        file_dat_face.close()
        file_dat_element.close()
        file_dat_node_id.close()
        pass

