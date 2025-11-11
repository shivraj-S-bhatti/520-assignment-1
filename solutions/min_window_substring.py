def min_window_substring(s: str, t: str) -> str:
    from collections import defaultdict

    if not s or not t or len(t) > len(s):
        return ""

    target_counts = defaultdict(int)
    for char in t:
        target_counts[char] += 1
    required = len(target_counts)

    window_counts = defaultdict(int)
    formed = 0
    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        if char in target_counts:
            window_counts[char] += 1
            if window_counts[char] == target_counts[char]:
                formed += 1

        while formed == required and left <= right:
            current_len = right - left + 1
            if current_len < min_len:
                min_len = current_len
                result = s[left:right+1]

            left_char = s[left]
            if left_char in target_counts:
                window_counts[left_char] -= 1
                if window_counts[left_char] < target_counts[left_char]:
                    formed -= 1
            left += 1

    return result