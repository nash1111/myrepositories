# import pandas as pd
import argparse
import os
import sys
import time

from ansys_file_reader import AnsysFileReader
from constants import *
from merge_nodes import MergeNodes
from mesh_data import MeshData
from mesh_file_writer import MeshFileWriter
from mesh_file_writer_for_lst_debug import MeshFileWriterForLstDebug
from neighbor_element_checker import NeighborElementChecker
from reorder_element_connectivity import ReorderElementConnectivity


def main(input_file, output_folder):
    """[summary]
    Args:
        input_file ([str]): 入力ファイル
        output_folder ([str]): 出力ディレクトリ
    """

    logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)

    time_start = time.time()

    path = input_file

    # 出力先ディレクトリを作成する
    os.makedirs(output_folder, exist_ok=True)

    # メッシュデータを格納するオブジェクト
    mesh_data = MeshData()

    # Ansysファイルを読み込む
    reader = AnsysFileReader()
    reader.read(path, mesh_data)
    logging.info(f'node={mesh_data.get_nodes_df()}')
    logging.info(f'elements={mesh_data.get_elements_df()}')

    # 節点をマージする
    merge_nodes = MergeNodes()
    merge_nodes.merge(mesh_data)

    # 要素の隣接関係を計算する
    neighbor_element_checker = NeighborElementChecker()
    neighbor_element_checker.check(mesh_data)

    # 要素内の節点順序並び替えと、要素へのフラグ設定を行う
    reorder_element_connectivity = ReorderElementConnectivity()
    reorder_element_connectivity.reorder(mesh_data)

    # メッシュファイルなどを出力する
    mesh_file_writer = MeshFileWriter()
    mesh_file_writer.write_clp_mesh_file(mesh_data, output_folder, "output_mesh.ms")
    mesh_file_writer.write_merge_node_info_file(mesh_data, output_folder, "output_merge_node_info.dat")
    mesh_file_writer.write_domain_id_file(mesh_data, output_folder, "output_domain_id.dat")
    mesh_file_writer.write_msh_file(mesh_data, output_folder, "output.msh")

    mesh_file_writer_lst = MeshFileWriterForLstDebug()
    mesh_file_writer_lst.write_lst_file(mesh_data, output_folder, "output.lst")

    time_end = time.time()
    logging.info(f'elapse time {time_end - time_start}[sec]')


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
