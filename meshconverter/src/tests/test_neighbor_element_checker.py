import numpy as np
import pandas as pd
import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
from ansys_file_reader import AnsysFileReader
from mesh_data import MeshData
from merge_nodes import MergeNodes
from neighbor_element_checker import NeighborElementChecker
cwd = os.getcwd()
sep = os.sep


def test():
    # path = 'src/tests/test_ds.dat'
    # ansys_reader = AnsysFileReader(path)
    # info_start_line = ansys_reader.get_info_start_line()
    # elements_info_start_lines = info_start_line[1]
    # texts = info_start_line[2]
    # test_nodes_info_start_line = 21
    # test_nodes_start = 23
    # test_nodes_info_length = 29
    # _test_elements_infos = np.array([[0, 10, 18, 22, 24, 14, 15, 23],
    #                                  [0, 10, 16, 19, 22, 18, 17, 20],
    #                                  [0, 22, 8, 1, 24, 23, 6, 5],
    #                                  [0, 19, 7, 1, 22, 20, 9, 8],
    #                                  [0, 19, 16, 10, 26, 21, 11, 12],
    #                                  [0, 10, 14, 24, 26, 12, 13, 25],
    #                                  [0, 1, 7, 19, 26, 3, 2, 21],
    #                                  [0, 24, 5, 1, 26, 25, 4, 3]])
    #
    # node_exclude_list = ansys_reader.get_nodes_exclude_index_list(test_nodes_start, test_nodes_info_length, texts)
    # my_columns = ['index', 'x', 'y', 'z']
    # node_df = pd.read_csv(path, skiprows=node_exclude_list, encoding='shift-jis', delim_whitespace=True, names=my_columns)
    #
    #
    # """
    # test for elements df
    # """
    # all_info = ansys_reader.get_info_start_line()
    # print(f'single_all_info={all_info}')
    # elements_info_start_lines = all_info[1]
    # single_elements = ansys_reader.get_elements_info_areas(elements_info_start_lines, texts)
    # print(f'single_elements={single_elements}')
    # elements_info_area = ansys_reader.get_elements_info_areas(all_info[1], texts)
    # print(f'single_elements_info_area={elements_info_area}')
    # # start_lines, lengths, element_ids
    # assert elements_info_area == ([56], [8], [1])
    # elements_starts = elements_info_area[0]
    # elements_exclude_list = ansys_reader.get_elements_exclude_index_list(elements_info_area[0], elements_info_area[1], texts)
    # my_element_columns = ['dummy1', 'dummy2', 'dummy3', 'dummy4', 'dummy5', 'dummy6', 'dummy7', 'dummy8', 'ElementType',
    #                       'dummy9', 'ElementId', 'Node0', 'Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7']
    # pd.set_option('display.max_columns', 100)
    # print(path, elements_exclude_list)
    # elements_df = ansys_reader.create_elements_df(path, elements_exclude_list, elements_info_area[1])[0]
    # print(f'single_element_df={elements_df}')
    # assert elements_df['Node0'][0] == 0
    #
    #
    # print('node_pandas=', node_df)
    # MD = MeshData(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    # print(f'element_pandas={elements_df}')
    # MD.num_nodes = len(node_df["x"])
    # print(texts)
    # coords = []
    # for i in range(len(node_df["x"])):
    #     coords.append(node_df["x"][i])
    #     coords.append(node_df["y"][i])
    #     coords.append(node_df["z"][i])
    # MD.set_coords(coords)
    # MD.set_num_elements_of_node(_test_elements_infos)
    # MD.set_nodes_df(node_df)
    #
    #
    # MD.set_min_coords([0, 0, 0])
    # MD.set_max_coords([1, 1, 1])
    # MD.set_tolerance(0.01)
    #
    #
    # MD.set_elements_df([elements_df])
    # MN = MergeNodes(MD)
    #
    # NE = NeighborElementChecker(MD)
    #
    # print(NE)
    # print(NE.set_node_belonginstate())
    #
    # print(NE.get_node_belonginstate())
    pass
