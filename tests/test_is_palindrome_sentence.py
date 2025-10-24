
def run_tests(impl):
    failures = []
    cases = [
        ("A man, a plan, a canal: Panama", True),
        ("No lemon, no melon!", True),
        ("race a car", False),
        ("", True),
        ("!!!!", True),
        ("ab@#a", True),
        ("Aa", True)
    ]
    for s, exp in cases:
        try:
            got = impl(s)
            if got != exp:
                failures.append(f"{s!r} -> {got!r}, expected {exp!r}")
        except Exception as e:
            failures.append(f"{s!r} raised {e.__class__.__name__}: {e}")
    return (len(failures) == 0, failures)
