# Polyeval
Easy and Extensible Tool for Benchmark Construction and Evaluation in Multiple Programming Languages. 

## Prerequisite
`PolyEval` leverages `Nix` for reproduction of the runtime enviroment. You need to install `Nix` on your computer first. If you are using Windows, using `NixOS-WSL` is highly recommended.

After installation of  `Nix`, clone this repository with submodules:
```bash
$ git clone --recursive https://github.com/polyeval/polyeval
```
And use `nix-shell` to download the dependencies and reproduce the environment:
```bash
$ cd ./polyeval
$ nix-shell --pure
```
Note: this will download all dependencies for executing programs in 34 programming languages, which may occupy a lot of download time and disk space.

The `compact` branch includes a lighter version that just download dependencies of 8 most popular languages: C#, C++, Go, Java, JavaScript, PHP, Python, Ruby, which requires less download time and disk space. You can clone the branch following these instructions: 
```bash
$ git clone -b compact --recursive https://github.com/polyeval/polyeval
$ cd ./polyeval
$ nix-shell --pure
```

The project leverage `PDM` for install packages:
```bash
$ pdm use # select any python version here
$ pdm install
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

Currently, 42 popular programming languages are supported: C#, C++, Clojure, CoffeeScript, Common Lisp, Crystal, D, Dart, Elixir, Elm, Emacs Lisp, Erlang, F#, Go, Groovy, Hack, Haskell, Haxe, Java, JavaScript, Julia, Kotlin, Lua, Nim, Objective-C, OCaml, Perl, PHP, PureScript, Python, Racket, Raku, ReasonML, ReScript, Ruby, Rust, Scala, Scheme, StandardML, Swift, TypeScript, Visual Basic.