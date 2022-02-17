class Person:
    "This is a person class."
    age = 10

    def greet(self):
        print('Hello')


#create a new object of person class
harry = Person()

#output: <function Person.greet>
print(Person.greet)

#Output: <bound method Person.greet of <__main__.Person object>>
print(harry.greet)

#Calling objects greet() method
#Output: Hello
harry.greet()
