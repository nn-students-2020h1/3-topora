from Board import Board
from Renderer import Renderer
class BossPuzzle:
    #в итоге возвращает string что идет сразу в сообщение
    Board_size=4
    def __init__(self):
        self.board=Board(BossPuzzle.Board_size)
        self.renderer=Renderer()

    def get_board(self):
        return self.renderer.render(self.board)

    def start_new_game(self):
        self.board.start_pose()

    def action(self,command:str):
        coordinates={}
        try:
            coordinates['first_x']=ord(command.split()[0][0])-ord('a')+1
            coordinates['first_y']=int(command.split()[0][1])
            coordinates['second_x']=ord(command.split()[1][0])-ord('a')+1
            coordinates['second_y']=int(command.split()[1][1])
            if  not self.board.move_cells(coordinates):
                return False
        except BaseException:
            return False
        return  True