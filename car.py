# -*- coding: cp1250 -*-
class Car(object):
    def __init__(self, x, y, lie, length, sign = 'C'):
        '''
        Stores the position datas of the car.

        (x,y): gives the position of upper left side of the car, in Descartes coordinate system.
               positive direct: x:right y:down        
        direction: gives ,whether the car lie horizontally or vertically
        '''
        self.x = x
        self.y = y
        self.lie = lie
        self.len = length
        self.sign = sign

    def Move(self, direction, steps):
        if self.lie == 'H':
            if direction == 'F' or direction == 'f':
                self.x += steps
            elif direction == 'B' or direction == 'b':
                self.x -= steps
        elif self.lie == 'V':
            if direction == 'F' or direction == 'f':
                self.y += steps
            elif direction == 'B' or direction == 'b':  
                self.y -= steps
        else:   #exceptionre cserélni kesobb
            print('hibas bemenet')

    def GetCoordinates(self):
        if self.lie == 'V':
            return[(self.x,self.y + i) for i in range(self.len)]
        if self.lie =='H':
            return[(self.x + i,self.y) for i in range(self.len)]

    def GetCoordinatesDict(self):
        return dict(map(lambda t:(t,self.sign),self.GetCoordinates()))
