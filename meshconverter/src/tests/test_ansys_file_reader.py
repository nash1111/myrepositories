import logging
import pandas as pd
import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
from ansys_file_reader import AnsysFileReader
cwd = os.getcwd()
sep = os.sep


def test_single_volume_ansysfilereader():
    # path = 'src/tests/test_ds.dat'
    # ansys_reader = AnsysFileReader(path)
    # info_start_line = ansys_reader.get_info_start_line()
    # elements_info_start_lines = info_start_line[1]
    # texts = info_start_line[2]
    # test_nodes_start = 23
    # test_nodes_info_length = 29
    # nodes_start = ansys_reader.get_info_start_line()[0]
    # nodes_info = ansys_reader.get_nodes_info_area(nodes_start, texts)
    # print(f'nodes_info={nodes_info}')
    # nodes_start = nodes_info[0]
    # nodes_length = nodes_info[1]
    #
    # assert nodes_start == test_nodes_start
    #
    # assert nodes_length == test_nodes_info_length
    #
    # node_exclude_list = ansys_reader.get_nodes_exclude_index_list(test_nodes_start, test_nodes_info_length, texts)
    # my_columns = ['index', 'x', 'y', 'z']
    # node_df = pd.read_csv(path, skiprows=node_exclude_list, encoding='shift-jis', delim_whitespace=True, names=my_columns)
    # print(f'node_df =\n{node_df}')
    #
    # """
    # test for elements df
    # """
    #
    # all_info = ansys_reader.get_info_start_line()
    # print(f'single_all_info={all_info}')
    #
    # elements_info_start_lines = all_info[1]
    # single_elements = ansys_reader.get_elements_info_areas(elements_info_start_lines, texts)
    # print(f'single_elements={single_elements}')
    #
    # elements_info_area = ansys_reader.get_elements_info_areas(all_info[1], texts)
    # print(f'single_elements_info_area={elements_info_area}')
    #
    # # start_lines, lengths, element_ids
    # assert elements_info_area == ([56], [8], [1])
    #
    # elements_exclude_list = ansys_reader.get_elements_exclude_index_list(elements_info_area[0], elements_info_area[1], texts)
    # pd.set_option('display.max_columns', 100)
    # print(path, elements_exclude_list)
    # elements_df = ansys_reader.create_elements_df(path, elements_exclude_list, elements_info_area[1])[0]
    #
    # print(f'single_element_df={elements_df}')
    # assert elements_df['Node0'][0] == 0

    pass


def test_multi_volume_ansysfilereader():
    # path = 'src/tests/test_multi.dat'
    # ansys_reader = AnsysFileReader(path)
    # info_start_line = ansys_reader.get_info_start_line()
    # elements_info_start_lines = info_start_line[1]
    # texts = info_start_line[2]
    # test_nodes_info_start_line = 21
    # test_nodes_start = 23
    # test_nodes_info_length = 26
    # _test_elements_starts = [53, 61]
    # _test_elements_lengths = [2, 2]
    #
    # all_info = ansys_reader.get_info_start_line()
    # print(f'multi_all_info={all_info}')
    #
    # multi_elements = ansys_reader.get_elements_info_areas(elements_info_start_lines, texts)
    # print(f'multi_elements={multi_elements}')
    #
    # ansys_reader.get_nodes_info_area(test_nodes_info_start_line, texts)
    # node_exclude_list = ansys_reader.get_nodes_exclude_index_list(test_nodes_start, test_nodes_info_length, texts)
    #
    # my_columns = ['index', 'x', 'y', 'z']
    # node_df = pd.read_csv(path, skiprows=node_exclude_list, encoding='shift-jis', delim_whitespace=True, names=my_columns)
    # print(f'node_df =\n{node_df}')
    #
    # elements_info_area = ansys_reader.get_elements_info_areas(elements_info_start_lines, texts)
    # # assert elements_info_area[0] == _test_elements_starts
    # logging.info(f'elements_info_area={elements_info_area}')
    #
    # elements_exclude_list = ansys_reader.get_elements_exclude_index_list(_test_elements_starts, _test_elements_lengths, texts)
    # print(f'multi_elements_exclude={elements_exclude_list}')
    # # pd.set_option('display.max_columns', 100)
    # elements_df = ansys_reader.create_elements_df(path, elements_exclude_list, _test_elements_lengths)
    #
    # print(f'elements_dfs{elements_df}')

    pass


# test_single_volume_ansysfilereader()

# test_multi_volume_ansysfilereader()
