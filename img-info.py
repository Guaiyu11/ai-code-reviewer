#!/usr/bin/env python3
"""
Image Info - Show image dimensions, format, EXIF data.
Usage: python img-info.py <image.jpg> [--exif]
"""

import sys
import os

def get_image_info(filepath):
    """Get image information."""
    try:
        from PIL import Image
        img = Image.open(filepath)
        info = {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
        }
        
        # EXIF
        exif = None
        if hasattr(img, '_getexif') and img._getexif():
            exif = img._getexif()
        
        return info, exif
    except ImportError:
        return None, None, "PIL not installed (pip install Pillow)"
    except Exception as e:
        return None, None, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python img-info.py <image.jpg> [--exif]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    info, exif, error = get_image_info(filepath)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    print(f"=== Image: {os.path.basename(filepath)} ===\n")
    print(f"Format:    {info['format']}")
    print(f"Mode:      {info['mode']}")
    print(f"Size:      {info['size']}")
    print(f"Dimensions: {info['width']} x {info['height']} pixels")
    
    if exif and '--exif' in sys.argv:
        print("\nEXIF Data:")
        for tag_id, value in exif.items():
            print(f"  {tag_id}: {value}")
