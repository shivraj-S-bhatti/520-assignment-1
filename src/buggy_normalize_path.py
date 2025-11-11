def normalize_path(path: str) -> str:
    """Normalizes a Unix-style path by resolving '.', '..' and redundant slashes.
    
    BUG: Removed trailing slash preservation for directory-like paths.
    """
    parts = path.split('/')
    stack = []
    is_absolute = path.startswith('/')

    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == '..':
            if stack and (is_absolute or stack[-1] != '..'):
                stack.pop()
            elif is_absolute:
                pass
            else:
                stack.append(part)
        else:
            stack.append(part)

    normalized_path = '/' + '/'.join(stack) if is_absolute else '/'.join(stack)

    # BUG: Removed trailing slash preservation - always removes trailing slash
    if normalized_path == '/' and not path.endswith('/'):
        return '/'
    elif normalized_path != '/' and normalized_path.endswith('/'):
        normalized_path = normalized_path[:-1]  # Always remove trailing slash

    return normalized_path if normalized_path else '.'

