"""Stylish formater."""
from typing import Any, List

STATUS_ADDED = 'added'
STATUS_REMOVED = 'removed'
STATUS_UPDATED = 'updated'
STATUS_NO_CHANGE = 'no change'
STATUS_NODE = 'node'

START_OFFSET = 1
ADD_OFFSET = 4

SIGN = {
    STATUS_ADDED: '+',
    STATUS_REMOVED: '-',
    STATUS_NO_CHANGE: ' ',
    STATUS_NODE: ' '
}

VALUE_FORMAT = {
    False: 'false',
    True: 'true',
    None: 'null'
}


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

    output = ['{']
    output.extend(get_node_rows(diff))
    output[-1] = '}'
    return '\n'.join(output)


def get_node_rows(
    node: dict,
    offset: int = START_OFFSET,
    force_sign: str = ''
) -> List[str]:
    """Formats the diff to a list of strings stylish."""

    node_rows = []
    spaces = ' ' * offset

    for value in node['values']:
        key, status = value['key'], value['diff']
        if status in SIGN:
            sign = SIGN[status]

        if status == STATUS_NODE:
            node_rows.append(
                '{spaces} {sign} {node}: '.format(
                    sign=sign,
                    spaces=spaces,
                    node=key
                ) + '{'
            )
            node_rows.extend(
                get_node_rows(
                    value, offset + ADD_OFFSET
                )
            )
        elif status == STATUS_UPDATED:
            node_rows.append(
                get_leaf(
                    spaces,
                    SIGN[STATUS_REMOVED],
                    key,
                    value['old_values'],
                    offset
                )
            )
            node_rows.append(
                get_leaf(
                    spaces,
                    SIGN[STATUS_ADDED],
                    key,
                    value['new_values'],
                    offset
                )
            )
        else:
            node_rows.append(
                get_leaf(
                    spaces,
                    sign,
                    key,
                    value['values'],
                    offset
                )
            )

    end_spases = ' ' * (offset - START_OFFSET)
    node_rows.append(end_spases + '}')
    return node_rows


def get_output_format(value: Any, offset: int) -> str:
    """Returns the values to the form stylish."""
    if isinstance(value, dict):
        new_value = get_dict_format(value, offset)
    elif value in VALUE_FORMAT:
        new_value = VALUE_FORMAT[value]
    else:
        new_value = value
    return new_value


def get_dict_format(value: dict, offset: int) -> str:
    """To handle values of type dictionary."""
    rows = ['{']
    spaces = ' ' * offset
    for key in value.keys():
        rows.append('{spaces}   {key}: {value}'.format(
            spaces=spaces,
            key=key,
            value=get_output_format(
                value[key],
                offset + ADD_OFFSET
            )
        ))
    end_spases = ' ' * (offset - START_OFFSET)
    rows.append(end_spases + '}')
    return '\n'.join(rows)


def get_leaf(
    spaces: str,
    sign: str,
    key: str,
    value: Any,
    offset: int
) -> str:
    """Formats the sheet into a line of stylish."""
    leaf = '{spaces} {sign} {key}: {value}'.format(
                    spaces=spaces,
                    sign=sign,
                    key=key,
                    value=get_output_format(
                        value,
                        offset + ADD_OFFSET
                    )
                )
    return leaf
