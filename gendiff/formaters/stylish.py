"""Formaters."""
from gendiff.config import cfg


SIGN = {
    cfg['diff_status']['added']: cfg['format']['stylish']['sign']['added'],
    cfg['diff_status']['removed']: cfg['format']['stylish']['sign']['removed'],
    cfg['diff_status']['no_change']: (
        cfg['format']['stylish']['sign']['no_change']
    ),
    cfg['diff_status']['node']: cfg['format']['stylish']['sign']['node']
}

STYLISH_VALUE_FORMAT = {
    False: cfg['format']['stylish']['value_format']['false'],
    True: cfg['format']['stylish']['value_format']['true'],
    None: cfg['format']['stylish']['value_format']['none']
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
    output.extend(get_stylish_node_rows(diff))
    output[-1] = '}'
    return '\n'.join(output)


def get_stylish_node_rows(
    node,
    offset=cfg['format']['stylish']['start_offset'],
    force_sign=None
):
    node_rows = []
    spaces = ' ' * offset

    for value in node['value']:
        if value['diff'] in SIGN:
            sign = SIGN[value['diff']]

        if value['diff'] == cfg['diff_status']['node']:
            node_rows.append(
                '{spaces} {sign} {node}: '.format(
                    sign=sign,
                    spaces=spaces,
                    node=value['key']
                ) + '{'
            )
            node_rows.extend(
                get_stylish_node_rows(
                    value, offset + cfg['format']['stylish']['add_offset']
                )
            )
        elif value['diff'] == cfg['diff_status']['updated']:
            node_rows.append(
                get_leaf(
                    spaces,
                    cfg['format']['stylish']['sign']['removed'],
                    value['key'],
                    value['old_value'],
                    offset
                )
            )
            node_rows.append(
                get_leaf(
                    spaces,
                    cfg['format']['stylish']['sign']['added'],
                    value['key'],
                    value['new_value'],
                    offset
                )
            )
        else:
            node_rows.append(
                get_leaf(
                    spaces,
                    sign,
                    value['key'],
                    value['value'],
                    offset
                )
            )

    end_spases = ' ' * (offset - cfg['format']['stylish']['start_offset'])
    node_rows.append(end_spases + '}')
    return node_rows


def get_dict_format_stylish(value_dict, offset):
    rows = ['{']
    spaces = ' ' * offset
    for key in value_dict.keys():
        rows.append('{spaces}   {key}: {value}'.format(
            spaces=spaces,
            key=key,
            value=get_output_format_stylish(
                value_dict[key],
                offset + cfg['format']['stylish']['add_offset']
            )
        )
        )
    rows.append(spaces[1:] + '}')
    return '\n'.join(rows)


def get_output_format_stylish(value, offset):
    if isinstance(value, (dict)):
        new_value = get_dict_format_stylish(value, offset)
    elif value in STYLISH_VALUE_FORMAT:
        new_value = STYLISH_VALUE_FORMAT[value]
    else:
        new_value = value
    return new_value


def get_leaf(spaces, sign, key, value, offset):
    leaf = '{spaces} {sign} {key}: {value}'.format(
                    spaces=spaces,
                    sign=sign,
                    key=key,
                    value=get_output_format_stylish(
                        value,
                        offset + cfg['format']['stylish']['add_offset']
                    )
                )
    return leaf
