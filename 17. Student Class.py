class Student:
    def check_pass_fail(self):
        if self.marks>=40:
            return True
        else:
            return False


student1 = Student()
student1.name = "Sumaiya"
student1.marks = 100

print(student1.name)
print(student1.marks)

did_pass = student1.check_pass_fail()
print(did_pass)        
print('\n')

student2 = Student()
student2.name = "Sabic"
student2.marks = 100

print(student2.name)
print(student2.marks)

did_pass = student2.check_pass_fail()
print(did_pass)
print('\n')

student3 = Student()
student3.name = "Saiki"
student3.marks = 30

print(student3.name)
print(student3.marks)

did_pass = student3.check_pass_fail()
print(did_pass)   
