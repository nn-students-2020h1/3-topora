from Board import Board

class Renderer:
    def __init__(self):
        pass
    def render_list(self,board : Board): # list:int
        coord_list=[] # x: int , y: int
        render_queue=[]
        for i in range(board.size*board.size):
            coord_list.append([((i)%board.size)+1,((i)//board.size)+1])
        for cell  in coord_list:
            if cell[0]==board.freecoord[0] and cell[1]==board.freecoord[1]:
                render_queue.append(0)
            for numb in board.numbs:
                if numb.x==cell[0] and numb.y==cell[1]:
                    render_queue.append(numb.numb)
        return  render_queue

    def symbol_translate(self,numb: int): #string
        if numb>0:
            return chr(9312+numb-1)
        else:
            return chr(9711)


    def render(self,board : Board):
        board_draw=''
        render_queue=self.render_list(board)
        board_draw=chr(9679)+' '
        for i in range(0,board.size):
            board_draw+=chr(ord('a')+i)+'  '

        counter=0
        for i in range(1,len(render_queue)+1):
            if((i-1)%board.size==0):
                counter+=1
                board_draw+='\n'+str(counter)+' '
            board_draw+=self.symbol_translate(render_queue[i-1])

        return board_draw
