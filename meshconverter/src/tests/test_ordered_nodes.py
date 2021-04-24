import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)

from constants import *
from mesh_data import MeshData
import math
import numpy as np
import pandas as pd
import re
import logging


class OrderedNodesTester:
    """[summary]
    """

    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)

        pass

    def test(self):
        for reorder_pattern_id in range(len(ORDERED_NODES)):
            ordered_nodes = ORDERED_NODES[reorder_pattern_id]
            ordered_face_numbers = ORDERED_FACE_NUMBER[reorder_pattern_id]

            for face_id in range(NUM_FACES_OF_ELEMENT):
                node_before_0 = NODES_OF_FACE[face_id][0]
                node_before_1 = NODES_OF_FACE[face_id][1]
                node_before_2 = NODES_OF_FACE[face_id][2]
                node_before_3 = NODES_OF_FACE[face_id][3]

                face_id_after = ordered_face_numbers[face_id]
                node_after_0 = ordered_nodes[NODES_OF_FACE[face_id_after][0]]
                node_after_1 = ordered_nodes[NODES_OF_FACE[face_id_after][1]]
                node_after_2 = ordered_nodes[NODES_OF_FACE[face_id_after][2]]
                node_after_3 = ordered_nodes[NODES_OF_FACE[face_id_after][3]]

                nodes_before = {node_before_0, node_before_1, node_before_2, node_before_3}
                nodes_after = {node_after_0, node_after_1, node_after_2, node_after_3}

                self.logger.info(f'nodes_before={nodes_before}\nnodes_after={nodes_after}')

                if nodes_before == nodes_after:
                    self.logger.info(f'passed : reorder_pattern_id={reorder_pattern_id} : face_id={face_id}')
                    pass
                else:
                    self.logger.warning(f'error : reorder_pattern_id={reorder_pattern_id} : face_id={face_id}')


if __name__ == '__main__':
    tester = OrderedNodesTester()
    tester.test()
