"""Formaters."""
import json

# stylish


def get_dict_format_stylish(value_dict, offset):
    rows = ['{']
    spaces = ' ' * offset
    for key in value_dict.keys():
        rows.append('{spaces}   {key}: {value}'.format(
            spaces=spaces,
            key=key,
            value=get_output_format_stylish(
                value_dict[key], offset + 4
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


def get_stylish_node_rows(node, offset=1, force_sign=None):
    node_rows = []
    spaces = ' ' * offset

    sighs = {
        'added': '+',
        'removed': '-',
        'no change': ' ',
    }
    for value in node['value']:
        sign = sighs[value['diff']]

        if value['type'] == 'leaf':
            node_rows.append(
                '{spaces} {sign} {key}: {value}'.format(
                    spaces=spaces,
                    sign=sign,
                    key=value['key'],
                    value=get_output_format_stylish(value['value'], offset + 4)
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
            node_rows.extend(get_stylish_node_rows(value, offset + 4))

    node_rows.append(spaces[1:] + '}')
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


def get_output_plain_format(value):
    if value is False:
        new_value = 'false'
    elif value is True:
        new_value = 'true'
    elif value is None:
        new_value = 'null'
    elif type(value) is str:
        new_value = "'{value}'".format(value=value)
    elif type(value) in (dict, list):
        new_value = "[complex value]"
    else:
        new_value = value
    return new_value


def get_path(path, key):
    if not path:
        return key
    return '{path}.{key}'.format(path='.'.join(path), key=key)


def get_updated_plain_values(property_diff, property_value, other_value):
    if property_diff == 'added':
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
            node_rows[-1] = (
                "Property '{path}' was updated. "
                "From {old_value} to {new_value}").format(
                path=get_path(path, value['key']),
                old_value=get_output_plain_format(last_value),
                new_value=get_output_plain_format(value['value'])
            )

        elif value['diff'] == 'added':
            node_rows.append(
                "Property '{path}' was added with value: {value}".format(
                    path=get_path(path, value['key']),
                    value=get_output_plain_format(value['value'])
                )
            )
        elif value['diff'] == 'removed':
            node_rows.append(
                "Property '{path}' was removed".format(
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
