import pandas as pd

from constants import *


class MergeNodes:
    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)

        self.mesh_data = None
        self.min_coords = None
        self.max_coords = None
        self.bucket_length = None
        self.num_buckets_x = None
        self.num_buckets_y = None
        self.num_buckets_z = None
        self.num_nodes_in_bucket = None
        self.node_ids_in_bucket = None
        self.map_merge_nodes = None
        pass

    def merge(self, mesh_data):
        """
        節点のマージを行う。
        """
        self.mesh_data = mesh_data
        self.prepare_merge()
        self.merge_nodes()
        self.node_renumbering()

        self.logger.info(f'finish merge()')
        pass

    def to_bucket_index_x(self, x):
        return int((x - self.min_coords[0]) / self.bucket_length)

    def to_bucket_index_y(self, y):
        return int((y - self.min_coords[1]) / self.bucket_length)

    def to_bucket_index_z(self, z):
        return int((z - self.min_coords[2]) / self.bucket_length)

    def prepare_merge(self):
        """
        節点マージに使用するバケットを作成する。
        """
        mesh_data = self.mesh_data
        nodes_df = mesh_data.get_nodes_df()
        tolerance = mesh_data.get_tolerance()

        num_nodes_before = mesh_data.get_num_nodes()
        coords_x = nodes_df[COLUMN_X].values
        coords_y = nodes_df[COLUMN_Y].values
        coords_z = nodes_df[COLUMN_Z].values
        max_coords = mesh_data.get_max_coords()
        min_coords = mesh_data.get_min_coords()
        self.max_coords = max_coords
        self.min_coords = min_coords
        range_x = max_coords[0] - min_coords[0]
        range_y = max_coords[1] - min_coords[1]
        range_z = max_coords[2] - min_coords[2]
        count_dimension = 0
        if range_x > tolerance:
            count_dimension += 1
        if range_y > tolerance:
            count_dimension += 1
        if range_z > tolerance:
            count_dimension += 1
        volume = range_x * range_y * range_z
        bucket_length = (volume / num_nodes_before) ** (1.0 / count_dimension)
        self.bucket_length = bucket_length
        self.logger.info(f'num_nodes_before={num_nodes_before}')
        self.logger.info(f'count_dimension={count_dimension}')
        self.logger.info(f'bucket_length={bucket_length}')

        num_buckets_x = int(range_x / bucket_length) + 1
        num_buckets_y = int(range_y / bucket_length) + 1
        num_buckets_z = int(range_z / bucket_length) + 1
        self.num_buckets_x = num_buckets_x
        self.num_buckets_y = num_buckets_y
        self.num_buckets_z = num_buckets_z

        self.logger.info(f'num_buckets_x={num_buckets_x}')
        self.logger.info(f'num_buckets_y={num_buckets_y}')
        self.logger.info(f'num_buckets_z={num_buckets_z}')

        num_nodes_in_bucket = [[[0] * num_buckets_z \
                                for i in range(num_buckets_y)] \
                               for j in range(num_buckets_x)]
        self.num_nodes_in_bucket = num_nodes_in_bucket

        for i_node in range(num_nodes_before):
            if i_node > 0 and i_node % LOGGER_INTERVAL == 0:
                self.logger.info(f'make num_nodes_in_bucket : {i_node} / {num_nodes_before}')
            x = coords_x[i_node]
            y = coords_y[i_node]
            z = coords_z[i_node]
            bucket_id_x = int((x - min_coords[0]) / bucket_length)
            bucket_id_y = int((y - min_coords[1]) / bucket_length)
            bucket_id_z = int((z - min_coords[2]) / bucket_length)
            # self.logger.info(f'bucket_id_x={bucket_id_x}, bucket_id_y={bucket_id_y}, bucket_id_z={bucket_id_z}')
            tmp_num_nodes = num_nodes_in_bucket[bucket_id_x][bucket_id_y][bucket_id_z]
            num_nodes_in_bucket[bucket_id_x][bucket_id_y][bucket_id_z] = tmp_num_nodes + 1

        # self.logger.info(f'num_nodes_in_bucket={num_nodes_in_bucket}')

        node_ids_in_bucket = [[[[] for i in range(num_buckets_z)] \
                               for i in range(num_buckets_y)] \
                              for j in range(num_buckets_x)]
        self.node_ids_in_bucket = node_ids_in_bucket

        for i_node in range(num_nodes_before):
            if i_node > 0 and i_node % LOGGER_INTERVAL == 0:
                self.logger.info(f'make node_ids_in_bucket : {i_node} / {num_nodes_before}')
            x = coords_x[i_node]
            y = coords_y[i_node]
            z = coords_z[i_node]
            bucket_id_x = int((x - min_coords[0]) / bucket_length)
            bucket_id_y = int((y - min_coords[1]) / bucket_length)
            bucket_id_z = int((z - min_coords[2]) / bucket_length)
            node_ids_in_bucket[bucket_id_x][bucket_id_y][bucket_id_z].append(i_node)

        # self.logger.info(f'node_ids_in_bucket={node_ids_in_bucket}')
        self.logger.info(f'finish prepare_merge()')
        pass

    def merge_nodes(self):
        """
        節点マージを行う。
        """
        self.logger.info(f'start merge_nodes()')
        mesh_data = self.mesh_data
        num_nodes_in_bucket = self.num_nodes_in_bucket
        node_ids_in_bucket = self.node_ids_in_bucket
        num_nodes_before = mesh_data.get_num_nodes()
        nodes_df = mesh_data.get_nodes_df()
        tolerance = mesh_data.get_tolerance()

        NOT_PROCESSED = -1
        map_merge_nodes = {}
        for i_node in range(num_nodes_before):
            map_merge_nodes[i_node] = NOT_PROCESSED

        coords_x = nodes_df[COLUMN_X].values
        coords_y = nodes_df[COLUMN_Y].values
        coords_z = nodes_df[COLUMN_Z].values

        num_buckets_x = self.num_buckets_x
        num_buckets_y = self.num_buckets_y
        num_buckets_z = self.num_buckets_z

        for i_node in range(num_nodes_before):
            if i_node > 0 and i_node % LOGGER_INTERVAL == 0:
                self.logger.info(f'merge_nodes : {i_node} / {num_nodes_before}')
            is_processed = False
            node_a = i_node
            node_a_x = coords_x[node_a]
            node_a_y = coords_y[node_a]
            node_a_z = coords_z[node_a]

            node_a_x_index = self.to_bucket_index_x(node_a_x)
            node_a_y_index = self.to_bucket_index_y(node_a_y)
            node_a_z_index = self.to_bucket_index_z(node_a_z)

            x_index_min = node_a_x_index - 1
            y_index_min = node_a_y_index - 1
            z_index_min = node_a_z_index - 1

            x_index_max = node_a_x_index + 1
            y_index_max = node_a_y_index + 1
            z_index_max = node_a_z_index + 1

            if x_index_max >= num_buckets_x:
                x_index_max = num_buckets_x - 1
            if y_index_max >= num_buckets_y:
                y_index_max = num_buckets_y - 1
            if z_index_max >= num_buckets_z:
                z_index_max = num_buckets_z - 1
            if x_index_min < 0:
                x_index_min = 0
            if y_index_min < 0:
                y_index_min = 0
            if z_index_min < 0:
                z_index_min = 0

            for index_x in range(x_index_min, x_index_max + 1):
                for index_y in range(y_index_min, y_index_max + 1):
                    for index_z in range(z_index_min, z_index_max + 1):
                        tmp_num_nodes_in_bucket = num_nodes_in_bucket[index_x][index_y][index_z]
                        tmp_node_id_list = node_ids_in_bucket[index_x][index_y][index_z]
                        for node_id_in_bucket in range(tmp_num_nodes_in_bucket):
                            node_b = tmp_node_id_list[node_id_in_bucket]
                            if node_a == node_b:
                                continue
                            if map_merge_nodes[node_b] == NOT_PROCESSED:
                                continue

                            node_b_x = coords_x[node_b]
                            node_b_y = coords_y[node_b]
                            node_b_z = coords_z[node_b]

                            if abs(node_a_x - node_b_x) > tolerance:
                                continue
                            if abs(node_a_y - node_b_y) > tolerance:
                                continue
                            if abs(node_a_z - node_b_z) > tolerance:
                                continue

                            map_merge_nodes[node_a] = map_merge_nodes[node_b]
                            is_processed = True
                            break

                    if is_processed:
                        break
                if is_processed:
                    break

            if not is_processed:
                map_merge_nodes[node_a] = node_a

        self.map_merge_nodes = map_merge_nodes

        self.logger.info(f'finish merge_nodes()')
        pass

    def node_renumbering(self):
        """
        節点マージの結果を、要素コネクティビティに反映させる。
        """
        self.logger.info(f'start node_renumbering()')
        mesh_data = self.mesh_data
        map_merge_nodes = self.map_merge_nodes
        nodes_df = mesh_data.get_nodes_df()
        elements_df = mesh_data.get_elements_df()
        num_nodes_before = mesh_data.get_num_nodes()

        coords_x_old = nodes_df[COLUMN_X].values
        coords_y_old = nodes_df[COLUMN_Y].values
        coords_z_old = nodes_df[COLUMN_Z].values

        num_merged_nodes = 0
        for i_node in range(num_nodes_before):
            if map_merge_nodes[i_node] == i_node:
                num_merged_nodes += 1

        merged_coords_x = []
        merged_coords_y = []
        merged_coords_z = []

        num_merged_nodes = 0
        for i_node in range(num_nodes_before):
            if i_node > 0 and i_node % LOGGER_INTERVAL == 0:
                self.logger.info(f'make merged_coords : {i_node} / {num_nodes_before}')

            if map_merge_nodes[i_node] == i_node:
                x = coords_x_old[i_node]
                y = coords_y_old[i_node]
                z = coords_z_old[i_node]
                merged_coords_x.append(x)
                merged_coords_y.append(y)
                merged_coords_z.append(z)
                map_merge_nodes[i_node] = num_merged_nodes
                num_merged_nodes += 1
            else:
                map_merge_nodes[i_node] = map_merge_nodes[map_merge_nodes[i_node]]

        elements_df[COLUMN_NODE_0] = elements_df[COLUMN_NODE_0].map(map_merge_nodes)
        elements_df[COLUMN_NODE_1] = elements_df[COLUMN_NODE_1].map(map_merge_nodes)
        elements_df[COLUMN_NODE_2] = elements_df[COLUMN_NODE_2].map(map_merge_nodes)
        elements_df[COLUMN_NODE_3] = elements_df[COLUMN_NODE_3].map(map_merge_nodes)
        elements_df[COLUMN_NODE_4] = elements_df[COLUMN_NODE_4].map(map_merge_nodes)
        elements_df[COLUMN_NODE_5] = elements_df[COLUMN_NODE_5].map(map_merge_nodes)
        elements_df[COLUMN_NODE_6] = elements_df[COLUMN_NODE_6].map(map_merge_nodes)
        elements_df[COLUMN_NODE_7] = elements_df[COLUMN_NODE_7].map(map_merge_nodes)

        merged_node_ids = []
        for i_node in range(num_merged_nodes):
            merged_node_ids.append(i_node + 1)

        merged_nodes_df = pd.DataFrame({
            COLUMN_NODE_ID: merged_node_ids,
            COLUMN_X: merged_coords_x,
            COLUMN_Y: merged_coords_y,
            COLUMN_Z: merged_coords_z
        })
        # self.logger.info(f'merged_nodes_df={merged_nodes_df}')

        # self.logger.info(f'map_merge_nodes={map_merge_nodes}')

        mesh_data.set_merged_nodes(num_merged_nodes, map_merge_nodes, merged_nodes_df)

        self.logger.info(f'finish node_renumbering()')
        pass

