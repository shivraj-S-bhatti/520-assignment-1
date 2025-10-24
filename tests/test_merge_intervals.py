
def run_tests(impl):
    failures = []
    def check(inp, expected):
        try:
            got = impl(inp)
            if got != expected:
                failures.append(f"{inp!r} -> {got!r}, expected {expected!r}")
        except Exception as e:
            failures.append(f"{inp!r} raised {e.__class__.__name__}: {e}")

    check([(1,3),(2,6),(8,10),(15,18)], [(1,6),(8,10),(15,18)])
    check([(1,4),(4,5)], [(1,5)])
    check([], [])
    check([(1,1)], [(1,1)])
    check([(5,7),(1,2),(2,3)], [(1,3),(5,7)])
    check([(1,5),(2,3)], [(1,5)])

    return (len(failures) == 0, failures)
