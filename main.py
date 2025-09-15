from math import *
from sys import *


class pixel:
    def __init__(self,r,x,y,x0,y0,z0,token_list):
        self.x = x
        self.y = y
        self.b = self.calc_b(r,x0,y0,z0)
        self.token_list = token_list
        self.token = self.token_translate()

    def calc_b(self, r, x0,y0,z0):
        disc = r**2-self.x**2-self.y**2

        if disc < 0:
            b = 0
        else:
            z = sqrt(disc)
            b = (self.x*x0+self.y*y0+z*z0)/r**2

        return b
    def token_translate(self):
        if self.b <= 0:
            token = self.token_list[0]
        elif 0 < self.b <= 0.3:
            token = self.token_list[1]
        elif 0.3 < self.b <= 0.5:
            token = self.token_list[2]
        elif 0.5 < self.b <= 0.7:
            token = self.token_list[3]
        elif 0.7 < self.b <= 0.9:
            token = self.token_list[4]
        elif 0.9 < self.b <= 1:
            token = self.token_list[5]
        else:
            print("Error no matching token found")
            exit()

        return token



def read():
    #Params:
    x_resolution = 100
    y_resolution = 100
    """"#TESTING
    r = float(input("Input sphere radius: "))
    x0 = float(input("Input light origin x cord: "))
    y0 = float(input("Input light origin y cord: "))
    """

    #TESTING
    r = 5
    x0 = 3
    y0 = 2

    token_list = ["M", "*", "+", "-","."," "]

    return r,x0,y0, x_resolution,y_resolution,token_list


def calc_light_vals(r, x0, y0,x_res, y_res,token_list):

    #Calculate z0
    try: z0 = sqrt(r**2-x0**2-y0**2)
    except ValueError:
        print("Error:Light origin outside of target sphere")
        exit()

    pixel_list = []
    for step in range(y_res + 1):
        y = -r + step*(2 * r / float(y_res))
        for step in range(x_res + 1):
            x = -r + step * (2 * r / float(x_res))

            pixel_list.append(pixel(r,x,y,x0,y0,z0,token_list))

    return pixel_list

            #Calculation for given (x,y) pa

def main():

    #Read radius and light origin (x and y)
    r, x0, y0, x_resolution, y_resolution, token_list = read()
    pixel_list = calc_light_vals(r, x0, y0, x_resolution, y_resolution, token_list)

    output_string = ""
    count = 1
    for pixel in pixel_list:
        output_string = output_string + "" + pixel.token
        if count%(x_resolution+1) == 0:
            output_string += ","''
        count+=1

    outputlist = output_string.split(",")
    for x in outputlist:
        print(x)

    return




if __name__ == '__main__':
    main()