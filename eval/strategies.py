
import re, pathlib

def extract_python_code(text: str) -> str:
    """
    Extract the first Python code block from a response; if none, return the whole text.
    """
    fence = re.search(r"```(?:python)?\s*(.+?)```", text, re.DOTALL|re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    return text.strip()

def build_problem_spec(md_path: str) -> str:
    return pathlib.Path(md_path).read_text()

def fill_template(tmpl: str, problem_spec: str, **kwargs) -> str:
    out = tmpl.replace("{PROBLEM_SPEC}", problem_spec)
    for k,v in kwargs.items():
        out = out.replace("{"+k+"}", v)
    return out
