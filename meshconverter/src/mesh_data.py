class MeshData:
    def __init__(self):
        # 節点数
        self.num_nodes = None
        # 節点の座標値を格納したデータフレーム
        self.nodes_df = None
        # 最大座標値
        self.max_coords = None
        # 最小座標値
        self.min_coords = None
        # 同一座標値の節点かどうかを判定する際の閾値
        self.tolerance = None

        # ファイルに書かれていた節点IDから、プログラム内部で使うインデックスへの変換を表した辞書である。
        # この辞書に現れるインデックスは、節点マージ前のインデックスであるため、
        # 節点マージ後での取り扱いには注意が必要である。
        self.dictionary_node_id_to_index = None

        # 要素数
        self.num_elements = None
        # 領域数
        self.num_domains = None
        # 要素コネクティビティのデータフレーム
        self.elements_df = None

        # 節点マージでの節点番号の対応を表す
        self.map_merge_nodes = None
        # 節点マージ前のデータフレームである
        self.nodes_df_old = None
        # 節点マージ前の節点個数である
        self.num_nodes_old = None

        # 要素同士の隣接関係で、要素番号を格納した配列である
        self.neighbor_element = None
        # 要素同士の隣接関係で、隣接要素の側での面番号を格納した配列である
        self.neighbor_face = None
        # 節点ごとに、いくつの要素に属しているかを表した配列である
        self.num_elements_of_node = None
        # 節点ごとの、属している要素の番号の配列である
        self.element_id_of_node = None

        # 要素ごとに設定されたフラグの配列である
        self.element_flag = None

        pass

    # 節点関連のデータをセットする
    def set_nodes(self, num_nodes, nodes_df, max_coords, min_coords, tolerance, dictionary_node_id_to_index):
        self.num_nodes = num_nodes
        self.nodes_df = nodes_df
        self.max_coords = max_coords
        self.min_coords = min_coords
        self.tolerance = tolerance
        self.dictionary_node_id_to_index = dictionary_node_id_to_index
        pass

    # 要素コネクティビティをセットする
    def set_elements(self, num_elements, num_domains, elements_df):
        self.num_elements = num_elements
        self.num_domains = num_domains
        self.elements_df = elements_df
        pass

    # 節点マージの結果をセットする
    def set_merged_nodes(self, num_merge_nodes, map_merge_nodes, nodes_df):
        self.map_merge_nodes = map_merge_nodes
        # マージ前
        self.nodes_df_old = self.nodes_df
        self.num_nodes_old = self.num_nodes
        # マージ後
        self.nodes_df = nodes_df
        self.num_nodes = num_merge_nodes
        pass

    # 要素同士の隣接関係のデータをセットする
    def set_neighbor(self, neighbor_element, neighbor_face, num_elements_of_node, element_id_of_node):
        self.neighbor_element = neighbor_element
        self.neighbor_face = neighbor_face
        self.num_elements_of_node = num_elements_of_node
        self.element_id_of_node = element_id_of_node
        pass

    # getter

    def get_num_nodes(self):
        return self.num_nodes

    def get_num_nodes_old(self):
        return self.num_nodes_old

    def get_num_elements(self):
        return self.num_elements

    def get_num_domains(self):
        return self.num_domains

    def get_nodes_df(self):
        return self.nodes_df

    def get_nodes_df_old(self):
        return self.nodes_df_old

    def get_elements_df(self):
        return self.elements_df

    def get_max_coords(self):
        return self.max_coords

    def get_min_coords(self):
        return self.min_coords

    def get_tolerance(self):
        return self.tolerance

    def get_element_flag(self):
        return self.element_flag

    def get_neighbor_element(self):
        return self.neighbor_element

    def get_neighbor_face(self):
        return self.neighbor_face

    def get_num_elements_of_node(self):
        return self.num_elements_of_node

    def get_element_id_of_node(self):
        return self.element_id_of_node

    def get_map_merge_nodes(self):
        return self.map_merge_nodes

    def get_dictionary_node_id_to_index(self):
        return self.dictionary_node_id_to_index

    def set_element_flag(self, value):
        self.element_flag = value

    def set_elements_df(self, value):
        self.elements_df = value

