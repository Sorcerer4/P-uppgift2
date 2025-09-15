from math import *
from sys import *

class sphere:
    def __init__(self,r,x0,y0,token_list, res):
        self.x0 = x0
        self.y0 = y0
        self.z0 = self.calc_z0(r, x0,y0)
        self.token_list = token_list
        self.brightness = self.rayTrace(r,res)
        self.tokens = self.token_translate(self.brightness)

    def rayTrace(self, r, res):

        x_res, y_res = res
        b_matrix = []

        for y_pixel in range(y_res + 1):
            y = -r + y_pixel * (2*r / float(y_res))
            row = []

            for x_pixel in range(x_res + 1):
                x = -r + x_pixel * (2*r / float(x_res))

                #Main Brightness calculation
                b = self.calc_b(r,x,y)

                row.append(b)
            b_matrix.append(row)

        return b_matrix

    def calc_z0(self,r,x0,y0):

        try:
            z0 = sqrt(r ** 2 - x0 ** 2 - y0 ** 2)
        except ValueError:
            print("Error:Light origin outside of target sphere")
            exit()
        return z0

    def calc_b(self, r, x, y):
        disc = r**2-x**2-y**2

        if disc < 0:
            b = 0
        else:
            z = sqrt(disc)
            b = (x*self.x0+y*self.y0+z*self.z0)/r**2

        return b

    def token_translate(self, b_vals):
        print(numpy.shape(b_vals))
        count = 0
        t_matrix = []
        for b_row in b_vals:
            t_row = []
            for b in b_row:
                if b <= 0:
                    t_row.append(self.token_list[0])
                elif 0 < b <= 0.3:
                    t_row.append(self.token_list[1])
                elif 0.3 < b <= 0.5:
                    t_row.append(self.token_list[2])
                elif 0.5 < b <= 0.7:
                    t_row.append(self.token_list[3])
                elif 0.7 < b <= 0.9:
                    t_row.append(self.token_list[4])
                elif 0.9 < b <= 1:
                    t_row.append(self.token_list[5])
                else:
                    print("Error no matching token found")
                    exit()

            t_matrix.append(t_row)
        return t_matrix



def read():
    #Params:
    res =  [60, 60]
    """"#TESTING
    r = float(input("Input sphere radius: "))
    x0 = float(input("Input light origin x cord: "))
    y0 = float(input("Input light origin y cord: "))
    """

    #TESTING
    r = 4
    x0 = 1
    y0 = 0

    token_list = ["M", "*", "+", "-","."," "]

    return r,x0,y0,token_list, res





    return

            #Calculation for given (x,y) pa
def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()
    s = sphere(r,x0,y0,token_list,res)

    for y in s.tokens:
        print(y)


"""
    output_string = ""
    count = 1
    for pixel in pixel_list:
        output_string = output_string + " " + pixel.token
        if count%(x_resolution+1) == 0:
            output_string += ","''
        count+=1

    outputlist = output_string.split(",")
    for x in outputlist:
        print(x)
"""


if __name__ == '__main__':
    main()