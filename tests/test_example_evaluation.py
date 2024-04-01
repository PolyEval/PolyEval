from polyeval import parse_questions, initialize_template, evaluate
import yaml

example_ped = open("tests/data/example.ped").read()
question = parse_questions(example_ped)[0]

with open("./tests/data/example.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.CLoader)

template = initialize_template("./execution-templates", targets=list(data.keys()))
for lang, code in data.items():
    status, result = evaluate(template, lang, question, code, exist_ok=True)
    if status == True:
        print(f"{lang}: Evaluation OK!")
    else:
        print(f"{lang}: Evaluation Failed! {result}")