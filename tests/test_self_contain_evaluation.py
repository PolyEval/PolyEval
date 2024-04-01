from polyeval import parse_questions, initialize_template, evaluate, find_target
import yaml

example_ped = open("tests/data/self_contain.ped").read()
question = parse_questions(example_ped)[0]

with open("./tests/data/hello_world.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.CLoader)

template = initialize_template("./execution-templates", targets=list(data.keys()))
for lang in data:
    code = find_target(lang).code_generator.gen_all_self_contain(question.functions)
    status, result = evaluate(template, lang, question, code, exist_ok=True)
    if status == True:
        print(f"{lang}: Evaluation OK!")
    else:
        print(f"{lang}: Evaluation Failed! {result}")