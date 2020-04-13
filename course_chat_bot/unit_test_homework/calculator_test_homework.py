import  warnings
class Calculator:
    operator_tuple_int=('+', '-', '*', '/')
    operator_tuple_str=('+','-')
    @staticmethod
    def div(x, y):
        try:
            if y==0:
                raise BaseException
            return x / y
        except:
            return 0

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def sub(x, y):
        return x - y

    @staticmethod
    def mul(x, y):
        return x * y

    @staticmethod
    def get_numbers():
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        return num1, num2

    @staticmethod
    def check_operator_int(operator:str):
        if operator in Calculator.operator_tuple_int:
            return True
        else:
            return False

    @classmethod
    def calculate(cls,num1:int,num2:int,operator:str):
        access = cls.check_operator(operator)
        if not access:
           return None
        if operator == '+':
            return (cls.add(num1, num2))
        elif operator == '-':
            return (cls.sub(num1, num2))
        elif operator == '*':
            return (cls.mul(num1, num2))
        elif operator == '/':
            return (cls.div(num1, num2))


    @staticmethod
    def check_operator_str(operator:str):
        if operator in Calculator.operator_tuple_str:
            return True
        else:
            return False

    @staticmethod
    def sub_str(str1:str,str2:str):
        try:
            return str1[:len(str2)]
        except BaseException:
            return False

    @classmethod
    def calculate(cls,str1:str,str2:str,operator:str):
        if str1=='' or str2=='':
            warnings.warn('Empty arguments')
        access=Calculator.check_operator_str(operator)
        if not access:
            return None
        if operator=='+':
            return Calculator.add(str1,str2)
        elif operator=='-':
            return cls.sub_str(str1,str2)

