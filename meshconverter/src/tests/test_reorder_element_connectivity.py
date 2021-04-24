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
from reorder_element_connectivity import ReorderElementConnectivity
cwd = os.getcwd()
sep = os.sep

