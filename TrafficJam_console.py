import os

def main():
    
    puzzle = 'puzzles/' + raw_input('What puzzle do you want to solve? (Level: 1-8)') + '.txt'
    mytable = reedpuzzle(puzzle)
    signs = mytable.signs()
    carstring = mytable.carsring()
	
    while signs['R'].x != (mytable.size - 2):
        os.system('cls' if os.name=='nt' else 'clear')
        mytable.printtable()
        print
        m = raw_input('What is your next move? (format: car('+ carstring +') dir(f/b) steps) ').split()
        if mytable.isvalidmove(signs[m[0]], m[1], int(m[2])):
             signs[m[0]].Move(m[1],int(m[2]))
##        else:
##             print
##             print("Invalid move!")
    else:
        os.system('cls' if os.name=='nt' else 'clear')
        mytable.printtable()
        print
        print "You win!"

def reedpuzzle(puzzle):
    cars = []
    with open(puzzle, "r") as puzzle:
        for sor in puzzle:
             c = sor.split()
             cars.append(Car(int(c[0]), int(c[1]), c[2], int(c[3]), c[4]))
    return Table(cars)

class Car(object):
    
    def __init__(self, x, y, lie, length, sign):
        """
        Stores the position datas of the car.

        (x,y): gives the position of upper left side of the car, in Descartes coordinate system.
               positive direct: x:right y:down        
        direction: gives ,whether the car lie horizontally or vertically
        """
        self.x = x
        self.y = y
        self.lie = lie
        self.len = length
        self.sign = sign

    def Move(self, direction, steps):
        operator = {'f': 1 , 'b': -1}
        if self.lie == 'h':
            self.x += (operator[direction]*steps)
        elif self.lie == 'v':
            self.y += (operator[direction]*steps)

    def GetCoordinates(self):
        if self.lie == 'v':
            return[(self.x,self.y + i) for i in range(self.len)]
        elif self.lie == 'h':
            return[(self.x + i,self.y) for i in range(self.len)]

    def GetCoordinatesDict(self):
        return dict(map(lambda t:(t,self.sign),self.GetCoordinates()))

class Table(object):
    
        def __init__(self, cars, size = 6):
             self.size = size
             self.cars = cars

        def carsring(self):
             return ','.join([c.sign for c in self.cars])

        def signs(self):
             return dict([(c.sign,c) for c in self.cars])

        def GetCoordinates(self):
             d = {}
             for c in self.cars:
                 d.update(c.GetCoordinatesDict())
             return d

        def printtable(self):
             carcoordinates = self.GetCoordinates()   
             for j in range(self.size):
                 for i in range(self.size):
                     if (i,j) in carcoordinates:
                         print(carcoordinates[(i,j)]),
                     else:
                         print('+'),
                 print

        def isvalidmove(self, c, direction, steps):
             carcoordinates = self.GetCoordinates()  
             movingcoord = {'h': c.x , 'v': c.y}

             startpos = {'f': movingcoord[c.lie] + c.len , 'b': movingcoord[c.lie] - 1}
             endpos = {'f': movingcoord[c.lie] + c.len + steps , 'b':  movingcoord[c.lie] - steps - 1}
             rangesteps = {'f': 1 , 'b': -1}

             route = range(startpos[direction] , endpos[direction] , rangesteps[direction])
             if c.lie == 'h':
                  freecoordinates = map(lambda i:(i,c.y) not in carcoordinates, route)
             elif c.lie == 'v':
                  freecoordinates = map(lambda i:(c.x,i) not in carcoordinates, route)
             freecoordinates.append(True)
             return reduce(lambda a, b: a and b , freecoordinates) and endpos[direction] <= self.size and endpos[direction] + 1 >= 0

if __name__=="__main__":
    main()



