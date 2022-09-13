from path_planing import path_plan
import time
import math
import numpy as np
import pickle as pkl
import random

def save_dict(save_dict,path = 'D:\运力匹配算法\code\station_dict\station_dict.pkl'):
    with open(path,'wb') as f:
        pkl.dump(save_dict, f)

def read_dict(path = 'D:\运力匹配算法\code\station_dict\station_dict.pkl'):
    with open(path,'rb') as f:
        data = pkl.load(f)
    return data

def travel_simulate(bus, station_dict:dict, time_scale):
    bus.psg_list = []
    bus.state = 1
    served_psg = []
    for idx in range(len(bus.plan_route)-1):
        station = plan_route[idx]
        for psg in bus.psg_list:
            if psg.a_station == station:
                bus.psg_list.remove(psg)
        for psg in station_dict[station].psg_list:
            if psg.board_bus == bus.ID:
                station_dict[station].psg_list.remove(psg)
                bus.psg_list.append(psg)
                served_psg.append(psg)
            if len(bus.psg_list) >=bus.N:
                break
        time.sleep(travel_time(station,plan_route[idx+1])*time_scale)
    station = plan_route[-1]
    for psg in bus.psg_list:
        if psg.a_station == station:
            bus.psg_list.remove(psg)
    bus.state = 0
    bus.psg_sum += len(served_psg)
    return served_psg

def travel_time(start, target, node_list, map_matric):
    start_node = node_list[start.node_idx]
    target_node = node_list[target.node_idx]
    _, travel_distance = path_plan(start_node, target_node, node_list, map_matric)
    velocity = 15
    return travel_distance / velocity


def cal_tpsg(station, target):
    cnt = 0
    for psg in station.psg_list:
        if psg.a_station == target.station_id:
            cnt += 1
    return cnt


def distance_score(start, target,node_list,map_matric,k_d):
    start_node = node_list[start.node_idx]
    target_node = node_list[target.node_idx]
    _, distance = path_plan(start_node, target_node, node_list, map_matric)
    return k_d*distance

def Passenger_score(start, target, k_p):
    return -k_p*target.psg_count

def distrib_score(bus, start, target, k_a):
    # 在计算分数前，先将当前站点加入队列
    t_psg, all_psg = 0,0
    station_dict = read_dict()
    for station_id in bus.plan_route:
        t_psg += cal_tpsg(station_dict[station_id], target)
        all_psg += station_dict[station_id].psg_count
    if all_psg == 0 or t_psg == 0:
        return 0
    a_s = t_psg/all_psg
    return k_a * math.log(a_s)

def waittime_score(target, k_w):
    average_wait_time = sum([(time.time()-psg.b_time) for psg in target.psg_list])/target.psg_count

    return - k_w *average_wait_time

def calculate_score(bus, start, target, node_list,map_matric, k):
    #print(start.station_id, target.station_id,distance_score(start, target, node_list, map_matric, k[0]),Passenger_score(start, target, k[1]),distrib_score(bus, start, target, k[2]),waittime_score(target, k[3]))
    return distance_score(start, target, node_list, map_matric, k[0])+Passenger_score(start, target, k[1])+distrib_score(bus, start, target, k[2])+ waittime_score(target, k[3]) + random.randint(-2000, 2000)

