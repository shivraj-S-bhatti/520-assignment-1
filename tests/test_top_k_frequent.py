
def run_tests(impl):
    failures = []

    def check(nums, k, expected):
        try:
            got = impl(nums, k)
            if got != expected:
                failures.append(f"{nums!r}, k={k} -> {got!r}, expected {expected!r}")
        except Exception as e:
            failures.append(f"{nums!r}, k={k} raised {e.__class__.__name__}: {e}")

    check([1,1,1,2,2,3], 2, [1,2])
    check([4,4,4,5,5,6], 1, [4])
    check([3,3,2,2,1], 2, [2,3])  # tie -> smaller first
    check([1], 1, [1])

    # Errors
    try:
        impl([1,2,3], 0)
        failures.append("Expected ValueError for k=0")
    except ValueError:
        pass
    try:
        impl([1,2,3], 4)
        failures.append("Expected ValueError for k>unique")
    except ValueError:
        pass

    return (len(failures) == 0, failures)
