def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    # Check if the cleaned string is equal to its reverse
    return cleaned == cleaned[::-1]

# Example usage
if __name__ == "__main__":
    test_string = "racecar"
    print(f"'{test_string}' is a palindrome: {is_palindrome(test_string)}")


'''This can also work for simple strings, but it will not work for strings with special characters or spaces.'''
# def is_palindrome(s):
#     return s == s[::-1]

# print(is_palindrome("racecar"))