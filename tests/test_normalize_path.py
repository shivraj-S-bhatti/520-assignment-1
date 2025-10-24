
def run_tests(impl):
    failures = []

    def check(inp, expected):
        try:
            got = impl(inp)
            if got != expected:
                failures.append(f"{inp!r} -> {got!r}, expected {expected!r}")
        except Exception as e:
            failures.append(f"{inp!r} raised {e.__class__.__name__}: {e}")

    # Happy paths
    check('/a//b/./c/../', '/a/b/')
    check('a/b/../../c', 'c')
    check('../../x', '../../x')
    check('/', '/')
    check('/././', '/')
    check('/../', '/')
    check('a//b////c', 'a/b/c')
    check('a/./b/./c/', 'a/b/c/')
    check('a/../../..', '../../')
    check('a/../..', '../')
    check('', '')

    return (len(failures) == 0, failures)
