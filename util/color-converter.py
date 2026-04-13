#!/usr/bin/env python3
"""
Color Converter - Convert between HEX, RGB, HSL, HSV color formats.
Usage: python color-converter.py <color> [--format FMT]
Examples:
  python color-converter.py "#FF5733"
  python color-converter.py "rgb(255, 87, 51)"
  python color-converter.py "hsl(11, 100%, 60%)"
"""

import sys
import re

def hex_to_rgb(h):
    """HEX to RGB tuple."""
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """RGB to HEX string."""
    return '#{:02X}{:02X}{:02X}'.format(int(r), int(g), int(b))

def rgb_to_hsv(r, g, b):
    """RGB to HSV tuple."""
    r, g, b = r/255, g/255, b/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    else:
        h = (60 * ((r-g)/df) + 240) % 360
    
    s = 0 if mx == 0 else df/mx
    v = mx
    
    return h, s*100, v*100

def hsv_to_rgb(h, s, v):
    """HSV to RGB tuple."""
    h, s, v = h/360, s/100, v/100
    if s == 0:
        return v*255, v*255, v*255
    
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    i %= 6
    if i == 0: return v*255, t*255, p*255
    if i == 1: return q*255, v*255, p*255
    if i == 2: return p*255, v*255, t*255
    if i == 3: return p*255, q*255, v*255
    if i == 4: return t*255, p*255, v*255
    return v*255, p*255, q*255

def rgb_to_hsl(r, g, b):
    """RGB to HSL tuple."""
    r, g, b = r/255, g/255, b/255
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn) / 2
    
    if mx == mn:
        return 0, 0, l*100
    
    df = mx - mn
    s = df / (2 - mx - mn) if (mx + mn) > 1 else df / (mx + mn)
    
    if mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    else:
        h = (60 * ((r-g)/df) + 240) % 360
    
    return h, s*100, l*100

def parse_color(input_str):
    """Parse color from various formats."""
    input_str = input_str.strip()
    
    # HEX
    if re.match(r'^#?[0-9A-Fa-f]{6}$', input_str) or re.match(r'^#?[0-9A-Fa-f]{3}$', input_str):
        return hex_to_rgb(input_str), 'hex'
    
    # RGB
    match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', input_str, re.I)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3))), 'rgb'
    
    # HSL
    match = re.match(r'hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', input_str, re.I)
    if match:
        h, s, l = float(match.group(1)), float(match.group(2)), float(match.group(3))
        r, g, b = hsv_to_rgb(h, 100, 100)  # approximate
        return (r/255*100, g/255*100, b/255*100), 'hsl'
    
    return None, None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python color-converter.py <color>")
        print("Formats: #RRGGBB, rgb(R,G,B), hsl(H,S%,L%)")
        sys.exit(1)
    
    color_str = sys.argv[1]
    
    rgb, fmt = parse_color(color_str)
    
    if rgb is None:
        print(f"Could not parse color: {color_str}")
        sys.exit(1)
    
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    
    h, s, v = rgb_to_hsv(r, g, b)
    h2, s2, l = rgb_to_hsl(r, g, b)
    
    print("=== Color Converter ===\n")
    print(f"Input:  {color_str}")
    print()
    print(f"HEX:    {rgb_to_hex(r, g, b)}")
    print(f"RGB:    rgb({r}, {g}, {b})")
    print(f"HSV:    hsv({h:.1f}, {s:.1f}%, {v:.1f}%)")
    print(f"HSL:    hsl({h2:.1f}, {s2:.1f}%, {l:.1f}%)")
    print(f"HEX3:   #{rgb_to_hex(r,g,b).lstrip('#')[0]*3}{rgb_to_hex(r,g,b).lstrip('#')[1]*3}{rgb_to_hex(r,g,b).lstrip('#')[2]*3}" if len(rgb_to_hex(r,g,b).lstrip('#')) == 6 else "")
