

class Question:

    def __init__(self, max_marks, difficulty):
        self._max_marks = max_marks
        self.__difficulty = difficulty
        self.__correct = False
        self.__user_answer = None
        self.__correct_answer = None


    def check_answer(self):
        if self.__user_answer == self.__correct_answer():
            print("Correct Answer !!!")
            return True, self.__max_marks
        else:
            print(f"{self.__user_answer} is incorrect, correct answer {self.__correct_answer}")
            return False, 0
        
