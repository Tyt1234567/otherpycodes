import random

class Generate_questions:
    def __init__(self):
        self.number11_18 = list(range(11,19))
        self.number11_99 = list(range(11,100))
        self.number2_9 = list(range(2,10))
        self.numberx0 = [10,20,30,40,50,60,70,80,90]
        self.number10_99 = list(range(10, 100))
        self.number1_9 = list(range(1, 10))
        self.number1_6 = list(range(1,7))
        self.number2_6 = list(range(2,7))
        self.signs = ['+', '-']

    # 20以内退位减法
    def two_digits_less_than_20_minus_one_digit(self):
        beijianshus = self.number11_18
        jianshus = self.number2_9
        questions = []
        length=0
        while length < 100:
            beijianshu = random.choice(beijianshus)
            jianshu = random.choice(jianshus)
            answer = beijianshu - jianshu
            if  answer > 0 and answer < 10:
                questions.append(f"{beijianshu} - {jianshu} =")
                length += 1
        return questions

    #两位数加减整十数
    def two_digits_minus_plus_x0(self):
        number1s = self.number11_99
        x0s = self.numberx0
        signs = self.signs
        questions = []
        length = 0
        while length < 100:
            number1 = random.choice(number1s)
            x0 = random.choice(x0s)
            sign = random.choice(signs)
            if sign == '+' and 0 < number1 + x0 < 100:
                questions.append(f'{number1} + {x0} =')
                length += 1
            if sign == '-' and 0 < number1 - x0 < 100:
                questions.append(f'{number1} - {x0} =')
                length += 1
        return questions

    #两位数加减一位数（进位、退位）
    def two_digits_minus_plus_one_digit(self):
        number1s = self.number10_99
        number2s = self.number1_9
        signs = self.signs
        questions = []
        length = 0
        while length < 100:
            number1 = random.choice(number1s)
            number2 = random.choice(number2s)
            sign = random.choice(signs)
            if sign == '+' and 0 <= number1 + number2 < 100 and int(str(number1 + number2)[0]) == int(str(number1)[0]) + 1:
                questions.append(f'{number1} + {number2} =')
                length += 1
            sign = random.choice(signs)
            if sign == '-' and 0 <= number1 - number2 < 100 and int(str(number1 - number2)[0]) == int(str(number1)[0]) - 1:
                questions.append(f'{number1} - {number2} =')
                length += 1
        return questions

    #6以内的乘法以及加减运算
    def mutiple_plus_mius_less_than_6(self):
        mutiples = self.number2_6
        signs = self.signs
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            plus = random.choice([multiple1,multiple2])
            sign = random.choice(signs)
            if sign == '+' and 0 <= multiple1*multiple2 + plus < 100 :
                questions.append(f'{multiple1} × {multiple2} + {plus} =')
                length += 1
            if sign == '-' and 0 <= multiple1 * multiple2 - plus < 100:
                questions.append(f'{multiple1} × {multiple2} - {plus} =')
                length += 1
        return questions

    #6以内的乘法运算
    def mutiple_less_than_6(self):
        mutiples = self.number2_6
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'{multiple1} × {multiple2} =')
            length += 1
        return questions

    #6以内乘法（求乘数）
    def solve_multipe_less_than_6(self):
        mutiples = self.number2_6
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'{multiple1} × (     ) = {multiple1*multiple2}')
            length += 1

            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'(     ) × {multiple2} = {multiple1 * multiple2}')
            length += 1
        return questions

    # 10以内的乘法以及加减运算
    def mutiple_plus_mius_less_than_10(self):
        mutiples = self.number2_9
        signs = self.signs
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            plus = random.choice([multiple1,multiple2])
            sign = random.choice(signs)
            if sign == '+' and 0 <= multiple1*multiple2 + plus < 100 :
                questions.append(f'{multiple1} × {multiple2} + {plus} =')
                length += 1
            if sign == '-' and 0 <= multiple1 * multiple2 - plus < 100:
                questions.append(f'{multiple1} × {multiple2} - {plus} =')
                length += 1
        return questions

    # 10以内的乘法运算
    def mutiple_less_than_10(self):
        mutiples = self.number2_9
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'{multiple1} × {multiple2} =')
            length += 1
        return questions

    # 10以内乘法（求乘数）
    def solve_multipe_less_than_10(self):
        mutiples = self.number2_9
        questions = []
        length = 0
        while length < 100:
            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'{multiple1} × (     ) = {multiple1*multiple2}')
            length += 1

            multiple1 = random.choice(mutiples)
            multiple2 = random.choice(mutiples)
            questions.append(f'(     ) × {multiple2} = {multiple1 * multiple2}')
            length += 1
        return questions


    #20以内求加数运算
    def calculate_plus(self):
        add = self.number1_9
        questions = []
        length = 0
        while length < 100:
            add1 = random.choice(add)
            add2 = random.choice(add)
            if length%2 == 0:
                questions.append(f'(    ) + {add2} = {add1+add2}')
            else:
                questions.append(f'{add1} + (    ) = {add1+add2}')
            length += 1
        return questions

    #20以内求减数/被减数运算
    def calculate_minus(self):
        beijianshus = self.number11_18
        jianshus = self.number2_9
        questions = []
        length = 0
        while length < 100:
            beijianshu = random.choice(beijianshus)
            jianshu = random.choice(jianshus)
            answer = beijianshu - jianshu
            if answer > 0 and answer < 10:
                if length%2==0:
                    questions.append(f"(    ) - {jianshu} = {beijianshu - jianshu}")
                else:
                    questions.append(f"{beijianshu} - (    ) = {beijianshu - jianshu}")
                length += 1
        return questions


if __name__ == "__main__":
    generator = Generate_questions()
