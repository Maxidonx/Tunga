# Find the First Non-Repeating Character

# Given a string, find the first non-repeating character in it and return its index. If it doesn't exist, return -1. # Note: all the input strings are already lowercase.

from collections import Counter
def first_non_repeating_character(s):
    count = Counter(s)
    for char in s:
        if count[char] == 1:
            return char
        return None
    
print(first_non_repeating_character("leetcode")) # l