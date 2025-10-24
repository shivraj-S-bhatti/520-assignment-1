
def run_tests(impl):
    failures = []
    cases = [
        ('a,b,c', ['a','b','c']),
        ('a,"b,c",d', ['a','b,c','d']),
        ('"a""b",c', ['a"b','c']),
        ('', ['']),
        ('"","",', ['', '', '']),
        ('" spaced ",x', [' spaced ', 'x'])
    ]
    for line, exp in cases:
        try:
            got = impl(line)
            if got != exp:
                failures.append(f"{line!r} -> {got!r}, expected {exp!r}")
        except Exception as e:
            failures.append(f"{line!r} raised {e.__class__.__name__}: {e}")
    return (len(failures) == 0, failures)
