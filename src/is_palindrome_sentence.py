def is_palindrome_sentence(s: str) -> bool:
    """
    Check if a string is a palindrome ignoring non-alphanumeric characters and case.

    Return True if s reads the same forward and backward considering only [A-Za-z0-9], case-insensitive; else False.
    """
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True