
def run_tests(impl):
    failures = []
    cases = [
        (["2","1","+","3","*"], 9),
        (["4","13","5","/","+"], 6),
        (["10","6","9","3","+","-11","*","/","*","17","+","5","+"], 22),
        (["3","-4","/"], -0)  # trunc toward zero -> 0
    ]
    for tokens, exp in cases:
        try:
            got = impl(tokens)
            if got != exp:
                failures.append(f"{tokens} -> {got!r}, expected {exp!r}")
        except Exception as e:
            failures.append(f"{tokens} raised {e.__class__.__name__}: {e}")

    # Error: div by zero
    try:
        impl(["1","0","/"])
        failures.append("Expected ValueError for division by zero")
    except ValueError:
        pass
    except Exception as e:
        failures.append(f"div by zero raised {e.__class__.__name__}, expected ValueError")

    return (len(failures) == 0, failures)
