# Alien-Numerals-Calculation-App

A modern Python application for converting Alien Numeral strings to integers.

## Overview

The Alien Numeral system is similar to Roman numerals, where symbols represent specific values and can be combined to form larger numbers. Some symbol combinations follow a subtraction rule for efficient representation.

## Features

- **Object-Oriented Design**: Clean, maintainable code using modern OOP principles
- **Type Hinting**: Full type annotations for better code clarity and IDE support
- **Comprehensive Docstrings**: Detailed documentation following Google docstring style
- **Validation**: Built-in validation for input strings
- **Interactive Mode**: Test conversions interactively
- **Extensive Examples**: Predefined test cases demonstrating functionality

## Symbol System

### Single Symbol Values
- `A` = 1
- `B` = 5
- `Z` = 10
- `L` = 50
- `C` = 100
- `D` = 500
- `R` = 1000

### Formation Rules

Like Roman numerals, Alien Numerals follow specific rules to prevent ambiguity:

#### 1. **Repetition Limits**
- **Repeatable up to 3 times**: `A`, `Z`, `C`, `R`
  - ✓ Valid: `AAA` (3), `ZZZ` (30), `CCC` (300)
  - ✗ Invalid: `AAAA` (use `AB` for 4), `ZZZZ` (use `ZL` for 40)
- **Cannot repeat**: `B`, `L`, `D`
  - ✓ Valid: `B` (5), `L` (50), `D` (500)
  - ✗ Invalid: `BB`, `LL`, `DD`

#### 2. **Valid Subtraction Pairs**
- `A` can only precede `B` or `Z`: `AB` (4), `AZ` (9)
- `Z` can only precede `L` or `C`: `ZL` (40), `ZC` (90)
- `C` can only precede `D` or `R`: `CD` (400), `CR` (900)
- ✗ Invalid combinations: `AL`, `AR`, `ZD`, `ZR`, etc.

#### 3. **Why These Rules?**
Just like Roman numerals don't use `IIII` for 4 (instead using `IV`), these rules ensure:
- **Uniqueness**: Only one correct way to write each number
- **Brevity**: Shorter representations (e.g., `AB` instead of `AAAA`)
- **Clarity**: Prevents ambiguous or non-standard forms

## Installation

### Prerequisites
- Python 3.9 or higher

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/spksupakorn/Alien-Numerals-Calculation-App.git
   cd Alien-Numerals-Calculation-App
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

## Usage

### Option 1: Running Directly with Python
```bash
python main.py
# or
python3 main.py
```

### Option 2: Running with Docker 🐳

Docker provides a consistent environment across all platforms without needing to install Python locally.

#### Build the Docker image:
```bash
docker build -t alien-numerals-app .
```

#### Run the application:
```bash
docker run -it alien-numerals-app
```

#### Quick one-liner (build and run):
```bash
docker build -t alien-numerals-app . && docker run -it alien-numerals-app
```

#### Other useful Docker commands:
```bash
# List Docker images
docker images

# Remove the image
docker rmi alien-numerals-app

# Run without interactive mode (just see the demo)
docker run alien-numerals-app

# View running containers
docker ps

# Stop a running container
docker stop <container-id>
```

**Note**: The `-it` flags are required for the interactive mode to work properly in Docker.

### Using as a Module

```python
from main import AlienNumeralConverter

# Create a converter instance
converter = AlienNumeralConverter()

# Convert Alien Numerals to integers
result = converter.to_integer("AAA")  # Returns: 3
result = converter.to_integer("LBAAA")  # Returns: 58
result = converter.to_integer("RCRZCAB")  # Returns: 1994

# Validate if string contains only valid symbols
is_valid = converter.is_valid("ABC")  # Returns: True
is_valid = converter.is_valid("XYZ")  # Returns: False

# Validate if numeral follows proper formation rules
is_valid, error = converter.is_valid_numeral("AAA")   # Returns: (True, "")
is_valid, error = converter.is_valid_numeral("AAAA")  # Returns: (False, "Symbol 'A' repeats...")

# Safe conversion with validation (recommended)
result, error = converter.to_integer_safe("AB")    # Returns: (4, "")
result, error = converter.to_integer_safe("AAAA")  # Returns: (None, "Symbol 'A' repeats...")

# Get symbol information
info = converter.get_symbol_info()
print(info)
```

