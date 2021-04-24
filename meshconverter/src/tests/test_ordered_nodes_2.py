import os
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_dir)

from constants import *
from mesh_data import MeshData
from mesh_file_writer_for_lst_debug import MeshFileWriterForLstDebug
import math
import numpy as np
import pandas as pd
import re
import logging


class OrderedNodesTester2:
    """[summary]
    """

    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)

        pass

    def test(self):
        mesh_data = self.create_mesh_data()

        mesh_file_writer_lst = MeshFileWriterForLstDebug()
        mesh_file_writer_lst.write_lst_file(mesh_data, "test_output", "output_1.lst")

        logging.info(f'node={mesh_data.get_nodes_df()}')
        logging.info(f'elements={mesh_data.get_elements_df()}')

    def create_mesh_data(self):
        edge_length = 1.0

        nodes_df = pd.DataFrame({})
        node_id = []
        coords_x = []
        coords_y = []
        coords_z = []
        dictionary_node_id_to_index = {}

        elements_df = pd.DataFrame({})
        element_id = []
        domain_id = []
        connectivity = [[] for i in range(8)]

        offset = 0
        for reorder_pattern_id in range(24):
            ordered_nodes = ORDERED_NODES[reorder_pattern_id]
            ordered_face_numbers = ORDERED_FACE_NUMBER[reorder_pattern_id]

            index1 = reorder_pattern_id % 4
            index2 = reorder_pattern_id // 4
            x0 = index1 * 1.2 * edge_length
            y0 = index2 * 1.2 * edge_length
            z0 = 0.0
            x1 = x0 + edge_length
            y1 = y0
            z1 = z0
            x2 = x0
            y2 = y0 + edge_length
            z2 = z0
            x3 = x0 + edge_length
            y3 = y0 + edge_length
            z3 = z0
            x4 = x0
            y4 = y0
            z4 = z0 + edge_length
            x5 = x1
            y5 = y1
            z5 = z1 + edge_length
            x6 = x2
            y6 = y2
            z6 = z2 + edge_length
            x7 = x3
            y7 = y3
            z7 = z3 + edge_length

            p0 = offset
            p1 = p0 + 1
            p2 = p0 + 2
            p3 = p0 + 3
            p4 = p0 + 4
            p5 = p0 + 5
            p6 = p0 + 6
            p7 = p0 + 7
            offset += 8

            tmp_x = [x0, x1, x2, x3, x4, x5, x6, x7]
            tmp_y = [y0, y1, y2, y3, y4, y5, y6, y7]
            tmp_z = [z0, z1, z2, z3, z4, z5, z6, z7]
            tmp_connectivity = [p0, p1, p2, p3, p4, p5, p6, p7]

            dictionary_node_id_to_index[p0] = p0
            dictionary_node_id_to_index[p1] = p1
            dictionary_node_id_to_index[p2] = p2
            dictionary_node_id_to_index[p3] = p3
            dictionary_node_id_to_index[p4] = p4
            dictionary_node_id_to_index[p5] = p5
            dictionary_node_id_to_index[p6] = p6
            dictionary_node_id_to_index[p7] = p7

            node_id.extend(tmp_connectivity)

            element_id.append(reorder_pattern_id)
            domain_id.append(0)

            for i in range(8):
                coords_x.append(tmp_x[ordered_nodes[i]])
                coords_y.append(tmp_y[ordered_nodes[i]])
                coords_z.append(tmp_z[ordered_nodes[i]])
                connectivity[i].append(tmp_connectivity[ordered_nodes[i]])

        num_nodes = offset
        num_elements = 24
        num_domains = 1

        min_coords = [min(coords_x), min(coords_y), min(coords_z)]
        max_coords = [max(coords_x), max(coords_y), max(coords_z)]

        x_length = max_coords[0] - min_coords[0]
        y_length = max_coords[1] - min_coords[1]
        z_length = max_coords[2] - min_coords[2]
        box_length = math.sqrt(x_length * x_length + y_length * y_length + z_length * z_length)
        tolerance = box_length * TOLERANCE_RATE

        nodes_df[COLUMN_NODE_ID] = node_id
        nodes_df[COLUMN_X] = coords_x
        nodes_df[COLUMN_Y] = coords_y
        nodes_df[COLUMN_Z] = coords_z

        elements_df[COLUMN_ELEMENT_ID] = element_id
        elements_df[COLUMN_DOMAIN_ID] = domain_id
        elements_df[COLUMN_NODE_0] = connectivity[0]
        elements_df[COLUMN_NODE_1] = connectivity[1]
        elements_df[COLUMN_NODE_2] = connectivity[2]
        elements_df[COLUMN_NODE_3] = connectivity[3]
        elements_df[COLUMN_NODE_4] = connectivity[4]
        elements_df[COLUMN_NODE_5] = connectivity[5]
        elements_df[COLUMN_NODE_6] = connectivity[6]
        elements_df[COLUMN_NODE_7] = connectivity[7]

        mesh_data = MeshData()
        mesh_data.set_nodes(num_nodes, nodes_df, max_coords, min_coords, tolerance, dictionary_node_id_to_index)
        mesh_data.set_elements(num_elements, num_domains, elements_df)

        return mesh_data


if __name__ == '__main__':
    tester = OrderedNodesTester2()
    tester.test()
