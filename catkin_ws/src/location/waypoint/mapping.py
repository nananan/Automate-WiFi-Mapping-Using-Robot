#!/usr/bin/env python

import imp, os
db_man = imp.load_source('DB_Manager', os.path.dirname(os.path.abspath(__file__))+'/../../cinnamon/src/db.py')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

from operator import itemgetter

class Mapping:
    def __init__(self):
        self.DB_Man = db_man.DB_Manager.getInstance()
        # self.APs = []

    def getAPs(self):
        for i in self.DB_Man.select_APs():
            print(i, self.DB_Man.select_APs()[i])
        return self.DB_Man.select_APs()

    def createMappingAP(self, mac_address):
        maps = {}
        maps_AP = {}
        positions = self.DB_Man.select_Waypoints_AP(mac_address)
        for pos in positions:
            # print(pos)
            if pos[8] not in maps_AP:
                maps_AP[pos[8]] = [pos[9]]
            else:
                maps_AP[pos[8]].append(pos[9])
            key = (pos[1],pos[2],pos[3])
            if key not in maps:
                maps[key] = [pos[9]]
            else:
                maps[key].append(pos[9])
    
    #def mapping(self):
        map_position = {}
        map_min_max_AP = {}
        #signal = 0
        for key, value in maps_AP.items():
            map_min_max_AP[key] = (min(value), max(value))
            # print("MINIMOOOOOOOOOOO",key, max(value))
        for key, value in maps.items():
            signal = 0
            # print(key)
            for i in value:
                signal = signal + int(i)
                # print(signal,i)
            map_position[key] = (signal/len(value))
            #print(map_position[key])
        
        return (map_position, map_min_max_AP)

    # def getMapping(self):
    #     return self.maps

    # def color(self):
    #     list_color = [["red","violet"],["blue","green"],["orange","black"]]
    #     # x,y,c = zip(*np.random.rand(30,3)*90-1)
    #     print(map(itemgetter(0), self.map_position))
    #     cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", list_color[0])
    #     norm = matplotlib.colors.Normalize(vmin=-90, vmax=-20)
    #     for key, value in self.map_position.items():
    #         print(key, value, cmap(norm(value))[:3])
    #         print(norm(value))
        
    #     norm=plt.Normalize(-30,-90)
    #     plt.scatter(map(itemgetter(0), self.map_position),map(itemgetter(1), self.map_position),c=self.map_position.values(), cmap=cmap, norm=norm)
    #     plt.colorbar()
    #     plt.show()
        # x = np.linspace(0, 2*np.pi, 64)
        # y = np.cos(x) 
        # plt.figure()
        # plt.plot(x,y)
        # n =20
        # colors = plt.cm.jet(np.linspace(20,90,n))
        # for i in range(n):
        #     plt.plot(x, i*y, color=colors[i])
        # plt.show()


if __name__ == "__main__":
    mapping = Mapping()
    mapping.getAPs()
    mapping.createMappingAP("ce:c0:79:5e:db:e8")
    # mapping.mapping()
    # mapping.color()
