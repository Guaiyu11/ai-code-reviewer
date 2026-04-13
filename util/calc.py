#!/usr/bin/env python3
"""
Calculator - Simple CLI calculator with basic math and conversions.
Usage: python calc.py <expression>
Examples:
  python calc.py "2 + 2"
  python calc.py "sqrt(16)"
  python calc.py "10 * 5 / 2"
  python calc.py "2^10"
  python calc.py "100 in binary"
  python calc.py "0xFF in decimal"
"""

import sys
import math

FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    'factorial': math.factorial,
    'gcd': math.gcd,
    'pi': math.pi,
    'e': math.e,
}

def eval_safe(expr):
    """Safely evaluate a mathematical expression."""
    # Replace common operators
    expr = expr.replace('^', '**')
    expr = expr.replace('ln(', 'log(')
    
    # Handle percentage
    import re
    expr = re.sub(r'(\d+)%', r'(\1/100)', expr)
    
    # Handle "X in Y" conversions
    conversion_match = re.match(r'(.+?)\s+in\s+(.+)', expr, re.IGNORECASE)
    if conversion_match:
        value_str = conversion_match.group(1).strip()
        target = conversion_match.group(2).strip().lower()
        
        # Try to parse the value
        try:
            value = float(eval(value_str, {"__builtins__": {}}, FUNCTIONS))
        except:
            return None, f"Could not parse value: {value_str}"
        
        return convert_units(value, target)
    
    # Simple eval with safe functions
    local_vars = FUNCTIONS.copy()
    try:
        result = eval(expr, {"__builtins__": {}}, local_vars)
        return result, None
    except Exception as e:
        return None, str(e)

def convert_units(value, target):
    """Convert units."""
    target = target.lower().strip()
    
    conversions = {
        'binary': lambda v: bin(int(v)),
        'hex': lambda v: hex(int(v)),
        'octal': lambda v: oct(int(v)),
        'decimal': lambda v: int(v),
        'base 2': lambda v: bin(int(v)),
        'base 16': lambda v: hex(int(v)),
        'base 8': lambda v: oct(int(v)),
        'radians': lambda v: math.radians(v),
        'degrees': lambda v: math.degrees(v),
    }
    
    if target in conversions:
        result = conversions[target](value)
        return result, None
    
    return None, f"Unknown conversion target: {target}"

def format_result(value):
    """Format the result for display."""
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        # Limit decimal places
        formatted = f"{value:.10f}".rstrip('0')
        return formatted
    return str(value)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python calc.py <expression>")
        print("\nExamples:")
        print("  2 + 2")
        print("  sqrt(16)")
        print("  10 * 5 / 2")
        print("  2^10")
        print("  255 in binary")
        print("  0xFF in decimal")
        print("  sin(30)")
        print("  50%")
        sys.exit(1)
    
    expr = ' '.join(sys.argv[1:])
    
    result, error = eval_safe(expr)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    print(f"{expr} = {format_result(result)}")
