from define import Station, Passengers, Bus
import time

def capacity_manage(avail_bus:list, station_set:list, station_dict:dict,node_list, map_matric, k_set, max_route):
    moving_bus = []
    while len(avail_bus) != 0:
        for bus in avail_bus:
            next_station = bus.choose_next_station(station_set, station_dict, node_list, map_matric, k_set)
            station_dict = bus.state_update(station_dict)
            if len(bus.plan_route) > max_route:
                bus.state = 1
                bus.start_time = time.time()
                avail_bus.remove(bus)
                moving_bus.append(bus)
    return moving_bus

def board_simulate(moving_bus:list, station_dict:dict):
    served_psg_count = 0
    for bus in moving_bus:
        bus.psg_list = []
        for idx in range(len(bus.plan_route)):
            station = bus.plan_route[idx]
            for psg in station_dict[station].psg_list:
                if len(bus.psg_list) >= bus.N:
                    break
                if psg.state == 0 and psg.a_station in bus.plan_route[idx+1:]:
                    psg.state = 1
                    psg.board_bus = bus.ID
                    station_dict[station].psg_list.remove(psg)
                    bus.psg_list.append(psg)
                    served_psg_count += 1
            # if len(bus.psg_list) >= bus.N:
            #     break
    #print(served_psg_count)
    return station_dict, served_psg_count