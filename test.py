def test(situation, all_psg, served_psg):
    print(situation)
    for i in range(5):
        print("time: "+str((i+1)*720)+'s')
        print("当前游客总数:"+str(all_psg[i])+"  已服务游客总数:"+str(served_psg[i]))
    

#
# test('low', [121,239,358,466,575], [114, 230, 342, 449, 551])


print("场景: low")
print('平均运送游客人数: 55.1人/h')
print('游客平均服务时间: 16.3min')
print('平均车辆行驶里程: 1.4km')