import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
from ansys_file_reader import AnsysFileReader
from mesh_data import MeshData
cwd = os.getcwd()
sep = os.sep


def test():
    # answeres
    # test_input_file = cwd + sep + 'src' + sep + 'tests' + sep + 'test_ds.dat'
    # test_multi_elements_input_file = cwd + sep + 'src' + sep + 'tests' + sep + 'test_multi.dat'
    # test_large = cwd + sep + 'src' + sep + 'tests' + sep + 'test_multi_large.dat'
    # test_nodes_info_start_line = 21
    # test_nodes_info_length = 29
    # test_nodes_start = 23
    # test_nodes_end = 50
    #
    # test_elements_info_start_lines = [53]
    #
    # create instance
    # AS = AnsysFileReader(test_input_file)
    # MULTI_AS = AnsysFileReader(test_multi_elements_input_file)
    # LARGE_AS = AnsysFileReader(test_large)
    #
    # texts = AS.get_info_start_line()[2]
    # nodes_info = AS.get_nodes_info(test_nodes_start, test_nodes_info_length, texts)
    # np_nodes_info = AS.get_parsed_nodes(nodes_info)
    # nodes_pandas = AS.create_nodes_pandas(np_nodes_info)
    pass


def test_num_nodes():
    # # 適当に初期化
    # MD = MeshData(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    #
    # # num_nodesに値をset
    # MD.num_nodes = nodes_pandas.count().sum()
    # # num_nodesのテスト
    # assert 4 == MD.get_num_nodes()
    pass


def test_num_domains():
    # _test_elements_start_lines = [50, 58]
    #
    # texts = MULTI_AS.get_info_start_line()[2]
    #
    # MD = MeshData(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    # MD.num_domains = len(MULTI_AS.get_elements_info_areas(_test_elements_start_lines, texts)[2])
    # # 領域が2つあることのテスト
    # assert MD.num_domains == 2
    pass


# test_num_nodes()
# test_num_domains()
