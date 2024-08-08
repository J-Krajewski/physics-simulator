
from Question import Question
import random
import math

class FallingBodyQuestion(Question):

    def __init__(self,max_marks, difficulty):
        super().__init__(max_marks, difficulty)
        self.__ball_radius = None
        self.__ball_y = None
        self.__ball_x = None
        self.__floor_y = None
        self.__floor_x = None
        self.__gravity = None
        self.__unknown = None
        self.__height = None
        self.__possible_unknowns = ["time","height"]
        self.__time_in_air = 0

    def generate_values(self,earth_gravity):
        self.__height = random.randint(30,70)
        self.__ball_y = 1
        self.__ball_x = 50
        self.__floor_x = 300
        self.__floor_y = self.__height + self.__ball_y

        if earth_gravity:
            self.__gravity = 9.80665
        else:
            self.__gravity = random.uniform(1.5,10.0)
    
    def calculate_time(self):
        self.__time_in_air = math.sqrt(2* self.__height/self.__gravity)
    
    def choose_unknown(self):
        self.__unknown = random.choice(self.__possible_unknowns)

    def print_question(self):

        print(f" A ball has a {self.__unknown} of {self.__height}m under Earth's gravity.  ")
        print(f"Calculate ")
        


        


    





