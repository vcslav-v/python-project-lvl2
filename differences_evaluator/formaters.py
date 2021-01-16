"""Formaters."""


def stylish(diff: dict) -> str:
    """Format diff data dict.
     - deleted key: value
     + added key: value
       unchanged key: value

    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """

    def _get_sign(diff_item):
        if diff_item['diff'] == 'added':
            return '+'
        elif diff_item['diff'] == 'removed':
            return '-'
        elif diff_item['diff'] == 'no change':
            return ' '

    def _get_output_stylish_format(value):
        if value is False:
            return 'false'
        elif value is True:
            return 'true'
        elif value is None:
            return 'null'
        else:
            return value

    def _get_stylish_node_rows(node, offset=3, force_sign=None):
        node_rows = []
        spaces = ' ' * offset
        for leaf in node['leafs']:
            sign = _get_sign(leaf)
            node_rows.append(
                '{spaces} {sign} {key}: {value}'.format(
                    spaces=spaces,
                    sign=force_sign or _get_sign(leaf),
                    key=leaf['key'],
                    value=_get_output_stylish_format(leaf['value'])
                )
            )

        if node['children']:
            for child in node['children']:
                sign = force_sign or _get_sign(child)
                node_rows.append(
                    '{spaces} {sign} {node}: '.format(
                        sign=sign,
                        spaces=spaces,
                        node=child['node']
                    ) + '{'
                )
                if force_sign or child['diff'] != 'no change':
                    node_rows.extend(
                        _get_stylish_node_rows(child, offset+3, ' ')
                    )
                else:
                    node_rows.extend(_get_stylish_node_rows(child, offset+3))
        node_rows.append(spaces + '}')
        return node_rows

    output = ['{']
    output.extend(_get_stylish_node_rows(diff))
    output[-1] = '}'
    return '\n'.join(output)
