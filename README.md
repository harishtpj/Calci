# 🧮 Calci
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![python-version](https://img.shields.io/badge/Python-v3.9.10-blue)](https://www.python.org/)
![calci-version](https://img.shields.io/badge/Calci-v1.0-orange)
[![Maintainability](https://api.codeclimate.com/v1/badges/2314adc23737058808cd/maintainability)](https://codeclimate.com/github/harishtpj/Calci/maintainability)

Calci - A Modern, Fast compiled language written in Python.

# ℹ About
**Calci** is a Compiler written in *Python* which Compiles to *C Language*. This language has a very **modern and simple syntax** which lessens the learning curve. This syntax is derived from Pascal and C Languages. The current version of Calci is **v1.0**.

# 📃 Requirements
- Python >= 3.6
- Any C compiler (preferred [tcc](https://bellard.org/tcc/)/[gcc](https://gcc.gnu.org/) compiler)

# 💻 Running the compiler
Use command ```calci``` to run compiler
```
usage: calci [-h] [-l LANG] [-S] [-v] file

The Calci programming language compiler

positional arguments:
  file                  The File to compile

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  the Language to Transpile
  -S, --source          only Compiles Calci File to Given Language
  -v, --version         shows version info of Calci compiler
```

# A Sample Hello, World! Program
Save the following file as ```hello.ca```
``` python
# This is a Hello, World program written in Calci language

println "Hello, World!"
println "This is the first program written in calci lang"
```
run ```calci hello.ca``` to get executable. To get transpiled C code. run ```calci -S hello.ca```

# 📝 License

#### Copyright © 2022 [M.V.Harish Kumar](https://github.com/harishtpj). <br>
#### This project is [BSD-3](https://github.com/harishtpj/Calci/blob/master/LICENSE) licensed.
