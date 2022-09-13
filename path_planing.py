import numpy as np
from geopy.distance import geodesic
from Linknode import LinkNode
import pandas as pd
from tqdm import tqdm
import time

inf = 1e8

def rdnumpy(txtname):
    f = open(txtname)
    line = f.readlines()
    lines = len(line)  # 行数
    for l in line:
        le = l.strip('\n').split(',')
        columns = len(le)  # 列
 
    A = np.zeros((lines, columns), dtype=float)
    A_row = 0
    for lin in line:
        list = lin.strip('\n').split(',')
        A[A_row:] = list[0:columns]
        A_row += 1
    return A

def calculate_distance(node_A, node_B):
    return geodesic((node_A.position[1],node_A.position[0]), (node_B.position[1],node_B.position[0])).m

def get_min_f(open_list, f_list):
    open_f = []
    for node in open_list:
        open_f.append(f_list[node.idx])
    min_f = min(open_f)
    min_idx = open_f.index(min_f)
    node_idx = open_list[min_idx].idx
    return node_idx

def path_plan(start_node, target_node, node_list, map_matric):
    open_list, close_list = [],[]
    node_num = len(node_list)
    f_list = np.ones(node_num)*inf
    g_list = np.ones(node_num)*inf
    h_list = np.ones(node_num)*inf
    f_list = f_list.tolist()
    g_list = g_list.tolist()
    h_list = h_list.tolist()
    for i in range(node_num):
        if map_matric[start_node.idx][i] !=0:
            g_list[i] = map_matric[start_node.idx][i]
            h_list[i] = calculate_distance(node_list[i], target_node)
            f_list[i] = g_list[i] + h_list[i]
    open_list.append(start_node)
    c_node = start_node
    while target_node not in open_list:
        c_idx = get_min_f(open_list, f_list)
        c_node = node_list[c_idx]
        close_list.append(c_node)
        open_list.remove(c_node)
        for idx in range(node_num):
            if map_matric[c_node.idx][idx] == 0 or node_list[idx] in close_list:
                continue
            if node_list[idx] not in open_list:
                node_list[idx].parent_node(c_node)
                open_list.append(node_list[idx])
                g_list[idx] = g_list[c_node.idx] + map_matric[c_node.idx][idx]
                h_list[idx] = calculate_distance(node_list[idx], target_node)
                f_list[idx] = g_list[idx] + h_list[idx]
            if node_list[idx] in open_list:
                if g_list[c_node.idx] + map_matric[c_node.idx][idx] < g_list[idx]:
                    node_list[idx].parent_node(c_node)
                    g_list[idx] = g_list[c_node.idx] + map_matric[c_node.idx][idx]
                    f_list[idx] = g_list[idx] + h_list[idx]
        if len(open_list) == 0:
            break
    
    back_node = target_node
    path_list = []
    while back_node != start_node:
        path_list.append(back_node.idx)
        back_node = node_list[back_node.parent]
    path_list.append(start_node.idx)
    return list(reversed(path_list)),g_list[target_node.idx]-inf


def main():
    map_matric = rdnumpy(r'路径规划数据\link_matric.txt')
    nodes_df = pd.read_excel(r'路径规划数据\nodes.xlsx')
    node_list = []
    for idx in nodes_df['NodeID']:
    
        position = [float(item) for item in nodes_df['positon'][idx].split()]
        new_node = LinkNode(idx, position)
        node_list.append(new_node)
    station_node = [0,19,36,46,8,11,18,26,30,43]
    station_matric = [[] * len(station_node) for _ in range(len(station_node))]
    start_time = time.time()
    full_path = [0,4,5,6,9]
    full_nodes = []
    full_length = 0
    for i in range(len(full_path) - 1):
        sub_nodes, sub_length = path_plan(node_list[station_node[full_path[i]]], node_list[station_node[full_path[i+1]]], node_list, map_matric)
        full_nodes.extend(sub_nodes[:-1])
        full_length += sub_length
    full_nodes.append(sub_nodes[-1])
    print(full_nodes, full_length)
    # for x in tqdm(range(len(station_node))):
    #     for y in range(len(station_node)):
    #         station_matric[x].append(path_plan(node_list[station_node[x]], node_list[station_node[y]], node_list, map_matric)) 
    # print(station_matric)

main()