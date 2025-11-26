def int_to_roman(n: int) -> str:
    """Convert an integer to Roman numerals (1..3999)."""
    if not 1 <= n <= 3999:
        raise ValueError("Input must be between 1 and 3999")

    roman_map = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
        50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }

    result = ""
    values = sorted(roman_map.keys(), reverse=True)

    for value in values:
        while n >= value:
            result += roman_map[value]
            n -= value

    return result