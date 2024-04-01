from polyeval import *

ped_dsl = open("./tests/self_contain.ped").read()
questions = parse_questions(ped_dsl)
assert len(questions) == 1
question = questions[0]
question.pretty_print()