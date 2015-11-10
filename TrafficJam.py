from car import Car
import os

def maketable(carcoordinates):
     for i in range(6):
         for j in range(6):
             if (j,i) in carcoordinates:
                 print(carcoordinates[(j,i)]),
             else:
                 print('+'),
         print

def carcoordinates(cars):
     d = {}
     for c in cars:
         d.update(c.GetCoordinatesDict())
     return d

def validmove(carcoordinates, c, direction, steps):
     if c.lie == 'H':
          if direction == 'F' or direction == 'f':
               return reduce(lambda a, b: a and b, map(lambda i:(i,c.y) not in carcoordinates, range(c.x + c.len,c.x + c.len + steps))) and c.x + c.len + steps <= 6
          if direction == 'B' or direction == 'b':
               return reduce(lambda a, b: a and b, map(lambda i:(i,c.y) not in carcoordinates, range(c.x - steps, c.x))) and c.x - steps >= 0
     if c.lie == 'V':
          if direction == 'F' or direction == 'f':
               return reduce(lambda a, b: a and b, map(lambda i:(c.x,i) not in carcoordinates, range(c.y + c.len,c.y + c.len + steps))) and c.y + c.len + steps <= 6
          if direction == 'B' or direction == 'b':
               return reduce(lambda a, b: a and b, map(lambda i:(c.x,i) not in carcoordinates, range(c.y - steps, c.y))) and c.y - steps >= 0


A = Car(4,2,'V',2,'A')
R = Car(0,2,'H',2,'R')
cars = [A,R]
carstring = ','.join([c.sign for c in cars])
signs = dict([(c.sign,c) for c in cars])
while R.x != 4:
    os.system('cls' if os.name=='nt' else 'clear')
    d = carcoordinates(cars)
    maketable(d)
    print
    m = raw_input('What is your next move? (format: car('+ carstring +') dir(F/B) steps) ').split()
    if validmove(d, signs[m[0]], m[1], int(m[2])):
         signs[m[0]].Move(m[1],int(m[2]))
    else:
         print
         print("Invalid move!")
else:
    os.system('cls' if os.name=='nt' else 'clear')
    d = carcoordinates(cars)
    maketable(d)
    print
    print "You win!"

# if __name__=="__main__":
     
