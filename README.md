# Polyeval
Easy and Extensible Tool for Benchmark Construction and Evaluation in Multiple Programming Languages. 

## Installation

You can install `PolyEval` python package using `pip`:
```bash
$ pip install git+https://github.com/polyeval/polyeval.git
```

## Example

This repository contains tests for example usage, which leverage `Nix` for reproduction of the runtime enviroment.
```bash
$ git clone --recursive https://github.com/polyeval/polyeval
$ cd ./polyeval
$ nix-shell --pure # Will download pdm for project management, as well as dependencies for executing programs in all 34 programming languages. 
$ pdm install
$ pdm run python tests/test_example_evaluation.py # Will execute example tests for 34 programming languagaes.
```

Download dependencies may occupy lots of time and disk space. [polyeval-example](https://github.com/polyeval/polyeval-example) provides an example that download dependencies and evaluate programs of 8 mainstream programming languages.

```bash
$ git clone --recursive https://github.com/polyeval/polyeval-example
$ cd ./polyeval-example
$ nix-shell --pure
$ pdm install
$ pdm run python test_example_evaluation.py # Will execute example tests for 8 programming languagaes.
```

## Usage

### PolyEval Description(ped)
`PolyEval` defines a domain-specific language called `PolyEval Description`(ped). Here's an example:
```ped
def Example
    fun all_above(numbers: list<double>, threshold: double) -> bool
        ([1.0, 2.0, 3.0], 0.5) -> true
        ([1.0, 2.8, 3.0, 4.0, 5.0, 0.5], 0.7) -> false
```
This defines the behaviour of generated test program. For detailes, check [`PolyEvalDescription.md`](./PolyEvalDescription.md).

### Evaluation

For example, we can use `PolyEval` to check whether this C++ function pass the above testcases:
```cpp
bool allAbove(const vector<double>& numbers, double threshold) {
    return ranges::all_of(numbers, [=](double n) { return n > threshold; });
}
```
Then evaluate with this Python script:
```python
from polyeval import parse_questions
from polyeval.eval.execution import initialize_template
from polyeval.eval.evaluation import evaluate

ped_dsl = """
def Example
    fun all_above(numbers: list<double>, threshold: double) -> bool
        ([1.0, 2.0, 3.0], 0.5) -> true
        ([1.0, 2.8, 3.0, 4.0, 5.0, 0.5], 0.7) -> false
"""
question = parse_questions(ped_dsl)[0]

code = """
bool allAbove(const vector<double>& numbers, double threshold) {
    return ranges::all_of(numbers, [=](double n) { return n > threshold; });
}
"""
template = initialize_template("./execution-template", targets=["cpp"])
status, _ = evaluate(template, "cpp", question, code, exist_ok=True)
print(f"Evaluation Result: {status}")
```
More exmaples are placed at [`tests`](./tests) folder. You can run them directly:
```bash
$ python tests/test_execution.py
$ python tests/test_example_evaluation.py
```

## Supported Languages

Currently, 34 popular programming languages are supported in main packages: C#, C++, Clojure, CoffeeScript, Crystal, D, Dart, Elixir, Elm, Erlang, F#, Go, Groovy, Hack, Haskell, Java, JavaScript, Julia, Kotlin, Lua, Nim, Objective-C, OCaml, Perl, PHP, PureScript, Python, Racket, ReScript, Ruby, Rust, Scala, Swift, TypeScript.
Extra targets are supported in https://github.com/polyeval/polyeval-extra/.
