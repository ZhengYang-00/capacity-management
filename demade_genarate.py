import numpy as np 
import random 
import time


from define import Station, Passengers, Bus
from utils import save_dict, read_dict

def around(num):
    return num# + np.random.normal(scale= num/5, size=1)

def get_time_step(start_id, time_scale):
    station_count = 10
    if start_id < 200*station_count:
        time_step = 1200/200/station_count
        time_step = time_step*time_scale
    else:
        time_step = 2400/100/station_count
        time_step = time_step*time_scale
    return time_step



def update(situation, circle, dict_path, start_id, time_scale = 1):
    # 分别定义为 high,urgent or average,center or average, low
    circle = circle*time_scale
    station_dict = read_dict(dict_path)
    station_count = len(station_dict.keys())
    station_list = list(station_dict.keys())
    start_time = time.time()

    if situation == 'low':
        time_step = 3600/60/station_count
        time_step = time_step*time_scale

        # start_id = 0
        while True:
            if time.time() - start_time > circle:
                save_dict(station_dict, dict_path)
                return station_dict, start_id
            station_set = random.sample(station_list, 2)
            t_psg = Passengers(idx=start_id, state = 0, b_station= station_set[0], a_station= station_set[1])
            idx = station_set[0]
            station_dict[idx].add_psg(t_psg)
            start_id += 1
            time.sleep(around(time_step))
    
    elif situation.split('_')[0] == 'high':
        if situation.split('_')[1] == 'average':
            time_step = 3600/300/station_count
            time_step = time_step*time_scale
            # start_id = 0
            if situation.split('_')[2] == 'average':
                while True:
                    if time.time() - start_time > circle:
                        
                        save_dict(station_dict, dict_path)
                        return station_dict, start_id
                    station_set = random.sample(station_list, 2)
                    t_psg = Passengers(idx=start_id, state = 0, b_station= station_set[0], a_station= station_set[1])
                    idx = station_set[0]
                    station_dict[idx].add_psg(t_psg)
                    start_id += 1
                    time.sleep(around(time_step))

            if situation.split('_')[2] == 'center':
                center_station = random.choice(station_list)
                while True:
                    if time.time() - start_time > circle:
                        save_dict(station_dict, dict_path)
                        return station_dict, start_id
                    b_station = random.choice(station_list)
                    if b_station != center_station:
                        if random.random() < 0.67:
                            a_station = center_station
                        else:
                            station_list.remove(b_station)
                            a_station = random.choice(station_list)
                            station_list.append(b_station)
                        t_psg = Passengers(idx=start_id, state = 0, b_station= b_station, a_station= a_station)
                        station_dict[b_station].add_psg(t_psg)
                    else:
                        station_list.remove(b_station)
                        a_station = random.choice(station_list)
                        station_list.append(b_station)
                        t_psg = Passengers(idx=start_id, state = 0, b_station= b_station, a_station= a_station)
                        station_dict[b_station].add_psg(t_psg)
                    start_id += 1
                    time.sleep(around(time_step))

        if situation.split('_')[1] == 'urgent':
            # start_id = 0
            if situation.split('_')[2] == 'average':
                while True:
                    if time.time() - start_time > circle:
                        save_dict(station_dict, dict_path)
                        return station_dict, start_id
                    time_step = get_time_step(start_id, time_scale)
                    station_set = random.sample(station_list, 2)
                    t_psg = Passengers(idx=start_id, state = 0, b_station= station_set[0], a_station= station_set[1])
                    station_dict[station_set[0]].add_psg(t_psg)
                    start_id += 1
                    time.sleep(around(time_step))

            if situation.split('_')[2] == 'center':
                center_station = random.choice(station_list)
                while True:
                    if time.time() - start_time > circle:
                        save_dict(station_dict, dict_path)
                        return station_dict, start_id
                    time_step = get_time_step(start_id, time_scale)
                    b_station = random.choice(station_list)
                    if b_station != center_station:
                        if random.random() < 0.67:
                            a_station = center_station
                        else:
                            station_list.remove(b_station)
                            a_station = random.choice(station_list)
                            station_list.append(b_station)
                        t_psg = Passengers(idx=start_id, state = 0, b_station= b_station, a_station= a_station)
                        station_dict[b_station].add_psg(t_psg)
                    else:
                        station_list.remove(b_station)
                        a_station = random.choice(station_list)
                        station_list.append(b_station)
                        t_psg = Passengers(idx=start_id, state = 0, b_station= b_station, a_station= a_station)
                        station_dict[b_station].add_psg(t_psg)
                    start_id += 1
                    time.sleep(around(time_step))

def test(situation, distrib_list, target_list):
    print('场景',situation)
    for i in range(10):
        print("站点"+str(i)+"当前乘客数:"+str(distrib_list[i])+"  以站点"+str(i)+"为目的地的当前乘客数:"+str(target_list[i]))
        #print()

#test('high_average_average', [289,315,305,294,298,308,310,291,311,302], [312,300,302,294,290,301,288,292,295,303])