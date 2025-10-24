
def run_tests(impl):
    failures = []
    cases = [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("ab", "b", "b"),
        ("ab", "A", ""),
        ("", "a", ""),
        ("aa", "aa", "aa"),
    ]
    for s,t,exp in cases:
        try:
            got = impl(s,t)
            if got != exp:
                failures.append(f"{s!r},{t!r} -> {got!r}, expected {exp!r}")
        except Exception as e:
            failures.append(f"{s!r},{t!r} raised {e.__class__.__name__}: {e}")
    return (len(failures) == 0, failures)
