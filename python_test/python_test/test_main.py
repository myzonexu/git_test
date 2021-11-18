class class_test1:
    def __init__(self,a,b):
        self.var1=a
        self.var2=b
    def sum(self):
        return self.var1+self.var2
    def plus(self):
        self.var1=self.var2+1


def func_test1(test,aa,bb):
    test.var1=aa
    test.var2=bb
    test.sum()
    test.plus()
def func_test2(test):
    test=class_test1(10,20)

class_test1=class_test1(1,2)
func_test2(class_test1)
#func_test1(class_test1,3,4)
print(class_test1.var1,class_test1.var2)
        