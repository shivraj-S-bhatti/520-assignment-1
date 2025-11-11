def is_palindrome_sentence(s: str) -> bool:
    """
    Checks if the string is a palindrome ignoring non-alphanumeric characters and case.
    Returns True if the filtered string reads the same forward and backward, else False.
    """
    filtered = [c.lower() for c in s if c.isalnum()]
    return filtered == filtered[::-1]