from math import *
from sys import *
import pygame
import xlwings as xw

"""class Scenery:
    def __init__(self):
        
"""
class Sphere:
    def __init__(self,r,x0,y0,token_list):
        self.x0 = x0
        self.y0 = y0
        self.z0 = self.calc_z(r, x0, y0)
        self.token_list = token_list
        self.brightness, self.tokens, self.shadow_cords = self.ray_trace(r)

    def ray_trace(self, r):

        b_matrix = []
        t_matrix = []
        shadow_cords = []

        for ry_Step in range (2*r):
            y = -r + ry_Step

            b_row = []
            t_row = []

            for rx_Step in range(2*r):
                x = -r + rx_Step

                #Main Brightness calculation
                b = self.calc_b(r,x,y)
                b_row.append(b)

                #Translate Brightness to token
                t_row.append(self.token_translate(b))

                #Calculate Shadow
                shadow = self.shadow_calc(r,x,y)
                if shadow is not None: shadow_cords.append(shadow)

            b_matrix.append(b_row)
            t_matrix.append(t_row)

        return (b_matrix, t_matrix, shadow_cords)

    def shadow_calc(self, r, x,y):
        disc = r**2-x**2-y**2
        x0 = self.x0
        y0 = self.y0
        z0 = self.z0
        if disc > 0:
            shadow_x = x0 - (z0 * (x-x0)) / 2
            shadow_y = y0 - (z0 * (y - y0)) / 2
            return [shadow_x, shadow_y]


    def calc_z(self,r,x0,y0):

        try:
            z = sqrt(r ** 2 - x0 ** 2 - y0 ** 2)
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

    def token_translate(self, b):
        if b <= 0:
            return(self.token_list[0])
        elif 0 < b <= 0.1:
            return(self.token_list[1])
        elif 0.1 < b <= 0.2:
            return(self.token_list[2])
        elif 0.2 < b <= 0.3:
            return(self.token_list[3])
        elif 0.3 < b <= 0.4:
            return(self.token_list[4])
        elif 0.4 < b <= 0.5:
            return(self.token_list[5])
        elif 0.5 < b <= 0.6:
            return(self.token_list[6])
        elif 0.6 < b <= 0.7:
            return(self.token_list[7])
        elif 0.7 < b <= 0.8:
            return(self.token_list[8])
        elif 0.8 < b <= 0.9:
            return(self.token_list[9])
        elif 0.9 < b <= 1:
            return(self.token_list[10])
        else:
            print("Error no matching token found")
            exit()


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
    token_list= ws.range("B7:B17").value

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
def shadow():


    return

def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()

    #Calculate sphere
    s = Sphere(r,x0,y0,token_list)

    for row in s.tokens:
        printline=""
        for token in row:
            printline += token
        print(printline)




if __name__ == '__main__':
    main()