import unittest
from  calculator_test_homework import Calculator

class Test_calculator(unittest.TestCase):

    def test_div(self):
        self.assertEqual(Calculator.div(1,2),1/2)

    def test_add(self):
        self.assertNotEqual(Calculator.add(1,2),2)

    def test_check_operator_0(self):
        self.assertFalse(Calculator.check_operator_int('&'))

    def test_check_operator_1(self):
        self.assertTrue(Calculator.check_operator_int('/'))

    def test_calculation_str_0(self):
        Mystr='Hello'
        self.assertIs(Mystr,Calculator.add(Mystr,''))

    def test_add_str(self):
        Mystr='Hello my'
        self.assertNotIn(Mystr,Calculator.calculate(Mystr,' world','-'))

    def test_calcalation_int_1(self):
        self.assertIsNot([2],[Calculator.add(1,1)])

    def test_div_except(self):
        self.assertRaises(BaseException,Calculator.div(1,0))

    def test_calculate_none(self):
        c=Calculator.calculate(1,2,'+')
        self.assertIsNotNone(Calculator.calculate(1,2,'+'))

    def test_operator_tuple_0(self):
        self.assertIn('+',Calculator.operator_tuple_int)

    def test_calculation_0(self):
        self.assertIsNone(Calculator.calculate(2,3,'&'))

    def test_calculation_str_1(self):
        self.assertIsInstance(Calculator.calculate(1,2,'+'),int)

    def test_calculation_str_2(self):
        self.assertNotIsInstance(Calculator.calculate('2','3','+'),int)
    def test_calculation_str_3(self):
        self.assertWarns(Warning,Calculator.calculate,'','warn me please','+')

