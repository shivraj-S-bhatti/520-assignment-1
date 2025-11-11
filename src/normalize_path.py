def normalize_path(path: str) -> str:
    """Normalizes a Unix-style path by resolving '.', '..' and redundant slashes."""
    parts = path.split('/')
    stack = []
    is_absolute = path.startswith('/')

    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == '..':
            if stack and (is_absolute or stack[-1] != '..'): #Don't pop if at root or already preserving leading '..'
                stack.pop()
            elif is_absolute:  #Handle absolute path at root. Don't go above.
                pass # stay at root
            else:
                stack.append(part) #preserve leading ".."
        else:
            stack.append(part)

    normalized_path = '/' + '/'.join(stack) if is_absolute else '/'.join(stack)

    # Handle trailing slash:  Only keep for root
    if normalized_path == '/' and not path.endswith('/'): #special case for a/../ -> '' or a/../b -> b instead of b/
        return '/'
    elif normalized_path != '/' and normalized_path.endswith('/'):
        normalized_path = normalized_path[:-1] # remove any other trailing slash

    return normalized_path if normalized_path else '.'  #Empty path resolves to current directory