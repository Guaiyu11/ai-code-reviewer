#!/usr/bin/env python3
"""颜色格式转换：HEX <-> RGB <-> HSL。

Usage:
    python color-rgb.py "#FF5733"
    python color-rgb.py "rgb(255, 87, 51)"
    python color-rgb.py --random
"""

import argparse
import colorsys
import random
import sys
import re


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h*360), round(s*100), round(l*100)


def main():
    parser = argparse.ArgumentParser(description="颜色格式转换")
    parser.add_argument("color", nargs="?", help="颜色值（HEX 或 RGB）")
    parser.add_argument("--random", action="store_true", help="随机颜色")
    args = parser.parse_args()

    if args.random:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    elif args.color:
        c = args.color.strip()
        if c.startswith("rgb"):
            m = re.findall(r"\d+", c)
            if len(m) == 3:
                r, g, b = map(int, m)
            else:
                print("RGB 格式错误，应为 rgb(r,g,b)", file=sys.stderr)
                return
        elif c.startswith("#"):
            r, g, b = hex_to_rgb(c)
        else:
            r, g, b = hex_to_rgb(c)
    else:
        parser.print_help()
        return

    h, s, l = rgb_to_hsl(r, g, b)
    hex_val = rgb_to_hex(r, g, b)

    print(f"HEX:  {hex_val}")
    print(f"RGB:  rgb({r}, {g}, {b})")
    print(f"HSL:  hsl({h}, {s}%, {l}%)")


if __name__ == "__main__":
    main()
