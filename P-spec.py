# Datastruktur: Ett object sphere som innehåller två matriser
# Brightness - En matris av alla ljusvärden
#Tokens - en matris av alla ljusvärden översatta till tecken.
#X0, Y0 är ljuskällans kordinater, Z0 är ljuskällans beräknade z kordinat
#Res är upplösningen på bollen.


#Algoritm:
#1. r, x0, y0, token_list, upplösning (i både x och y) läses in från en excel fil.
#2. Denna data kontrolleras, framförallt så att diskrimanten >0
#3. En instans av objektet skapas.
#4. I konstruktorn så beräknas z0 utifrån värdena r, x0 och y0
#5. En matris av ljusvärden skapas, antalet punkter bestämms av upplösningen.
#6. Ljusvärdena konverteras en för en till tecken enligt en lista som importerades tidigare.



class Sphere:
    def __init__(self,r,x0,y0,token_list, res):
        pass

    def ray_trace(self, r, res):

        pass

    def calc_z0(self,r,x0,y0):

        pass

    def calc_b(self, r, x, y):
        pass

    def token_translate(self, b_vals):
        pass

    def printTokens(self):
        pass

def read():
    pass


def main():

    #Read radius and light origin (x and y)
    r, x0, y0, token_list, res= read()

    #Calculate sphere
    s = Sphere(r,x0,y0,token_list,res)
    s.printTokens()



if __name__ == '__main__':
    main()