BOX_CHARS = '┌┬┐', '├┼┤', '└┴┘'
HORIZONTAL = '─'

def table_maker(expressions, *rows):
    """Generates an aligned table. Modified from https://github.com/salt-die/tables
    """
    lengths = tuple(map(len, expressions))

    # Pad the length of items in each column
    rows = [[f'{item:^{length}}' for item, length in zip(row, lengths)] for row in rows]
    rows.insert(0, list(expressions))

    # Make separators
    horizontals = tuple(HORIZONTAL * (length + 2) for length in lengths)
    top, title, bottom = (f'{l}{m.join(horizontals)}{r}' for l, m, r in BOX_CHARS)

    table = [f'│ {" │ ".join(row)} │' for row in rows]
    table.insert(0, top)
    table.insert(2, title)
    table.append(bottom)
    table = '\n'.join(table)
    return table