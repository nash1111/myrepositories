import argparse
import os
import random
import sys

from ansys_file_reader import AnsysFileReader
from constants import *
from mesh_data import MeshData
from mesh_file_writer import MeshFileWriter


def main(input_file, output_folder):
    path = input_file

    # create output folder if not exits
    os.makedirs(output_folder, exist_ok=True)

    mesh_data = MeshData()

    # load ansys file
    reader = AnsysFileReader()
    reader.read(path, mesh_data)
    logging.info(f'node={mesh_data.get_nodes_df()}')
    logging.info(f'elements={mesh_data.get_elements_df()}')

    elements_df = mesh_data.get_elements_df()

    for element_index in range(mesh_data.get_num_elements()):
        # get node0~node7
        column_node_list = [COLUMN_NODE_0, COLUMN_NODE_1, COLUMN_NODE_2, COLUMN_NODE_3,
                            COLUMN_NODE_4, COLUMN_NODE_5, COLUMN_NODE_6, COLUMN_NODE_7]
        elements_before_shuffle = elements_df.loc[element_index, column_node_list]

        shuffle_methods = random.choice(ORDERED_NODES)
        shuffled_list = []
        for shuffle_method in shuffle_methods:
            shuffled_list.append(elements_before_shuffle[shuffle_method])

        for shuffle_index in range(len(shuffled_list)):
            elements_df.loc[element_index, column_node_list[shuffle_index]] = shuffled_list[shuffle_index]

    mesh_data.set_elements_df(elements_df)

    mesh_file_writer = MeshFileWriter()
    mesh_file_writer.write_msh_file(mesh_data, output_folder, "output_1.msh")


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        parser = argparse.ArgumentParser(description='1 file and 1 directory needed')
        parser.add_argument('files', metavar='files', type=str, nargs=2,
                            help='input_file, output_directory')
        args = parser.parse_args()
        input_file_name, output_folder_name = args.files[0], args.files[1]
        main(input_file_name, output_folder_name)
    else:
        sys.exit("usage : python main.py input.dat output_dir")

