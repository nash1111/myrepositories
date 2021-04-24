import os

from constants import *


class MeshFileWriter:
    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)
        pass

    def write_clp_mesh_file(self, mesh_data, output_dir, file_name_clp):
        os.makedirs(output_dir, exist_ok=True)

        file_path_clp = os.path.join(output_dir, file_name_clp)

        self.logger.info(f'save clp mesh file : {file_path_clp}')
        file_clp = open(file_path_clp, 'w')

        num_nodes = mesh_data.get_num_nodes()
        nodes_df = mesh_data.get_nodes_df()
        coords_x = nodes_df[COLUMN_X].values
        coords_y = nodes_df[COLUMN_Y].values
        coords_z = nodes_df[COLUMN_Z].values

        elements_df = mesh_data.get_elements_df()
        num_elements = mesh_data.get_num_elements()
        node_0 = elements_df[COLUMN_NODE_0].values
        node_1 = elements_df[COLUMN_NODE_1].values
        node_2 = elements_df[COLUMN_NODE_2].values
        node_3 = elements_df[COLUMN_NODE_3].values
        node_4 = elements_df[COLUMN_NODE_4].values
        node_5 = elements_df[COLUMN_NODE_5].values
        node_6 = elements_df[COLUMN_NODE_6].values
        node_7 = elements_df[COLUMN_NODE_7].values
        list_domain_id = elements_df[COLUMN_DOMAIN_ID].values

        element_flag = mesh_data.get_element_flag()

        num_digits_node = len(str(num_nodes))
        num_digits_element = len(str(num_elements))
        num_digits_element_flag = NUM_DIGITS_OF_ELEMENT_FLAG
        num_digits_coordinate = 16

        format_node_id_label = '^' + str(num_digits_node)
        format_coordinate_label = '^' + str(num_digits_coordinate)

        format_node_id = str(num_digits_node) + 'd'
        format_coordinate = str(num_digits_coordinate) + '.9e'
        format_element_id = str(num_digits_element) + 'd'
        format_element_flag = str(num_digits_element_flag) + 'd'

        file_clp.write(f'comment1\n')
        file_clp.write(f'comment2\n')
        file_clp.write(f'comment3\n')
        file_clp.write(f'comment4\n')
        file_clp.write(f'comment5\n')
        file_clp.write(f'comment6\n')
        file_clp.write(f'comment7\n')
        file_clp.write(f'comment8\n')
        file_clp.write(f'comment9\n')
        file_clp.write(f'comment10\n')

        # write coords
        file_clp.write(f'total_nodal_point_number={num_nodes}\n')
        file_clp.write(f'{"n":{format_node_id_label}} '
                       f'{"x":{format_coordinate_label}} '
                       f'{"y":{format_coordinate_label}} '
                       f'{"z":{format_coordinate_label}}\n')
        for i_node in range(num_nodes):
            file_clp.write(f'{i_node+1:{format_node_id}} '
                           f'{coords_x[i_node]:{format_coordinate}} '
                           f'{coords_y[i_node]:{format_coordinate}} '
                           f'{coords_z[i_node]:{format_coordinate}}\n')

        # write elements
        file_clp.write(f'data\n')
        file_clp.write(f'{num_elements:{format_element_id}}\n')
        for i_element in range(num_elements):
            line = f'{i_element + 1:{format_element_id}} ' \
                   f'{node_0[i_element] + 1:{format_node_id}} ' \
                   f'{node_1[i_element] + 1:{format_node_id}} ' \
                   f'{node_2[i_element] + 1:{format_node_id}} ' \
                   f'{node_3[i_element] + 1:{format_node_id}} ' \
                   f'{node_4[i_element] + 1:{format_node_id}} ' \
                   f'{node_5[i_element] + 1:{format_node_id}} ' \
                   f'{node_6[i_element] + 1:{format_node_id}} ' \
                   f'{node_7[i_element] + 1:{format_node_id}} ' \
                   f'{element_flag[i_element]:{format_element_flag}}\n'
            file_clp.write(line)

        file_clp.close()
        pass

    def write_merge_node_info_file(self, mesh_data, output_dir, file_name_merge_node_info):
        os.makedirs(output_dir, exist_ok=True)

        file_path_merge_node_info = os.path.join(output_dir, file_name_merge_node_info)

        self.logger.info(f'save merge node info file : {file_path_merge_node_info}')
        file_merge_node_info = open(file_path_merge_node_info, 'w')

        num_nodes_old = mesh_data.get_num_nodes_old()
        map_merge_nodes = mesh_data.get_map_merge_nodes()
        dictionary_node_id_to_index = mesh_data.get_dictionary_node_id_to_index()

        for key in dictionary_node_id_to_index:
            value = dictionary_node_id_to_index[key]
            file_merge_node_info.write(f'{key} {map_merge_nodes[value] + 1}\n')

        file_merge_node_info.close()
        pass

    def write_domain_id_file(self, mesh_data, output_dir, file_name_domain_id):
        os.makedirs(output_dir, exist_ok=True)

        file_path_domain_id = os.path.join(output_dir, file_name_domain_id)

        self.logger.info(f'save domain id file : {file_path_domain_id}')
        file_domain_id = open(file_path_domain_id, 'w')

        num_elements = mesh_data.get_num_elements()
        elements_df = mesh_data.get_elements_df()
        domain_id = elements_df[COLUMN_DOMAIN_ID]

        for i_element in range(num_elements):
            file_domain_id.write(f'{i_element + 1} {domain_id[i_element]}\n')

        file_domain_id.close()
        pass

    def write_msh_file(self, mesh_data, output_dir, file_name_msh):
        os.makedirs(output_dir, exist_ok=True)

        file_path_msh = os.path.join(output_dir, file_name_msh)

        self.logger.info(f'save msh file : {file_path_msh}')
        file_msh = open(file_path_msh, 'w')

        num_nodes = mesh_data.get_num_nodes()
        nodes_df = mesh_data.get_nodes_df()
        coords_x = nodes_df[COLUMN_X].values
        coords_y = nodes_df[COLUMN_Y].values
        coords_z = nodes_df[COLUMN_Z].values

        elements_df = mesh_data.get_elements_df()
        num_elements = mesh_data.get_num_elements()
        node_0 = elements_df[COLUMN_NODE_0].values
        node_1 = elements_df[COLUMN_NODE_1].values
        node_2 = elements_df[COLUMN_NODE_2].values
        node_3 = elements_df[COLUMN_NODE_3].values
        node_4 = elements_df[COLUMN_NODE_4].values
        node_5 = elements_df[COLUMN_NODE_5].values
        node_6 = elements_df[COLUMN_NODE_6].values
        node_7 = elements_df[COLUMN_NODE_7].values
        list_domain_id = elements_df[COLUMN_DOMAIN_ID]
        self.logger.info(f'list_domain_id={list_domain_id}, {type(list_domain_id)}')

        # write elements
        file_msh.write(f'{num_elements}\n')
        for i_element in range(num_elements):
            line = f'' \
                   f'{node_0[i_element]} ' \
                   f'{node_1[i_element]} ' \
                   f'{node_3[i_element]} ' \
                   f'{node_2[i_element]} ' \
                   f'{node_4[i_element]} ' \
                   f'{node_5[i_element]} ' \
                   f'{node_7[i_element]} ' \
                   f'{node_6[i_element]}\n'
            file_msh.write(line)

        # write coords
        file_msh.write(f'{num_nodes}\n')
        for i_node in range(num_nodes):
            line = f'' \
                   f'{coords_x[i_node]} ' \
                   f'{coords_y[i_node]} ' \
                   f'{coords_z[i_node]}\n'
            file_msh.write(line)

        min_domain_id = min(list_domain_id)
        max_domain_id = max(list_domain_id)
        counts_list_domain_id = list_domain_id.value_counts()
        file_msh.write(f'{max_domain_id-min_domain_id+1}\n')
        for domain_id in range(min_domain_id, max_domain_id + 1):
            num_elements_in_domain = counts_list_domain_id[domain_id]
            file_msh.write(f'{num_elements_in_domain}\n')
            for i_element in range(num_elements):
                if list_domain_id[i_element] == domain_id:
                    file_msh.write(f'{i_element}\n')

        self.logger.info(f'elements_df={elements_df}')

        file_msh.close()
        pass

