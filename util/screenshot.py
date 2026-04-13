#!/usr/bin/env python3
"""
Screenshot - Take a screenshot (requires PIL).
Usage: python screenshot.py [--output screenshot.png] [--region x y w h]
"""

import sys
import os

def take_screenshot(region=None, output='screenshot.png'):
    """Take screenshot using PIL/Pillow."""
    try:
        from PIL import ImageGrab
    except ImportError:
        return None, "PIL not available. Install: pip install Pillow"
    
    try:
        if region:
            x, y, w, h = region
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        else:
            img = ImageGrab.grab()
        
        img.save(output)
        return output, None
    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    output = 'screenshot.png'
    region = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
        elif arg == '--region' and i + 4 < len(sys.argv):
            x, y, w, h = map(int, sys.argv[i + 1:i + 5])
            region = (x, y, w, h)
    
    result, error = take_screenshot(region, output)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    else:
        print(f"Saved: {result}")
