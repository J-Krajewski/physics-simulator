from FallingBodyQuestion import FallingBodyQuestion
from Question import Question

example_question = FallingBodyQuestion(5,2)

example_question.generate_values(True)

example_question.calculate_time()

example_question.choose_unknown()

print(example_question.get_question_text())




