class A():
    def __init__(self):
        self.x=7
        self.y=8
        self.z="name"

class Employee(object):
     def __init__(self, _dict):
         self.__dict__.update(_dict)

class Employee_2(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

if __name__ == '__main__':
    d = {'x': 100, 'y': 300, 'z': "blah"}
    a = A()


    print(a.x, a.y, a.z)
    a.__dict__.update(d)
    print(a.x, a.y, a.z)

    dict = {'name': 'Oscar', 'lastName': 'Reyes', 'age': 32}
    e = Employee(dict)

    print(e.name)
    print(e.age)

    print(round(9.090298349, 2))



