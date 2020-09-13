BOX_CHARS = '┌┬┐', '├┼┤', '└┴┘'
HORIZONTAL = '─'

def table_maker(expressions, *values):
    """Generates an aligned table. Modified from https://github.com/salt-die/Table-Maker"""
    lengths = tuple(map(len, expressions))
    rows = list(values)

    # Pad the length of items in each column
    for i, row in enumerate(rows):
        for j, (item, length) in enumerate(zip(row, lengths)):
            rows[i][j] = f'{item:^{length}}'

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