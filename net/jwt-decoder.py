#!/usr/bin/env python3
"""
JWT Decoder - Decode and inspect JWT tokens without verification.
Usage: python jwt-decoder.py <token>
"""

import sys
import base64
import json
import hmac
import hashlib
import time

def decode_base64url(data):
    """Decode base64url encoded data with padding."""
    # Add padding if needed
    missing = 4 - len(data) % 4
    if missing != 4:
        data += '=' * missing
    
    # Convert base64url to base64
    data = data.replace('-', '+').replace('_', '/')
    
    try:
        return base64.b64decode(data)
    except Exception:
        return None


def decode_jwt(token):
    """Decode a JWT token without verification."""
    parts = token.strip().split('.')
    
    if len(parts) != 3:
        return None, "Invalid JWT format - must have 3 parts (header.payload.signature)"
    
    header_b64, payload_b64, signature_b64 = parts
    
    # Decode header
    header_data = decode_base64url(header_b64)
    if not header_data:
        return None, "Failed to decode header"
    
    try:
        header = json.loads(header_data)
    except json.JSONDecodeError:
        return None, "Header is not valid JSON"
    
    # Decode payload
    payload_data = decode_base64url(payload_b64)
    if not payload_data:
        return None, "Failed to decode payload"
    
    try:
        payload = json.loads(payload_data)
    except json.JSONDecodeError:
        return None, "Payload is not valid JSON"
    
    # Decode signature (just show as base64, don't verify)
    signature = decode_base64url(signature_b64)
    signature_hex = signature.hex() if signature else "invalid"
    
    return {
        'header': header,
        'payload': payload,
        'signature_hex': signature_hex,
        'raw': {
            'header_b64': header_b64,
            'payload_b64': payload_b64,
            'signature_b64': signature_b64,
        }
    }, None


def explain_claim(claim, value):
    """Explain JWT standard claims."""
    explanations = {
        'iss': ('Issuer', 'Who issued this token'),
        'sub': ('Subject', 'Who this token represents'),
        'aud': ('Audience', 'Who this token is intended for'),
        'exp': ('Expiration', 'When this token expires'),
        'nbf': ('Not Before', 'When this token becomes valid'),
        'iat': ('Issued At', 'When this token was issued'),
        'jti': ('JWT ID', 'Unique identifier for this token'),
    }
    
    if claim in explanations:
        name, desc = explanations[claim]
        
        # Format timestamps
        if claim in ('exp', 'nbf', 'iat'):
            try:
                dt = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(value))
                return f"{name}: {value} ({desc}) -> {dt}"
            except:
                pass
        
        return f"{name}: {value} ({desc})"
    
    return f"{claim}: {value}"


def check_token_expiry(payload):
    """Check if token is expired or about to expire."""
    now = time.time()
    
    issues = []
    
    if 'exp' in payload:
        exp = payload['exp']
        if exp < now:
            remaining = now - exp
            issues.append(f"EXPIRED {int(remaining)} seconds ago")
        elif exp < now + 300:
            remaining = exp - now
            issues.append(f"EXPIRING in {int(remaining)} seconds")
        else:
            remaining = exp - now
            issues.append(f"Valid for {int(remaining)} seconds ({int(remaining/3600)} hours)")
    
    if 'nbf' in payload:
        nbf = payload['nbf']
        if nbf > now:
            remaining = nbf - now
            issues.append(f"Not valid yet - starts in {int(remaining)} seconds")
    
    if 'iat' in payload:
        issued = payload['iat']
        age = now - issued
        issues.append(f"Token age: {int(age)} seconds ({int(age/3600)} hours)")
    
    return issues


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python jwt-decoder.py <token>")
        print("\nExamples:")
        print("  python jwt-decoder.py 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'")
        print("\nNote: This decoder does NOT verify signatures. Only decode - never trust unverified tokens!")
        sys.exit(1)
    
    token = sys.argv[1]
    
    result, error = decode_jwt(token)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    print("=== JWT Decoder ===\n")
    print("(Note: Signature NOT verified - only decoding)")
    
    # Header
    print("\n## Header")
    print(f"Algorithm: {result['header'].get('alg', 'N/A')}")
    print(f"Type:      {result['header'].get('typ', 'N/A')}")
    print(f"Full:      {json.dumps(result['header'], indent=2)}")
    
    # Payload
    print("\n## Payload (Claims)")
    for key, value in result['payload'].items():
        explanation = explain_claim(key, value)
        print(f"  {explanation}")
    
    # Issues
    print("\n## Status")
    issues = check_token_expiry(result['payload'])
    for issue in issues:
        status = "🔴" if "EXPIRED" in issue else ("🟡" if "EXPIRING" in issue else "🟢")
        print(f"  {status} {issue}")
    
    # Signature
    print(f"\n## Signature")
    print(f"  Hex: {result['signature_hex'][:64]}...")
    
    # Raw parts
    if '--raw' in sys.argv:
        print(f"\n## Raw Base64url")
        print(f"  Header:    {result['raw']['header_b64']}")
        print(f"  Payload:   {result['raw']['payload_b64']}")
        print(f"  Signature: {result['raw']['signature_b64']}")
