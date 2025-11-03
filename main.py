"""
Alien Numerals Calculation Application

This module provides functionality to convert Alien Numeral strings into
their integer equivalents.
"""

from typing import Dict


class AlienNumeralConverter:
    """
    A converter class for translating Alien Numeral strings to integers.
    
    The Alien Numeral system is similar to Roman numerals, using specific
    symbols that can be combined to represent numbers. Some symbol combinations
    follow a subtraction rule.
    
    Attributes:
        SYMBOL_VALUES (Dict[str, int]): Mapping of single symbols to their values.
        SUBTRACTION_CASES (Dict[str, int]): Mapping of two-character combinations
            that represent subtraction cases.
    
    Example:
        >>> converter = AlienNumeralConverter()
        >>> converter.to_integer("AAA")
        3
        >>> converter.to_integer("LBAAA")
        58
    """
    
    # Class-level constants for symbol mappings
    SYMBOL_VALUES: Dict[str, int] = {
        'A': 1,
        'B': 5,
        'Z': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'R': 1000
    }
    
    def __init__(self) -> None:
        """
        Initialize the AlienNumeralConverter.
        
        The converter uses predefined mappings for symbol values and
        subtraction cases to perform conversions.
        """
        pass  # All data is stored at class level
    
    def to_integer(self, s: str) -> int:
        """
        Convert an Alien Numeral string to its integer equivalent.
        
        Uses the step-by-step left-to-right method with peek-ahead logic:
        1. Create a "bucket" (total) initialized to 0
        2. Loop through the string from index 0 to second-to-last character
        3. For each character, peek at the next character and compare values:
           - If current_value < next_value: Subtract (subtraction case)
           - If current_value >= next_value: Add (addition case)
        4. After the loop, add the last character (always an addition case)
        
        Args:
            s (str): The Alien Numeral string to convert. Must contain only
                valid symbols: A, B, Z, L, C, D, R.
        
        Returns:
            int: The integer value of the Alien Numeral string.
        
        Raises:
            KeyError: If an invalid symbol is encountered in the string.
        
        Example:
            >>> converter = AlienNumeralConverter()
            >>> converter.to_integer("RCRZCAB")
            1994
            >>> converter.to_integer("AAA")
            3
        """
        
        total: int = 0
        for i in range(len(s) - 1):
            current_value: int = self.SYMBOL_VALUES[s[i]]
            next_value: int = self.SYMBOL_VALUES[s[i + 1]]
            
            if current_value < next_value:
                total -= current_value
            else:
                total += current_value
                
        total += self.SYMBOL_VALUES[s[-1]]
        return total
    
    def is_valid(self, s: str) -> bool:
        """
        Check if a string contains only valid Alien Numeral symbols.
        
        Args:
            s (str): The string to validate.
        
        Returns:
            bool: True if all characters are valid symbols, False otherwise.
        
        Example:
            >>> converter = AlienNumeralConverter()
            >>> converter.is_valid("ABC")
            True
            >>> converter.is_valid("XYZ")
            False
        """
        return all(char in self.SYMBOL_VALUES for char in s)
    
    def get_symbol_info(self) -> str:
        """
        Get a formatted string describing all available symbols and their values.
        
        Returns:
            str: A formatted string with symbol information.
        """
        info = "Single Symbol Values:\n"
        for symbol, value in sorted(self.SYMBOL_VALUES.items(), key=lambda x: x[1]):
            info += f"  {symbol} = {value}\n"
        
        return info


def main() -> None:
    """
    Main function demonstrating the AlienNumeralConverter with test cases.
    """
    # Create an instance of the converter
    converter = AlienNumeralConverter()
    
    # Display symbol information
    print("=" * 60)
    print("ALIEN NUMERALS CALCULATION APPLICATION")
    print("=" * 60)
    print()
    print(converter.get_symbol_info())
    print("=" * 60)
    print()
    
    # Test cases as specified
    test_cases = [
        ("AAA", 3),
        ("LBAAA", 58),
        ("RCRZCAB", 1994)
    ]
    
    print("TEST CASES:")
    print("-" * 60)
    
    for numeral, expected in test_cases:
        result = converter.to_integer(numeral)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"Input: {numeral:15} | Result: {result:5} | Expected: {expected:5} | {status}")
    
    print("-" * 60)
    print()
    
    # Additional demonstration examples
    print("ADDITIONAL EXAMPLES:")
    print("-" * 60)
    
    additional_examples = [
        "A",      # 1
        "B",      # 5
        "AB",     # 4
        "BA",     # 6
        "Z",      # 10
        "AA",     # 2
        "R",      # 1000
        "RR",     # 2000
        "RCRZ",   # 1990
        "CDZCAB", # 494
    ]
    
    for numeral in additional_examples:
        result = converter.to_integer(numeral)
        print(f"Input: {numeral:15} | Result: {result:5}")
    
    print("-" * 60)
    print()
    
    # Interactive section
    print("Try your own conversions (press Ctrl+C to exit):")
    print()
    try:
        while True:
            user_input = input("Enter Alien Numeral: ").strip().upper()
            if not user_input:
                continue
            
            if converter.is_valid(user_input):
                result = converter.to_integer(user_input)
                print(f"Result: {result}")
            else:
                print(f"Invalid input! Use only: {', '.join(sorted(converter.SYMBOL_VALUES.keys()))}")
            print()
    except (KeyboardInterrupt, EOFError):
        print("\n\nThank you for using Alien Numerals Calculator!")


if __name__ == "__main__":
    main()
