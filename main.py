import numpy as np
import pandas as pd
from define import Passengers, Station, Bus
from Linknode import LinkNode
from demade_genarate import update 
from capacity_manage import capacity_manage, board_simulate
from path_planing import path_plan, rdnumpy
from utils import travel_time, save_dict, read_dict
import time
import random


def init_station(node_list):
    station_dict = {}
    station_node = [0,19,36,46,8,11,18,26,30,43]
    for idx in range(len(station_node)):
        new_station = Station(station_id=idx, psg_list = [], node_idx = station_node[idx])
        station_dict[idx] = new_station
    save_dict(station_dict)
    return station_dict

def init_bus():
    bus_list = []
    for idx in range(30):
        new_bus = Bus(ID = idx, state = 0, N = 30, psg_list = [], plan = [], c_station = 0)
        bus_list.append(new_bus)
    
    return bus_list
        

def main():
    #read road_link
    map_matric = rdnumpy(r'路径规划数据\link_matric.txt')
    # read map_nodes
    nodes_df = pd.read_excel(r'路径规划数据\nodes.xlsx')
    node_list = []
    for idx in nodes_df['NodeID']:
    
        position = [float(item) for item in nodes_df['positon'][idx].split()]
        new_node = LinkNode(idx, position)
        node_list.append(new_node)
    
    bus_list = init_bus()
    avail_bus = bus_list
    moving_bus = []
    station_dict = init_station(node_list)
    start_time = time.time()
    situation = 'low'
    circle = 720
    time_scale = 1/100
    #时间尺度不宜过小，否则程序计算消耗时间会影响需求生成
    pkl_path = 'D:\运力匹配算法\code\station_dict\station_dict.pkl'
    start_id = 0
    station_dict,start_id = update(situation = situation, circle = circle, dict_path = pkl_path,start_id = start_id,time_scale= time_scale)
    station_set = list(station_dict.keys())
    k_set = [1,200,800,300]
    k_none = [1,200,800,300]
    served_psg_count = 0
    while True:
        print('当前乘客总数',start_id)
        moving_bus.extend(capacity_manage(avail_bus, station_set, station_dict,node_list, map_matric, k_set = k_set, max_route = 5))
        station_dict, psg_count = board_simulate(moving_bus, station_dict)
        served_psg_count += psg_count
        print('已服务乘客总数',served_psg_count)
        save_dict(station_dict)
        station_dict,start_id = update(situation = situation, circle = circle, dict_path = pkl_path,start_id = start_id,time_scale= time_scale)
        # print(len(moving_bus))
        
        for bus in moving_bus:
            # print(bus.calculate_time(station_dict, node_list, map_matric))
            # print((time.time() - bus.start_time)/time_scale)
            #print(bus.ID, bus.plan_route)
            if (time.time() - bus.start_time)/time_scale > bus.calculate_time(station_dict, node_list, map_matric):
                bus.state = 0
                bus.plan_route = []       
                moving_bus.remove(bus)
                avail_bus.append(bus)
                
        
        #start_time = time.time()

        
    
main()