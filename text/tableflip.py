#!/usr/bin/env python3
"""
Tableflip - Generate text emoticons like (╯°□°）╯︵ ┻━┻
Usage: python tableflip.py [text]
"""

import sys

TABLEFLIPS = [
    '(╯°□°）╯︵ ┻━┻',
    '(ノಠ益ಠ)ノ彡┻━┻',
    '┻━┻ ︵ヽ(`Д´)ノ︵ ┻━┻',
    '(ノಠ益ಠ)ノ彡︵ table',
    '┬─┬ノ( º _ ºノ) ︵ ┻━┻',
    '(╯°□°)╯︵ ┻━━━━┻',
    '(ノಠ益ಠ)ノ彡┻━━━┻',
    '┻━┻︵└(՞▃՞└)',
]

def flip(text='┻━┻', emoticon='(╯°□°）╯'):
    """Generate tableflip."""
    return f"{emoticon}︵{text}"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(flip(sys.argv[1]))
    else:
        for tf in TABLEFLIPS:
            print(tf)
