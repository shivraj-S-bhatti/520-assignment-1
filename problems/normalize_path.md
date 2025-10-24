# Normalize a Unix-style path

**Function signature:**

```python
def normalize_path(path: str) -> str:
```

**Task:** Given a Unix-style path string, return its normalized form by resolving '.', '..' and redundant slashes. Preserve absolute vs relative semantics.

**Details & Constraints:**

Rules:
- Multiple '/' collapse to a single '/'.
- '.' means current directory, skip it.
- '..' pops one segment unless at root for absolute paths (then stay at '/'). For relative paths, leading '..' should be preserved.
- Preserve a trailing slash only if the normalized path is root '/'.
Examples:
- '/a//b/./c/../' -> '/a/b/'
- 'a/b/../../c' -> 'c'
- '../../x' -> '../../x'
