# import logging
# import numpy as np
# import pandas as pd
import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)
# from ansys_file_reader import AnsysFileReader
# from constants import NODES_COLUMNS
# from mesh_data import MeshData
# from mesh_file_writer import MeshFileWriter
# from merge_nodes import MergeNodes
from main import main
# test


def test_main_single_volume():
    # test file, output_folder_name
    #  test_file_path = 'src/tests/test_ds.dat'
    #
    # test_output_path = 'output'
    # print(f'test_file_path={test_file_path}')
    #
    # main(test_file_path, test_output_path, 1)
    pass


# test_main_single_volume()

"""
def test_main_multiple_volume():
    # test file, output_folder_name
    test_file_path = 'src/tests/test_multi.dat'
    test_output_path = 'output'

    # test of file name
    main(test_file_path, test_output_path, 1)

test_main_multiple_volume()
"""


"""
def test_main_large_file():
    # test file, output_folder_name
    test_file_path = 'src/tests/test_multi.dat'
    test_output_path = 'output'

    # test of file name
    main(test_file_path, test_output_path, 1)

test_main_large_file()
"""
