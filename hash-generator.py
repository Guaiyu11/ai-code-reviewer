#!/usr/bin/env python3
"""
Hash Generator - Generate various cryptographic hashes from files or strings.
Usage: python hash-generator.py <string|file> [--algo ALGO]
Supported: md5, sha1, sha256, sha512, blake2b, sha3_256
"""

import sys
import os
import hashlib

ALGOS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512,
    'blake2b': hashlib.blake2b,
    'sha3_256': hashlib.sha3_256,
}


def hash_string(s, algo='sha256'):
    """Hash a string."""
    h = ALGOS.get(algo, hashlib.sha256)()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def hash_file(path, algo='sha256'):
    """Hash a file."""
    h = ALGOS.get(algo, hashlib.sha256)()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None, str(e)


def verify_file(path, expected_hash, algo='sha256'):
    """Verify a file against an expected hash."""
    actual = hash_file(path, algo)
    if actual is None:
        return False, "Could not read file"
    
    match = actual.lower() == expected_hash.lower()
    return match, actual


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python hash-generator.py <string|file> [--algo ALGO] [--verify HASH]")
        print("\nAlgorithms:", ', '.join(ALGOS.keys()))
        print("\nExamples:")
        print("  python hash-generator.py 'hello world'")
        print("  python hash-generator.py 'hello' --algo md5")
        print("  python hash-generator.py myfile.zip --algo sha256")
        print("  python hash-generator.py myfile.zip --verify abc123... --algo sha256")
        sys.exit(1)
    
    target = sys.argv[1]
    algo = 'sha256'
    verify_hash = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--algo' and i + 1 < len(sys.argv):
            algo = sys.argv[i + 1].lower()
        if arg == '--verify' and i + 1 < len(sys.argv):
            verify_hash = sys.argv[i + 1].lower()
    
    if algo not in ALGOS:
        print(f"Unknown algorithm: {algo}")
        print(f"Supported: {', '.join(ALGOS.keys())}")
        sys.exit(1)
    
    if os.path.exists(target):
        # It's a file
        if verify_hash:
            match, result = verify_file(target, verify_hash, algo)
            print(f"File: {target}")
            print(f"Expected ({algo}): {verify_hash}")
            print(f"Actual   ({algo}): {result}")
            print(f"Match: {'✅ YES' if match else '❌ NO'}")
        else:
            result = hash_file(target, algo)
            print(f"{algo.upper()}: {result}  {target}")
            # Also show other common hashes
            for other_algo in ['md5', 'sha1']:
                if other_algo != algo:
                    h = hash_file(target, other_algo)
                    print(f"{other_algo.upper()}: {h}  {target}")
    else:
        # It's a string
        result = hash_string(target, algo)
        print(f"Input:   {target[:100]}{'...' if len(target) > 100 else ''}")
        print(f"Length:  {len(target)} characters")
        print(f"\n{algo.upper()}: {result}")
