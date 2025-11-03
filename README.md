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

### Running the Application
```bash
python main.py
```

### Using as a Module

```python
from main import AlienNumeralConverter

# Create a converter instance
converter = AlienNumeralConverter()

# Convert Alien Numerals to integers
result = converter.to_integer("AAA")  # Returns: 3
result = converter.to_integer("LBAAA")  # Returns: 58
result = converter.to_integer("RCRZCAB")  # Returns: 1994

# Validate input
is_valid = converter.is_valid("ABC")  # Returns: True
is_valid = converter.is_valid("XYZ")  # Returns: False

# Get symbol information
info = converter.get_symbol_info()
print(info)
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
