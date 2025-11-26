def min_window_substring(s: str, t: str) -> str:
    """
    Finds the minimum window substring in s containing all characters of t.
    """
    if not t or not s:
        return ""

    t_freq = {}
    for char in t:
        t_freq[char] = t_freq.get(char, 0) + 1

    window_freq = {}
    have = 0  # Number of characters from t satisfied in the window
    need = len(t_freq)  # Number of distinct characters in t

    l = 0
    res = ""  # Minimum window found so far
    res_len = float('inf')

    for r in range(len(s)):
        char = s[r]
        window_freq[char] = window_freq.get(char, 0) + 1

        if char in t_freq and window_freq[char] == t_freq[char]:
            have += 1

        while have == need:
            # Update result
            if (r - l + 1) < res_len:
                res = s[l:r + 1]
                res_len = (r - l + 1)

            # Shrink window
            window_freq[s[l]] -= 1
            if s[l] in t_freq and window_freq[s[l]] < t_freq[s[l]]:
                have -= 1
            l += 1

    return res