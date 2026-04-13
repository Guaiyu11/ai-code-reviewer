#!/usr/bin/env python3
"""
QR Code Generator - Generate QR codes from text or URLs.
Usage: python qrcode-gen.py <text> [--output qr.png] [--size 10]
"""

import sys

def generate_qr(text, size=10):
    """Generate QR code (requires qrcode library)."""
    try:
        import qrcode
        from io import BytesIO
        img = qrcode.make(text, box_size=size)
        return img, None
    except ImportError:
        return None, "qrcode library not installed (pip install qrcode[pil])"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python qrcode-gen.py <text|url> [--output FILE.png] [--size N]")
        sys.exit(1)
    
    text = sys.argv[1]
    output = None
    size = 10
    
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
        elif arg == '--size' and i + 1 < len(sys.argv):
            size = int(sys.argv[i + 1])
    
    img, error = generate_qr(text, size)
    
    if error:
        print(error)
        sys.exit(1)
    
    if output:
        img.save(output)
        print(f"Saved: {output}")
    else:
        img.show()
