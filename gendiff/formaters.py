"""Formaters."""
import json

from gendiff.config import cfg


def get_output_string(diff_data: dict, output_format: str) -> str:

    if output_format == cfg['output_format']['stylish']:
        diff = stylish(diff_data)
    elif output_format == cfg['output_format']['plain']:
        diff = plain(diff_data)
    elif output_format == cfg['output_format']['json']:
        diff = json_diff_formater(diff_data)

    return diff


# stylish
SIGN = {
    cfg['diff_status']['added']: cfg['format']['stylish']['sign']['added'],
    cfg['diff_status']['removed']: cfg['format']['stylish']['sign']['removed'],
    cfg['diff_status']['no_change']: (
        cfg['format']['stylish']['sign']['no_change']
    ),
}


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
    if value is False:
        new_value = 'false'
    elif value is True:
        new_value = 'true'
    elif value is None:
        new_value = 'null'
    elif type(value) == dict:
        new_value = get_dict_format_stylish(value, offset)
    else:
        new_value = value
    return new_value


def get_stylish_node_rows(
    node,
    offset=cfg['format']['stylish']['start_offset'],
    force_sign=None
):
    node_rows = []
    spaces = ' ' * offset

    for value in node['value']:
        sign = SIGN[value['diff']]

        if value['type'] == 'leaf':
            node_rows.append(
                '{spaces} {sign} {key}: {value}'.format(
                    spaces=spaces,
                    sign=sign,
                    key=value['key'],
                    value=get_output_format_stylish(
                        value['value'],
                        offset + cfg['format']['stylish']['add_offset']
                    )
                )
            )
        elif value['type'] == 'node':
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

    end_spases = ' ' * (offset - cfg['format']['stylish']['start_offset'])
    node_rows.append(end_spases + '}')
    return node_rows


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


# plain
PLAIN_VALUE_FORMAT = {
    False: cfg['format']['plain']['value_format']['false'],
    True: cfg['format']['plain']['value_format']['true'],
    None: cfg['format']['plain']['value_format']['none']
}


def get_output_plain_format(value):
    if type(value) in (dict, list):
        new_value = cfg['format']['plain']['value_format']['complex_value']
    elif value in PLAIN_VALUE_FORMAT:
        new_value = PLAIN_VALUE_FORMAT[value]
    elif type(value) is str:
        new_value = cfg['format']['plain']['value_format']['string'].format(
            value=value
        )
    else:
        new_value = value
    return new_value


def get_path(path, key):
    if not path:
        return key
    return '{path}{sep}{key}'.format(
        path='.'.join(path),
        sep=cfg['format']['plain']['path_separator'],
        key=key)


def get_updated_plain_values(property_diff, property_value, other_value):
    if property_diff == cfg['diff_status']['added']:
        old_value, new_value = other_value, property_value
    else:
        old_value, new_value = property_value, other_value
    return old_value, new_value


def get_plain_node_rows(node, path=[]):
    node_rows = []
    if node['value'] != []:
        last_key, last_value = (
            node['value'][0]['key'], node['value'][0]['value']
        )
    for value in node['value']:
        if value['type'] == 'node':
            new_path = path.copy()
            new_path.append(value['key'])
            node_rows.extend(get_plain_node_rows(value, new_path))

        elif value['key'] == last_key and node_rows:
            node_rows[-1] = cfg['format']['plain']['updated_msg'].format(
                path=get_path(path, value['key']),
                old_value=get_output_plain_format(last_value),
                new_value=get_output_plain_format(value['value'])
            )

        elif value['diff'] == cfg['diff_status']['added']:
            node_rows.append(
                cfg['format']['plain']['added_msg'].format(
                    path=get_path(path, value['key']),
                    value=get_output_plain_format(value['value'])
                )
            )
        elif value['diff'] == cfg['diff_status']['removed']:
            node_rows.append(
                cfg['format']['plain']['removed_msg'].format(
                    path=get_path(path, value['key'])
                )
            )
        last_key, last_value = value['key'], value['value']

    return node_rows


def plain(diff: dict) -> str:
    """Format diff data dict.
    Property 'path.property' was added with value: 'value'
    Property 'path.property' was removed
    Property 'path.property' was updated. From 'value 1' to 'value 2'
    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """

    output = []
    output.extend(get_plain_node_rows(diff))
    return '\n'.join(output)


# json

def json_diff_formater(diff: dict) -> str:
    """Format diff data dict to json.
    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """
    output = json.dumps(diff)
    return output
