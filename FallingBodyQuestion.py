
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
        

        self.__question_message = None

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

    def get_question_text(self):
        if self.__unknown == "time":
            self.__question_message = f"On Earth, a ball is dropped from a height of {self.__height} and lands at collides with the ground at time t, find t ({self._max_marks} marks)"
        elif self.__unknown == "height":
            self.__question_message = f"On Earth, a ball is dropped from height h and lands at collides with the ground at time {self.__time_in_air}, find h ({self._max_marks} marks)"

        return self.__question_message
    
    def get_floor_y(self):
        return  self.__floor_y
    
    def get_floor_x(self):
        return  self.__floor_x
    
    def get_ball_y(self):
        return  self.__ball_y
    
    def get_ball_x(self):
        return  self.__ball_x
    
    def get_ball_radius(self):
        return  self.__ball_radius
    

   

            
        


        


    





