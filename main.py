from importlib import reload
from math import *
from sys import *
import pygame
import xlwings as xw
import numpy as np
from pandas.core.apply import relabel_result


class Scenery:
    def __init__(self, r,x0,y0,token_list,res, windowsize):

        #Imporot settings for ball
        self.r = r
        self.x0 = x0
        self.y0 = y0

        #Import settings for render
        self.token_list = token_list
        self.res = res
        self.windowsize = windowsize

        #Create empty screen
        self.display_values =  np.zeros(res)

    def createball(self,r, x0, y0):
        #Create ball
        self.ball_y = self.res[0] / 2
        self.ball_x = self.res[1] / 2

        self.b = ball(r,x0,y0)
        self.shadow = self.b.shadow_cords

    def merge(self):
        b_image = np.array(self.b.brightness)

        ball_diameter = self.b.r*2
        start_x = (self.res[0] - ball_diameter) // 2
        start_y = (self.res[1] - ball_diameter) // 2

        mask = b_image > 0

        region = self.display_values[start_x:start_x + ball_diameter, start_y:start_y + ball_diameter] # Region for ball to be inserted into
        region[mask] = b_image[mask] #Uses matrix of False/True to replace elements in matrix with resp. to mask
        self.display_values[start_x:start_x + ball_diameter, start_x:start_x + ball_diameter] = region

    def insert_shadow(self):

        for cord in self.shadow:
            x_res, y_res = self.res
            x,y = [int(i) for i in cord]
            self.display_values[int(x + x_res / 2)][int(y + y_res / 2)] = 10

    def render(self,screen,pixel_width,pixel_height):
        clock = pygame.time.Clock()

        screen.fill((0,0,0)) #Fill screen with black background
        x = y = 0

        for row in self.display_values:
            for value in row:
                if value > 0 and value < 10:
                    color = int(255*value) #Interpolation, as value is between 0 and 1.
                elif value == 10:
                    color = 100             #Shadow dark grey pitch
                elif value <= 0:
                    color = 255             #Background Color
                else:
                  print("Unexpeted brightness value during render")

                pygame.draw.rect(screen,(color,color,color), (x,y,pixel_width,pixel_height))
                x += pixel_width

            #Cycle next row
            x = 0
            y += pixel_height

        #Update screen
        pygame.display.flip()
        clock.tick(60)


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

    def mainloop(self):
        r = self.r
        x0 = self.x0
        y0 = self.y0

        width , height = self.windowsize
        pygame.init()
        screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Ray Traced Ball")

        running = True

        while running:
            self.display_values = np.zeros(self.res)

            self.createball(r,x0,y0)
            self.insert_shadow()
            self.merge()

            #Compute render parameters
            ball_diameter = self.b.r * 2
            start_x = (self.res[0] - ball_diameter) // 2
            start_y = (self.res[1] - ball_diameter) // 2
            pixel_width = round(width / self.res[0])
            pixel_height = round(height / self.res[1])

            self.render(screen, pixel_width,pixel_height)

            waiting = True
            while waiting:
                event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    rel_x_pixel = mouse_x-(start_x*pixel_width)
                    rel_y_pixel = mouse_y-(start_y*pixel_height)

                    rel_x = rel_x_pixel/pixel_width - self.r
                    rel_y = rel_y_pixel/pixel_height - self.r

                    pixel_radius = self.r*pixel_width
                    disc =  pixel_radius** 2 - rel_x ** 2 - rel_y ** 2
                    print("mouse disc calc")
                    print(pixel_radius,rel_x,rel_y)
                    if disc > 0:
                        x0 = rel_x
                        y0 = rel_y
                        waiting = False

class ball:
    def __init__(self,r,x0,y0,):
        self.r = r
        self.x0 = x0
        self.y0 = y0
        self.z0 = self.calc_z(r, x0, y0)
        self.center = [0, 0, 2*self.r]
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
            print(f"r: {r},x:{x},y:{y}")
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
    r, x0, y0, token_list, res = read()

    #Create scene
    windowsize = 1000,1000
    s = Scenery(r, x0, y0, token_list, res, windowsize)
    s.mainloop()

if __name__ == '__main__':
    main()