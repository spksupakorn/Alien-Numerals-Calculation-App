"""
Alien Numerals Calculation Application

This module provides functionality to convert Alien Numeral strings into
their integer equivalents.
"""

from typing import Dict, Tuple, Optional


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
    
    # Maximum repetitions allowed for each symbol (like Roman numerals)
    MAX_REPETITIONS: Dict[str, int] = {
        'A': 3,  # AAA is OK (3), but AAAA (4) should be AB
        'B': 1,  # B cannot repeat (use Z for 10)
        'Z': 3,  # ZZZ is OK (30), but ZZZZ (40) should be ZL
        'L': 1,  # L cannot repeat (use C for 100)
        'C': 3,  # CCC is OK (300), but CCCC (400) should be CD
        'D': 1,  # D cannot repeat (use R for 1000)
        'R': 3   # RRR is OK (3000)
    }
    
    # Valid subtraction pairs (smaller value can appear before larger value)
    VALID_SUBTRACTION_PAIRS: Dict[str, list] = {
        'A': ['B', 'Z'],      # A can appear before B (AB=4) or Z (AZ=9)
        'Z': ['L', 'C'],      # Z can appear before L (ZL=40) or C (ZC=90)
        'C': ['D', 'R']       # C can appear before D (CD=400) or R (CR=900)
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
    
    def is_valid_numeral(self, s: str) -> Tuple[bool, str]:
        """
        Check if a string follows proper Alien Numeral formation rules.
        
        Rules (similar to Roman numerals):
        1. Only valid symbols allowed
        2. Symbols cannot repeat more than their maximum allowed times
           - A, Z, C, R can repeat up to 3 times (e.g., AAA = 3, but AAAA is invalid, use AB)
           - B, L, D can appear only once (no BB, LL, DD)
        3. Subtraction only works for specific pairs:
           - A can only precede B or Z
           - Z can only precede L or C
           - C can only precede D or R
        4. A smaller value can only appear before one larger value
        
        Args:
            s (str): The Alien Numeral string to validate.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
                - (True, "") if valid
                - (False, error_message) if invalid
        
        Example:
            >>> converter = AlienNumeralConverter()
            >>> converter.is_valid_numeral("AAA")
            (True, '')
            >>> converter.is_valid_numeral("AAAA")
            (False, "Symbol 'A' repeats more than 3 times consecutively")
            >>> converter.is_valid_numeral("AB")
            (True, '')
        """
        # Check if string is empty
        if not s:
            return (False, "Empty string is not a valid numeral")
        
        # Check if all characters are valid symbols
        if not self.is_valid(s):
            invalid_chars = [c for c in s if c not in self.SYMBOL_VALUES]
            return (False, f"Invalid symbols: {', '.join(invalid_chars)}")
        
        # Check for excessive repetitions
        i = 0
        while i < len(s):
            char = s[i]
            count = 1
            
            # Count consecutive repetitions
            while i + count < len(s) and s[i + count] == char:
                count += 1
            
            # Check against maximum allowed repetitions
            max_allowed = self.MAX_REPETITIONS.get(char, 1)
            if count > max_allowed:
                return (False, f"Symbol '{char}' repeats more than {max_allowed} time(s) consecutively. Use subtraction notation instead (e.g., AB for 4, not AAAA)")
            
            i += count
        
        # Check for invalid subtraction patterns
        for i in range(len(s) - 1):
            current = s[i]
            next_char = s[i + 1]
            current_value = self.SYMBOL_VALUES[current]
            next_value = self.SYMBOL_VALUES[next_char]
            
            # If current < next, it's a subtraction case - validate it
            if current_value < next_value:
                if current not in self.VALID_SUBTRACTION_PAIRS:
                    return (False, f"Symbol '{current}' cannot be used in subtraction notation")
                
                if next_char not in self.VALID_SUBTRACTION_PAIRS[current]:
                    return (False, f"Invalid subtraction pair: '{current}{next_char}'. {current} can only precede {', '.join(self.VALID_SUBTRACTION_PAIRS[current])}")
        
        return (True, "")
    
    def to_integer_safe(self, s: str) -> Tuple[Optional[int], str]:
        """
        Safely convert an Alien Numeral string to integer with validation.
        
        This method validates the numeral before conversion to ensure it follows
        proper formation rules.
        
        Args:
            s (str): The Alien Numeral string to convert.
        
        Returns:
            Tuple[Optional[int], str]: (result, message)
                - (integer_value, "") if successful
                - (None, error_message) if validation fails
        
        Example:
            >>> converter = AlienNumeralConverter()
            >>> converter.to_integer_safe("AAA")
            (3, '')
            >>> converter.to_integer_safe("AAAA")
            (None, "Symbol 'A' repeats more than 3 times consecutively...")
        """
        is_valid, error_msg = self.is_valid_numeral(s)
        
        if not is_valid:
            return (None, error_msg)
        
        try:
            result = self.to_integer(s)
            return (result, "")
        except KeyError as e:
            return (None, f"Invalid symbol encountered: {e}")
    
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
    
    # Validation examples
    print("VALIDATION EXAMPLES:")
    print("-" * 60)
    print("Testing proper numeral formation rules...")
    print()
    
    validation_examples = [
        ("AAA", "Valid: 3 A's allowed"),
        ("AAAA", "Invalid: Use AB for 4, not AAAA"),
        ("AB", "Valid: Subtraction case = 4"),
        ("AL", "Invalid: A can only precede B or Z"),
        ("ZZZ", "Valid: 3 Z's allowed"),
        ("ZZZZ", "Invalid: Use ZL for 40, not ZZZZ"),
        ("BB", "Invalid: B cannot repeat"),
    ]
    
    for numeral, description in validation_examples:
        result, error = converter.to_integer_safe(numeral)
        if result is not None:
            print(f"✓ {numeral:10} = {result:4} | {description}")
        else:
            print(f"✗ {numeral:10}        | {description}")
    
    print("-" * 60)
    print()
    
    # Interactive section with validation
    print("Try your own conversions (press Ctrl+C to exit):")
    print("Note: The app validates proper numeral formation (e.g., AAAA is invalid, use AB)")
    print()
    try:
        while True:
            user_input = input("Enter Alien Numeral: ").strip().upper()
            if not user_input:
                continue
            
            # Use safe conversion with validation
            result, error_msg = converter.to_integer_safe(user_input)
            
            if result is not None:
                print(f"✓ Result: {result}")
            else:
                print(f"✗ Invalid: {error_msg}")
            print()
    except (KeyboardInterrupt, EOFError):
        print("\n\nThank you for using Alien Numerals Calculator!")


if __name__ == "__main__":
    main()
