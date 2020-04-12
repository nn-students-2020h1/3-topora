import unittest
from Board import Numbers, Board
from game import BossPuzzle
from Renderer import Renderer

class Test_Board(unittest.TestCase):
    def setUp(self):
        self.board=Board(4)
        self.board.start_pose(0)
    def tearDown(self):
        self.board= None

    def test_is_move_possible_1(self):
        coord_dict={'first_x':self.board.size+1,'first_y':self.board.size,
                    'second_x':self.board.size,'second_y':self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict),False)
    def test_is_move_possible_2(self):
        coord_dict = {'first_x': self.board.size-1, 'first_y': self.board.size-1,
                      'second_x': self.board.size, 'second_y': self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)
    def test_is_move_possible_3(self):
        coord_dict = {'first_x': self.board.size - 1, 'first_y': self.board.size - 1,
                      'second_x': self.board.size, 'second_y': self.board.size}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)
    def test_is_move_possible_4(self):
        coord_dict = {'first_x': self.board.freecell[0], 'first_y': self.board.freecell[1],
                      'second_x': self.board.freecell[0]-1, 'second_y': self.board.freecell[1]}
        self.assertEqual(self.board.is_move_possible(coord_dict), False)
    def test_is_move_possible_5(self):
        coord_dict = {'first_x': self.board.freecell[0]-1, 'first_y': self.board.freecell[1],
                      'second_x': self.board.freecell[0], 'second_y': self.board.freecell[1]}
        self.assertEqual(self.board.is_move_possible(coord_dict), True)

    def test_start_pose(self):
        self.board.start_pose(1)
        self.assertEqual(self.board.numbs[1].x,self.board.Start_poses[1][2][0])
        self.assertEqual(self.board.numbs[1].y, self.board.Start_poses[1][2][1])
    def test_move_body(self):
        coord_dict = {'first_x': self.board.numbs[4].x, 'first_y': self.board.numbs[4].y,
                      'second_x': self.board.freecell[0], 'second_y': self.board.freecell[1]}
        self.board.move_body(coord_dict)
        self.assertEqual(self.board.numbs[4].x,coord_dict['second_x'])
        self.assertEqual(self.board.numbs[4].y,coord_dict['second_y'])

    def test_check_for_solving_1(self):
        self.board.start_pose(0)
        self.assertEqual(self.board.check_for_solving(),True)
    def test_check_for_solving_2(self):
        self.board.start_pose(1)
        self.assertEqual(self.board.check_for_solving(),False)

class Test_Renderer(unittest.TestCase):
    def setUp(self):
        self.renderer=Renderer()
    def tearDown(self):
        self.renderer=None
