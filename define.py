import numpy as np 
import random 
import time
import math
from utils import calculate_score,travel_time
from path_planing import path_plan

class Station:
    def __init__(self, station_id, psg_list, node_idx):
        self.station_id = station_id
        self.psg_list = psg_list
        self.node_idx = node_idx
        self.psg_count = len(self.psg_list)
    def add_psg(self, psg):
        self.psg_list.append(psg)
        self.psg_count +=1
    def __eq__(self,other):
        return self.station_id == other.station_id

class Passengers:
    def __init__(self, idx,state, b_station, a_station):
        self.idx = idx
        self.state = state 
        self.b_station = b_station
        self.a_station = a_station 
        self.b_time = time.time()
        self.board_bus = None
    def change_state(self, state):
        self.state = state 
    def __eq__(self,other):
        return self.idx == other.idx


class Bus:
    def __init__(self, ID, state, N, psg_list, plan, c_station):
        self.ID = ID 
        self.state = 0
        self.N = 20
        self.psg_list = []
        self.plan_route = plan
        self.plan_route.append(c_station)
        self.c_station = c_station
        self.psg_sum = 0
        self.time_cost = 0
        self.start_time = 0
        self.travel_path = []
        self.time_plan = []
    def __eq__(self,other):
        return self.ID == other.ID

    def choose_next_station(self, station_set:list,station_dict:dict, node_list, map_matric, k_set:list):
        station_score = []
        station_list = station_set.copy()
        for s in self.plan_route:
            station_list.remove(s)
        #防止回头路
        for station in station_list:
            station_score.append(calculate_score(self, station_dict[self.c_station],station_dict[station], node_list, map_matric, k_set))
        min_value = min(station_score) # 求列表最小值
        min_idx = station_score.index(min_value) # 求最小值对应索引
        
        self.plan_route.append(station_list[min_idx])
        self.c_station = station_list[min_idx]
        return station_list[min_idx]

    def state_update(self, station_dict:dict):
        if len(self.plan_route) == 0 or len(self.plan_route) == 1:
            return station_dict
        else:
            c_station = self.plan_route[-2]
            n_station = self.plan_route[-1]
            for psg in self.psg_list:
                if psg.a_station == c_station:
                    self.psg_list.remove(psg)
            max_board = self.N - 2*len(self.plan_route)
            cnt_board = 0
            for station in self.plan_route:
                for psg in station_dict[station].psg_list:
                    if psg.a_station == station:
                        station_dict[station].psg_list.remove(psg)
                        self.psg_list.append(psg)
                        cnt_board +=1
                        if cnt_board >= max_board or len(self.psg_list) > self.N:
                            break
                if cnt_board >= max_board or len(self.psg_list) > self.N:
    
                    break
        return station_dict
    
    def calculate_time(self,station_dict, node_list, map_matric):
        self.time_cost = 0
        self.time_plan = [0]
        for idx in range(len(self.plan_route)-1):
            c_station = self.plan_route[idx]
            n_station = self.plan_route[idx+1]
            time_gap = travel_time(station_dict[c_station], station_dict[n_station], node_list, map_matric)
            self.time_cost += time_gap
            self.time_plan.append(time_gap)
        return self.time_cost

    def get_path(self, station_dict, node_list, map_matric):
        self.travel_path = []
        self.time_plan = []
        for idx in range(len(self.plan_route)-1):
            c_station = self.plan_route[idx]
            n_station = self.plan_route[idx+1]
            node_path = path_plan(station_dict[c_station], station_dict[n_station], node_list, map_matric)
            self.travel_path.extend(node_path)
        return self.travel_path
        
            






