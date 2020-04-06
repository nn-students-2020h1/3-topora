

class Numbers:
    def __init__(self,numb: int,x: int,y:int):
        self.numb=numb
        self.x=x
        self.y=y

first_position=[[1,4],[3,2],[3,3],[3,1],[4,1],[2,3],[1,1],[4,3],
                [1,3],[3,4],[2,4],[2,2],[2,1],[4,4],[4,2],[1,2]]
Start_poses=[first_position]
class Board:



    def __init__(self,size:int):
        self.size=size
        self.numbs=[]
        self.freecoord=[self.size,self.size]
        for i in range(1,self.size*self.size):
            self.numbs.append(Numbers(i,((i-1)%self.size)+1,((i-1)//self.size)+1))

    def is_move_possible(self,coord:dict):
        for each in coord.keys():
            if(coord[each]<0 or coord[each]>self.size):
                return False
        if( not ((abs(coord['first_x']-coord['second_x'])==1 and coord['first_y']==coord['second_y']) or
                 (abs(coord['first_y']-coord['second_y'])==1 and coord['first_x']==coord['second_x']))):
            return  False
        if (coord['second_x']==self.freecoord[0] and coord['second_y']==self.freecoord[1]):
            return True
        return False

    def move_body(self,coord:dict):
        for numb in self.numbs:
            if (coord['first_x'] == numb.x and coord['first_y'] == numb.y):
                numb.x, self.freecoord[0] = self.freecoord[0], numb.x
                numb.y, self.freecoord[1] = self.freecoord[1], numb.y
                break

    def move_cells(self,coord:dict):
        if self.is_move_possible(coord):
            self.move_body(coord)
            return True
        else:           return False

    def start_pose(self):
        self.freecoord=Start_poses[0][0]
        self.numbs.clear()
        for i in range(1,self.size*self.size):
            self.numbs.append(Numbers(i,Start_poses[0][i][0],Start_poses[0][i][1]))