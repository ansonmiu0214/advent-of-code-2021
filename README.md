# (Multilingual) Advent of Code 2021

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)

[**_Advent of Code_**](https://adventofcode.com/2021)
is a great opportunity to brush up on existing languages
and learn some new ones!

<p align="center">
<a href="#usage">Usage</a>
-
<a href="#directory-structure">Directory Structure</a>
-
<a href="#extending-language-support">Extending Language Support</a>
</p>

---

## Usage

```
usage: ./run_solution.sh LANGUAGE -d DAY -input INPUT -p PART

arguments:
                LANGUAGE    programming language
  -d, --day     DAY         the day of a problem, [1,25]
  -i, --input   INPUT       type of input file, {sample,test}
  -p, --part    PART        the part of a problem, {1,2}
```

### Examples

Run the **Golang** solution for **part 2** of **day 1**'s problem, using the **test** input

```bash
$ ./run_solution.sh golang --day 1 --input test --part 2
```

Run the **Python** solution for **part 1** of **day 2**'s problem, using the **sample** input

```bash
$ ./run_solution.sh python --day 2 --input sample --part 1
```

## Directory Structure

| File / Directory  | Description                                  |
| ----------------- | -------------------------------------------- |
| `data/sample/`    | Input files for the sample cases             |
| `data/test/`      | Input files for the user-specific test cases |
| `run_solution.sh` | Multilingual solution dispatcher             |

## Extending Language Support

Suppose you would like to write solutions in a new language, say `bash`.

1. Create a solutions directory for the new language.

    ```bash
    $ mkdir bash
    ```

2. Add a solution to the new solutions directory.

    ```bash
    $ echo "echo Hello, world!" > bash/day1.sh
    ```

3. Implement an adapter in `run_solutions.sh` for the new language.

    ```bash
    # file: ./run_solution.sh

    function pythonSolution  {... }
    function goSolution { ... }

    function bashSolution {
        SOLUTION_DIR=$1
        DAY=$2
        INPUT_FILE=$3
        PART=$4

        SOLUTION="$SOLUTION_DIR/day$DAY.sh"
        if [[ ! -f $SOLUTION ]]; then
            error "Cannot find solution: $SOLUTION"
        fi

        set -x
        bash $SOLUTION
    }
    ```

4. Register the new adapter in `run_solution.sh`.

    ```bash
    # file: ./run_solution.sh

    # Select the adapter function based on the user-specified language.
    case "$LANGUAGE" in
        python)
            RUN_SOLUTION=pythonSolution
            ;;
        golang)
            RUN_SOLUTION=golangSolution
            ;;
        #++++++++++++++++++++++++++++
        bash)
            RUN_SOLUTION=bashSolution
            ;;
        #++++++++++++++++++++++++++++
        *)
            error "Unsupported language: $LANGUAGE"
            ;;
    esac
    ```
