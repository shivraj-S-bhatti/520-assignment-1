
def run_tests(impl):
    failures = []
    known = {
        1:'I', 4:'IV', 9:'IX', 58:'LVIII', 1994:'MCMXCIV', 3999:'MMMCMXCIX',
        44:'XLIV', 945:'CMXLV', 3888:'MMMDCCCLXXXVIII'
    }
    for n, r in known.items():
        try:
            got = impl(n)
            if got != r:
                failures.append(f"{n} -> {got!r}, expected {r!r}")
        except Exception as e:
            failures.append(f"{n} raised {e.__class__.__name__}: {e}")

    # Edge cases
    for bad in [0, -1, 4000, 10000]:
        try:
            impl(bad)
            failures.append(f"Expected ValueError for {bad}")
        except ValueError:
            pass
        except Exception as e:
            failures.append(f"{bad} raised {e.__class__.__name__}, expected ValueError")

    return (len(failures) == 0, failures)
