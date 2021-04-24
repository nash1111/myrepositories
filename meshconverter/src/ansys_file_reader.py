import math

import pandas as pd

from constants import *


class AnsysFileReader:
    """[summary]
    """

    def __init__(self):
        logging.basicConfig(level=LOGGER_LEVEL, format=LOGGER_FORMAT)
        self.logger = logging.getLogger(__name__)

        pass

    def read(self, file_path, mesh_data):
        """
        ファイルの読み込みを行う関数である。
        外部からは、この関数を呼び出す。
        """
        self.logger.info(f'read file : {file_path}')

        # ファイルを1度読み込んで、データブロックの最初と最後の行番号を取得する
        result_get_line_numbers = self.get_line_numbers_of_start_and_end(file_path)
        # 節点座標値ブロックの最初と最後の行番号
        start_end_of_nodes = result_get_line_numbers[0]
        # 要素コネクティビティブロックの最初と最後の行番号
        start_end_of_elements = result_get_line_numbers[1]
        domain_id_of_elements = result_get_line_numbers[2]

        # 節点データを読み込み、データフレームとして返す
        nodes_df = self.read_nodes(file_path, start_end_of_nodes)
        # 要素コネクティビティを読み込み、データフレームとして返す
        elements_df = self.read_elements(file_path, start_end_of_elements, domain_id_of_elements)
        # self.logger.info(f'nodes_df={nodes_df}')
        # self.logger.info(f'elements_df={elements_df}')
        if nodes_df is None or elements_df is None:
            # 読み込みに失敗したらプログラムを終了する
            if nodes_df is None:
                self.logger.warning(f'failed to get nodes')
            if elements_df is None:
                self.logger.warning(f'failed to get elements')

            return False

        # 節点数
        num_nodes = len(nodes_df[COLUMN_NODE_ID])
        # 要素数
        num_elements = elements_df.shape[0]
        # 領域数
        num_domains = len(start_end_of_elements)
        # 最小座標
        min_coords = (min(nodes_df[COLUMN_X]), min(nodes_df[COLUMN_Y]), min(nodes_df[COLUMN_Z]))
        # 最大座標
        max_coords = (max(nodes_df[COLUMN_X]), max(nodes_df[COLUMN_Y]), max(nodes_df[COLUMN_Z]))
        self.logger.info(f'num_nodes={num_nodes}')
        self.logger.info(f'num_elements={num_elements}')
        self.logger.info(f'num_domains={num_domains}')
        self.logger.info(f'min_coords={min_coords}')
        self.logger.info(f'max_coords={max_coords}')

        """
        入力ファイルにかかれた節点IDから、プログラム内部で扱う節点のインデックスへ変換する辞書を作成する。
        入力ファイルで、節点IDが連番ではなく空きがある場合でも対応できるようにしている。
        """
        dictionary_node_id_to_index = {}
        for i in range(num_nodes):
            dictionary_node_id_to_index[nodes_df[COLUMN_NODE_ID][i]] = i
        # self.logger.info(f'dictionary_node_id_to_index={dictionary_node_id_to_index}')

        """
        要素コネクティビティで使われる節点番号について、
        入力ファイルでの値から、プログラム内部で使う節点インデックスへ変換する。
        処理の高速化のために、データフレームのmap()を使用している。
        """
        elements_df[COLUMN_NODE_0] = elements_df[COLUMN_NODE_0].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_1] = elements_df[COLUMN_NODE_1].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_2] = elements_df[COLUMN_NODE_2].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_3] = elements_df[COLUMN_NODE_3].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_4] = elements_df[COLUMN_NODE_4].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_5] = elements_df[COLUMN_NODE_5].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_6] = elements_df[COLUMN_NODE_6].map(dictionary_node_id_to_index)
        elements_df[COLUMN_NODE_7] = elements_df[COLUMN_NODE_7].map(dictionary_node_id_to_index)
        # print(f'map_df={elements_df}')

        # 座標値を比較して、同じ節点であるかを判定する際に使用する許容誤差を計算する
        x_length = max_coords[0] - min_coords[0]
        y_length = max_coords[1] - min_coords[1]
        z_length = max_coords[2] - min_coords[2]
        # bounding boxの対角線の長さ
        box_length = math.sqrt(x_length * x_length + y_length * y_length + z_length * z_length)
        # 判定に使用する許容誤差
        tolerance = box_length * TOLERANCE_RATE
        self.logger.info(f'x_length={x_length}')
        self.logger.info(f'y_length={y_length}')
        self.logger.info(f'z_length={z_length}')
        self.logger.info(f'box_length={box_length}')
        self.logger.info(f'tolerance={tolerance}')

        # 節点データをセットする
        mesh_data.set_nodes(num_nodes, nodes_df, max_coords, min_coords, tolerance, dictionary_node_id_to_index)
        # 要素データをセットする
        mesh_data.set_elements(num_elements, num_domains, elements_df)

        return True

    def get_line_numbers_of_start_and_end(self, file_path):
        """
        データブロックの最初と最後の行番号を抽出する。
        節点座標値のブロックは、start_end_of_nodes[0]が最初の行、start_end_of_nodes[1]が最後の行を表す。
        要素ブロックは複数存在することがある。
        i番目の要素ブロックについては、
        start_end_of_elements[i][0]が最初の行、start_end_of_elements[i][1]が最後の行、
        domain_id_of_elements[i]が領域番号を表す。
        Returns:
            start_end_of_nodes:節点ブロックの最初と最後の行番号のペア
            start_end_of_elements:要素ブロックの最初と最後の行番号のペアのリスト
            domain_id_of_elements:要素ブロックごとの領域番号
        """

        # line numbers of start and end of node block
        start_end_of_nodes = []

        # line numbers of start and end of element block of each domains
        start_end_of_elements = []
        domain_id_of_elements = []

        # read file contents
        raw_ansys_file = open(file_path, mode='r', encoding="shift-jis")
        line_list = raw_ansys_file.readlines()

        node_start = -1
        node_end = -1
        element_start = -1
        element_end = -1
        domain_id = -1
        line_number_domain_id = -1
        line_counter = 0
        for line in line_list:
            if 'Nodes for the whole assembly' in line:
                # start of node block
                # skip first 3 lines
                node_start = line_counter + 3
            elif 'Elements for Body' in line:
                # start of element block
                # skip first 4 lines
                element_start = line_counter + 4
                line_number_domain_id = line_counter + 1
            elif line_counter == line_number_domain_id:
                # get domain id
                line_split = line.split(',')
                if len(line_split) >= 2:
                    domain_id = int(line_split[1].strip())
                    self.logger.info(f'domain_id={domain_id} :line_number={line_counter}, line={line}')
                else:
                    self.logger.warning(f'failed to get domain ID :line_number={line_counter}, line={line}')
            elif line.startswith(ANSYS_END_OF_BLOCK):
                # end of node or element block
                if node_start != -1:
                    # previous line is last of node block
                    node_end = line_counter - 1
                    start_end_of_nodes = [node_start, node_end]
                    node_start = -1
                    node_end = -1
                elif element_start != -1:
                    # previous line is last of element block
                    element_end = line_counter - 1
                    start_end_of_elements.append([element_start, element_end])
                    domain_id_of_elements.append(domain_id)
                    element_start = -1
                    element_end = -1
                    domain_id = -1
                    line_number_domain_id = -1
            else:
                pass

            line_counter = line_counter + 1

            pass

        # close file
        raw_ansys_file.close()

        self.logger.info(f'start_end_of_nodes={start_end_of_nodes}')
        self.logger.info(f'start_end_of_elements={start_end_of_elements}')
        self.logger.info(f'domain_id_of_elements={domain_id_of_elements}')

        return start_end_of_nodes, start_end_of_elements, domain_id_of_elements

    def read_nodes(self, file_path, start_end_of_nodes):
        """
        節点データを読み込み、データフレームを作成する。
        pandasのread_csv()関数を使用する。
        """
        node_start = start_end_of_nodes[0]
        node_end = start_end_of_nodes[1]
        if node_start < 0 or node_start > node_end:
            self.logger.warning(f'error : node block : start={node_start}, end={node_end}')
            return None

        # read_csv()で、ファイル先頭からスキップする行数
        num_lines_to_skip = node_start
        # csvデータとして読み込む行数
        num_lines_to_read = node_end - node_start + 1

        # read_csv()により、ファイルから読み込んだ結果をデータフレームとして取得する。
        # データフレームの列名は、定数として定義してあるNODES_COLUMNSを使用する
        nodes_df = pd.read_csv(file_path, \
                              skiprows = num_lines_to_skip, \
                              nrows = num_lines_to_read, \
                              encoding = 'shift-jis', \
                              delim_whitespace = True, \
                              names = NODES_COLUMNS \
                              )
        return nodes_df

    def read_elements(self, file_path, start_end_of_elements, domain_id_of_elements):
        """
        要素コネクティビティデータを読み込み、データフレームを作成する。
        """
        elements_df = None
        for i in range(len(start_end_of_elements)):
            """
            要素コネクティビティのブロックごとに読み込み、
            結果を1つのデータフレームに結合していく。
            """
            start_end_of_elements_current = start_end_of_elements[i]
            domain_id = domain_id_of_elements[i]
            elements_df_of_single_domain = \
                self.read_elements_of_single_domain(file_path, start_end_of_elements_current, domain_id)
            if elements_df_of_single_domain is None:
                return None

            if elements_df is None:
                # 最初のブロックの場合は、データフレームをそのまま代入する。
                elements_df = elements_df_of_single_domain
            else:
                # すでにデータフレームが存在する場合は、データフレームの末尾に追加する
                # self.logger.info(f'### 1 elements_df={elements_df}')
                # self.logger.info(f'### 2 elements_df_of_single_domain={elements_df_of_single_domain}')
                elements_df = elements_df.append(elements_df_of_single_domain, ignore_index=True)

        return elements_df

    def read_elements_of_single_domain(self, file_path, start_end_of_elements, domain_id):
        """
        1つの要素コネクティビティブロックを読み込み、データフレームを作成する。
        pandasのread_csv()関数を使用する。
        """
        element_start = start_end_of_elements[0]
        element_end = start_end_of_elements[1]
        if element_start < 0 or element_start > element_end:
            self.logger.warning(f'error : element block : start={element_start}, end={element_end}')
            return None

        # read_csv()で、ファイル先頭からスキップする行数
        num_lines_to_skip = element_start
        # csvデータとして読み込む行数
        num_lines_to_read = element_end - element_start + 1

        # read_csv()で使用する、データフレームの列名である。
        # 以降の処理に不要なデータは、ダミーの列名を与えておく。
        columns_names_for_csv = [
            'dummy1', 'dummy2', 'dummy3', 'dummy4', 'dummy5', 'dummy6', 'dummy7', 'dummy8', \
            COLUMN_ELEMENT_TYPE, \
            'dummy9', \
            COLUMN_ELEMENT_ID, \
            COLUMN_NODE_0, COLUMN_NODE_1, COLUMN_NODE_2, COLUMN_NODE_3, \
            COLUMN_NODE_4, COLUMN_NODE_5, COLUMN_NODE_6, COLUMN_NODE_7 \
            ]
        pd.set_option('display.max_columns', 100)
        elements_df_raw = pd.read_csv(file_path, \
                              skiprows = num_lines_to_skip, \
                              nrows = num_lines_to_read, \
                              encoding = 'shift-jis', \
                              delim_whitespace = True, \
                              names = columns_names_for_csv \
                              )

        # このブロックの要素数
        num_elements_current = len(elements_df_raw[COLUMN_ELEMENT_ID])
        # このブロックの要素での領域番号の配列
        list_domain_id = [domain_id] * num_elements_current

        # read_csv()で返されたelements_df_rawから、処理に使う部分だけを取り出す。
        # また、ファイル形式の違いに対応するため、node2とnode3、node6とnode7を入れ替える。
        elements_df = pd.DataFrame({
            COLUMN_ELEMENT_ID: elements_df_raw[COLUMN_ELEMENT_ID],
            COLUMN_DOMAIN_ID: list_domain_id,
            COLUMN_NODE_0: elements_df_raw[COLUMN_NODE_0],
            COLUMN_NODE_1: elements_df_raw[COLUMN_NODE_1],
            COLUMN_NODE_2: elements_df_raw[COLUMN_NODE_3],
            COLUMN_NODE_3: elements_df_raw[COLUMN_NODE_2],
            COLUMN_NODE_4: elements_df_raw[COLUMN_NODE_4],
            COLUMN_NODE_5: elements_df_raw[COLUMN_NODE_5],
            COLUMN_NODE_6: elements_df_raw[COLUMN_NODE_7],
            COLUMN_NODE_7: elements_df_raw[COLUMN_NODE_6]
        })

        return elements_df
