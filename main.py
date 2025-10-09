import tkinter
from math import *
from sys import *
from tkinter import *
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
                elif 0 < b <= 0.1:
                    t_row.append(self.token_list[1])
                elif 0.1 < b <= 0.2:
                    t_row.append(self.token_list[2])
                elif 0.2 < b <= 0.3:
                    t_row.append(self.token_list[3])
                elif 0.3 < b <= 0.4:
                    t_row.append(self.token_list[4])
                elif 0.4 < b <= 0.5:
                    t_row.append(self.token_list[5])
                elif 0.5 < b <= 0.6:
                    t_row.append(self.token_list[6])
                elif 0.6 < b <= 0.7:
                    t_row.append(self.token_list[7])
                elif 0.7 < b <= 0.8:
                    t_row.append(self.token_list[8])
                elif 0.8 < b <= 0.9:
                    t_row.append(self.token_list[9])
                elif 0.9 < b <= 1:
                    t_row.append(self.token_list[10])
                else:
                    print("Error no matching token found")
                    exit()

            t_matrix.append(t_row)
        return t_matrix

class GUI(Tk, Sphere):
    def __init__(self):
        super().__init__()
        self.title("Ray Traced Ball")
        self.geometry("600x400")

        self.print_string = StringVar()

        self.label = Label(self, text=self.print_string, font= "Arial 17 bold")
        self.label.pack(pady=20)

        self.print_string.set("New text!")
        self.update()

        self.mainloop()

    def display_update(self, Sphere):

        output = ''
        for rad in Sphere.tokens:
            output += ''.join(rad)

        print(output)
        self.print_string.set(output)
        self.update()

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
            x0, y0 = input("Negativ discriminant, light source outside of range, please enter new values manually (X,Y): ")



    return r,x0,y0,token_list, res


def GUIloop(event):
    print("Cords: " + str(event.x)+ " , " + str(event.y))
    x = event.x
    y = event.y



def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()

    #Calculate sphere
    s = Sphere(r,x0,y0,token_list,res)

    """for row in s.tokens:
        for x in row:
            print(" "+ (x), end='')
        print("\n")"""

    app = Tk()
    #app.attributes('-fullscreen', True)
    app.geometry("1200x1000")
    app.title("RayTracedBall")

    T = Text(app, height=900, width=1000)
    output = ''
    for rad in s.tokens:
        output += ''.join(rad)
        output+="\n"

    fact = """Hej"""
    T.pack()
    T.insert(tkinter.END, output)

    app.bind("<ButtonRelease>",GUIloop)
    app.mainloop()


if __name__ == '__main__':
    main()