#!/usr/bin/env python3
"""
Emoji Gen - Generate emoji from text keywords.
Usage: python emoji-gen.py <keyword>
"""

import sys

EMOJI_MAP = {
    'smile': '😄', 'laugh': '😂', 'cry': '😢', 'angry': '😠', 'love': '❤️',
    'heart': '💕', 'star': '⭐', 'fire': '🔥', 'rocket': '🚀', 'check': '✅',
    'cross': '❌', 'warning': '⚠️', 'info': 'ℹ️', 'question': '❓', 'exclaim': '❗',
    'sun': '☀️', 'moon': '🌙', 'cloud': '☁️', 'rain': '🌧️', 'snow': '❄️',
    'cat': '🐱', 'dog': '🐕', 'bird': '🐦', 'fish': '🐟', 'tree': '🌳',
    'flower': '🌸', 'apple': '🍎', 'banana': '🍌', 'coffee': '☕', 'beer': '🍺',
    'wine': '🍷', 'pizza': '🍕', 'burger': '🍔', 'fries': '🍟', 'sushi': '🍣',
    'money': '💰', 'dollar': '💵', 'clock': '⏰', 'calendar': '📅', 'phone': '📱',
    'computer': '💻', 'key': '🔑', 'lock': '🔒', 'bulb': '💡', 'wrench': '🔧',
    'hammer': '🔨', 'book': '📚', 'pen': '🖊️', 'paper': '📄', 'folder': '📁',
    'car': '🚗', 'bike': '🚲', 'plane': '✈️', 'train': '🚂', 'boat': '⛵',
    'house': '🏠', 'building': '🏢', 'hospital': '🏥', 'school': '🏫', 'hotel': '🏨',
    'flag': '🚩', 'trophy': '🏆', 'medal': '🏅', 'target': '🎯', 'game': '🎮',
    'music': '🎵', 'movie': '🎬', 'camera': '📷', 'gift': '🎁', 'balloon': '🎈',
    'sunrise': '🌅', 'sunset': '🌄', 'mountain': '⛰️', 'beach': '🏖️', 'desert': '🏜️',
}

def best_match(keyword):
    """Find best emoji match for keyword."""
    keyword = keyword.lower()
    
    if keyword in EMOJI_MAP:
        return EMOJI_MAP[keyword]
    
    for word, emoji in EMOJI_MAP.items():
        if keyword in word or word in keyword:
            return emoji
    
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python emoji-gen.py <keyword>")
        print("\nKeywords:", ', '.join(sorted(EMOJI_MAP.keys())))
        sys.exit(1)
    
    keyword = sys.argv[1]
    emoji = best_match(keyword)
    
    if emoji:
        print(emoji)
    else:
        print(f"No emoji found for '{keyword}'")
        # Suggest similar
        similar = [k for k in EMOJI_MAP.keys() if keyword[0] == k[0]]
        if similar:
            print(f"Similar: {', '.join(similar[:5])}")
