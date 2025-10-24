
def run_tests(impl):
    failures = []
    def approx(a,b,eps=1e-9): return abs(a-b) <= eps

    try:
        if not approx(impl([1,0,0],[1,0,0]), 1.0):
            failures.append("identical vectors not 1.0")
    except Exception as e:
        failures.append(f"identical raised {e.__class__.__name__}: {e}")

    try:
        if not approx(impl([1,1],[0,0]), 0.0):
            failures.append("zero vector should yield 0.0")
    except Exception as e:
        failures.append(f"zero vector raised {e.__class__.__name__}: {e}")

    try:
        val = impl([1,2,3],[4,5,6])
        import math
        expected = (1*4+2*5+3*6)/(math.sqrt(1+4+9)*math.sqrt(16+25+36))
        if abs(val - expected) > 1e-9:
            failures.append("3D cosine incorrect")
    except Exception as e:
        failures.append(f"3D raised {e.__class__.__name__}: {e}")

    try:
        impl([1,2],[1,2,3])
        failures.append("Expected ValueError for length mismatch")
    except ValueError:
        pass
    except Exception as e:
        failures.append(f"len mismatch raised {e.__class__.__name__}, expected ValueError")

    return (len(failures) == 0, failures)
