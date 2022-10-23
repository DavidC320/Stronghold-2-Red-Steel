# 10/11/2022
# This is to test to see if class information can be transfered between each other

class Test1:
    def __init__(self, number):
        self.number = number

class Test2:
    def __init__(self, test, number):
        self.test = test
        self.number = number

class Main:
    def __init__(self):
        self.test1 = Test1(40)
        self.test2 = Test2(self.test1, self.test1.number)
        self.test3 = Test2(self.test2, None)

    def test_data(self):
        print(self.test1.number, self.test2.test.number, self.test2.number, self.test3.test.test.number)
        self.test1.number = 67556
        print(self.test1.number, self.test2.test.number, self.test2.number, self.test3.test.test.number)

Main().test_data()

a = "A"
b = "a"
if a and b != None:
    print(True)
else:
    print(False)