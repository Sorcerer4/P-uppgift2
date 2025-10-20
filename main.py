from math import *
from sys import *
import pygame
import xlwings as xw
import numpy as np

class Scenery:
    def __init__(self, r,x0,y0,token_list,res):
        self.display =  np.zeros(res)
        self.res = res
        self.token_list = token_list

        #Create ball
        self.ball_y = res[0] / 2
        self.ball_x = res[1] / 2

        self.b = ball(r,x0,y0)
        self.shadow = self.b.shadow_cords

    def merge(self):
        ball_diameter = self.b.r*2
        start = (self.res[0]-ball_diameter) // 2
        print(start)
        b_image = np.array(self.b.brightness)
        self.display[start:start+ball_diameter,start:start+ball_diameter] = b_image

    def insert_shadow(self):

        for cord in self.shadow:
            x_res, y_res = self.res
            x,y = [int(i) for i in cord]
            print(x,y)
            self.display[int(x+x_res/2)][int(y+y_res/2)] = 10

    def viewscreen(self):
        for row in self.display:
            for value in row:
                print(self.token_translate(value)+ " ",end="")
            print()

    def token_translate(self, b):
        if b <= 0:
            return(self.token_list[0])
        elif 0 < b <= 0.02:
            return(self.token_list[1])
        elif 0.02 < b <= 0.05:
            return(self.token_list[2])
        elif 0.05 < b <= 0.1:
            return(self.token_list[3])
        elif 0.1 < b <= 0.2:
            return(self.token_list[4])
        elif 0.2 < b <= 0.35:
            return(self.token_list[5])
        elif 0.35 < b <= 0.5:
            return(self.token_list[6])
        elif 0.5 < b <= 0.7:
            return(self.token_list[7])
        elif 0.7 < b <= 0.8:
            return(self.token_list[8])
        elif 0.8 < b <= 0.9:
            return(self.token_list[9])
        elif 0.9 < b <= 1:
            return(self.token_list[10])
        elif b == 10:
            return (self.token_list[11])
        else:
            print("Error no matching token found")
            exit()

class ball:
    def __init__(self,r,x0,y0):
        self.r = r
        self.x0 = x0
        self.y0 = y0
        self.z0 = self.calc_z(r, x0, y0)
        self.center = [0, 0, 50]
        self.brightness,self.shadow_cords = self.ray_trace()


    def ray_trace(self):
        r = self.r
        b_matrix = []
        shadow_cords = []

        for ry_Step in range (2*r):
            y = -r + ry_Step

            b_row = []

            for rx_Step in range(2*r):
                x = -r + rx_Step

                #Main Brightness calculation
                b = self.calc_b(r,x,y)
                b_row.append(b)

                #Calculate Shadow
                shadow = self.shadow_calc(r,x,y)
                if shadow is not None: shadow_cords.append(shadow)

            b_matrix.append(b_row)

        return (b_matrix,shadow_cords)

    def shadow_calc(self, r, x,y):
        disc = r**2-x**2-y**2
        x0 = self.x0
        y0 = self.y0
        z0 = self.z0
        if disc > 0:
            z = self.center[2] + self.calc_z(r,x,y)
            if (z != z0):
                t = -z0 / (z-z0)
                shadow_x = x0 + t*(x-x0)
                shadow_y = y0 + t*(y-y0)
                return [shadow_x, shadow_y]



    def calc_z(self,r,x,y):

        try:
            z = sqrt(r ** 2 - x ** 2 - y ** 2)
        except ValueError:
            print("Error:Light origin outside of target sphere")
            exit()
        return z

    def calc_b(self, r, x, y):
        disc = r**2-x**2-y**2

        if disc < 0:
            b = 0
        else:
            z = sqrt(disc)
            b = (x*self.x0+y*self.y0+z*self.z0)/r**2

        return b

class GUI():
    def __init__(self):
        self.surface = pygame.Surface()

def read():
    debugmode = True

    #Read from excel https://www.geeksforgeeks.org/python/working-with-excel-files-in-python-using-xlwings/
    print("reading parameters.xlsx..")
    wb = xw.Book('parameters.xlsx')
    wks = xw.sheets
    ws = wks[0]

    r,x0, y0 = ws.range("B2:B4").value
    res = ws.range("B5:B6").value
    token_list= ws.range("B7:B18").value

    print("Done reading.")

    #Convert values to right forms
    d = dict 
    r = int(r)
    x0 = int(x0)
    y0 = int(y0)
    res = [int(par) for par in res]

    #Checks

    if debugmode: print("Beginning indata checks")
    while True:
        disc = r ** 2 - x0 ** 2 - y0 ** 2
        if disc >= 0:
            if debugmode: print("pass pos_disc")
            break
        else:
            x0, y0 = input("Negativ discriminant, light source outside of range, please enter new values manually (X,Y): ").split()
            x0, y0 = int(x0), int(y0)




    return r,x0,y0,token_list, res

def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()

    #Create scene
    s = Scenery(r,x0,y0,token_list,res)
    s.merge()
    s.insert_shadow()
    s.viewscreen()


if __name__ == '__main__':
    main()