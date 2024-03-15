# calculator-py

## About

Calculator project from [Luiz Otávio Miranda's Python course](https://www.udemy.com/course/python-3-do-zero-ao-avancado/) to learn the principles of [PySide6](https://pypi.org/project/PySide6/), a graphical user interface (GUI) library.

## Visuals

<p align="center">
  <img src="https://github.com/guugimeness/calculator-py/blob/ba5bca1bb1619a9472b1f805a498bbdf599b0234/assets/calculator.png" alt="Image">
</p>

## Keyboard Shortcuts

* Enter: Enter, Return and '='
* Clear: ESC and 'C'
* Delete: Backspace, Delete and 'D'
* Pow: 'P'

## Installation

```bash
# Clone this repository
$ git clone https://github.com/guugimeness/calculator-py

# Access the project folder in your terminal
$ cd calculator-py

# Create and activate your virtual environment
$ python3 -m venv venv
$ source venv/bin/activate

# Install the dependencies using pip
$ pip install -r requirements.txt

# Use PyInstaller to create the calculator executable
$ pyinstaller Calculator.spec

# The application will be created in /dist
```

## Tech Stack

The following tools were used in the construction of the project:
* [Python](https://www.python.org/)
* [PySide6](https://pypi.org/project/PySide6/)
* [PyInstaller](https://pyinstaller.org/en/stable/)

## License

This project is under the license [MIT](./LICENSE)

## Status: Finished