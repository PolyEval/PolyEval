from polyeval import parse_questions, initialize_template
import yaml

with open("./tests/data/hello_world.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.CLoader)

template = initialize_template("./execution-templates", targets=list(data.keys()))
for lang, code in data.items():
    project = template.create_execution_project(
        lang, code, f"test-{lang}", exist_ok=True
    )
    status, result = project.execute()
    if status == True:
        print(f"{lang}: {result}")
        project.clean()
    else:
        print(f"{lang}: Execution Failed!")
