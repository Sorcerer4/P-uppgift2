from math import *
from sys import *
import xlwings as xw

class Sphere:
    def __init__(self,r,x0,y0,token_list, res):
        self.x0 = x0
        self.y0 = y0
        self.z0 = self.calc_z0(r, x0,y0)
        self.token_list = token_list
        self.brightness = self.ray_trace(r, res)
        self.tokens = self.token_translate(self.brightness)

    def ray_trace(self, r, res):

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
    debugmode = True

    #Read from excel https://www.geeksforgeeks.org/python/working-with-excel-files-in-python-using-xlwings/
    print("reading parameters.xlsx..")
    wb = xw.Book('parameters.xlsx')
    wks = xw.sheets
    ws = wks[0]

    r,x0, y0 = ws.range("B2:B4").value
    res = ws.range("B5:B6").value
    token_list= ws.range("B7:B12").value

    print("Done reading.")
    #Checks

    if debugmode: print("Beginning indata checks")
    while True:
        disc = r ** 2 - x0 ** 2 - y0 ** 2
        if disc >= 0:
            if debugmode: print("pass pos_disc")
            break
        else:
            x0, y0 = input("Negativ discriminant, light source outside of range, please enter new values manually (X,Y): ")

    #Convert values to right forms after passing all tests
    r = int(r)
    x0 = int(x0)
    y0 = int(y0)
    res = [int(par) for par in res]

    return r,x0,y0,token_list, res

def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()
    s = Sphere(r,x0,y0,token_list,res)

    for row in s.tokens:
        for element in row:
            print(element, end=" ")
        print("\r")

if __name__ == '__main__':
    main()