### Validation Examples

```python
# Valid numerals
converter.is_valid_numeral("AAA")     # (True, "") - 3
converter.is_valid_numeral("AB")      # (True, "") - 4 (subtraction)
converter.is_valid_numeral("ZZZ")     # (True, "") - 30
converter.is_valid_numeral("RCRZCAB") # (True, "") - 1994

# Invalid numerals - too many repetitions
converter.is_valid_numeral("AAAA")    # (False, "Symbol 'A' repeats more than 3 times...")
converter.is_valid_numeral("BBBB")    # (False, "Symbol 'B' repeats more than 1 time...")

# Invalid numerals - wrong subtraction pairs
converter.is_valid_numeral("AL")      # (False, "Invalid subtraction pair: 'AL'...")
converter.is_valid_numeral("ZD")      # (False, "Invalid subtraction pair: 'ZD'...")
```

## Test Cases

The application includes the following verified test cases:

| Input      | Expected Output | Breakdown                                                    |
|------------|-----------------|--------------------------------------------------------------|
| `AAA`      | 3               | A≥A(+1) → A≥A(+1) → +A(1) = 3                                |
| `LBAAA`    | 58              | L≥B(+50) → B≥A(+5) → A≥A(+1) → A≥A(+1) → +A(1) = 58         |
| `RCRZCAB`  | 1994            | R≥C(+1000) → C<R(-100) → R≥Z(+1000) → Z<C(-10) → C≥A(+100) → A<B(-1) → +B(5) = 1994 |

## Algorithm

The conversion algorithm uses a **step-by-step left-to-right peek-ahead method**:

### Step-by-Step Process:

1. **Initialize**: Create a "bucket" (total) starting at 0

2. **Main Loop**: Iterate from the first character to the **second-to-last** character
   - Get the value of the current character (at index `i`)
   - Get the value of the next character (at index `i+1`) - this is the "peek ahead"
   - **Compare the values**:
     - If `current_value < next_value`: **Subtract** the current value (subtraction case)
     - If `current_value >= next_value`: **Add** the current value (addition case)

3. **Final Step**: Add the last character's value (always addition, as there's no next character to compare)

### Example Walkthrough: `RCRZCAB` → 1994

```
i=0: R(1000) vs C(100)  → 1000 >= 100 → ADD 1000     → total = 1000
i=1: C(100)  vs R(1000) → 100 < 1000  → SUBTRACT 100 → total = 900
i=2: R(1000) vs Z(10)   → 1000 >= 10  → ADD 1000     → total = 1900
i=3: Z(10)   vs C(100)  → 10 < 100    → SUBTRACT 10  → total = 1890
i=4: C(100)  vs A(1)    → 100 >= 1    → ADD 100      → total = 1990
i=5: A(1)    vs B(5)    → 1 < 5       → SUBTRACT 1   → total = 1989
Finally: Add B(5)                      → total = 1994 ✓
```

## Project Structure

```
Alien-Numerals-Calculation-App/
├── main.py              # Main application with AlienNumeralConverter class
├── pyproject.toml       # Project configuration
├── README.md            # This file
├── Dockerfile           # Docker container configuration
├── .dockerignore        # Docker ignore patterns
└── .python-version      # Python version specification
```

## Requirements

- Python >= 3.9
- No external dependencies required (uses only standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created by spksupakorn

## Acknowledgments

Inspired by Roman numeral systems and designed as an educational example of clean Python OOP design.
