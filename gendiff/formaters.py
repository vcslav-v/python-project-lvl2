"""Formaters."""
import json

# stylish


def get_sign_stylish(diff_item):
    if diff_item['diff'] == 'added':
        return '+'
    elif diff_item['diff'] == 'removed':
        return '-'
    elif diff_item['diff'] == 'no change':
        return ' '


def get_output_format_stylish(value):
    if value is False:
        return 'false'
    elif value is True:
        return 'true'
    elif value is None:
        return 'null'
    else:
        return value


def get_stylish_node_rows(node, offset=1, force_sign=None):
    node_rows = []
    spaces = ' ' * offset
    for leaf in node['leafs']:
        sign = get_sign_stylish(leaf)
        node_rows.append(
            '{spaces} {sign} {key}: {value}'.format(
                spaces=spaces,
                sign=force_sign or get_sign_stylish(leaf),
                key=leaf['key'],
                value=get_output_format_stylish(leaf['value'])
            )
        )

    if node['children']:
        for child in node['children']:
            sign = force_sign or get_sign_stylish(child)
            node_rows.append(
                '{spaces} {sign} {node}: '.format(
                    sign=sign,
                    spaces=spaces,
                    node=child['node']
                ) + '{'
            )
            if force_sign or child['diff'] != 'no change':
                node_rows.extend(
                    get_stylish_node_rows(child, offset+2, ' ')
                )
            else:
                node_rows.extend(get_stylish_node_rows(child, offset+2))
    node_rows.append(spaces + '}')
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
        return 'false'
    elif value is True:
        return 'true'
    elif value is None:
        return 'null'
    elif value == '':
        return "''"
    elif type(value) in (dict, list):
        return "[complex value]"
    else:
        return value


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


def _get_plain_status_property(node):
    no_change_node_property = []
    unique_property = {}
    updated_property = {}

    for leaf in node['leafs']:
        if leaf['diff'] == 'no change':
            continue
        if leaf['key'] in unique_property.keys():
            old_value, new_value = get_updated_plain_values(
                leaf['diff'],
                leaf['value'],
                get_output_plain_format(
                    unique_property.pop(leaf['key'])['value']
                )
            )
            updated_property[leaf['key']] = {
                'old_value': old_value,
                'new_value': new_value
                }
            continue
        unique_property[leaf['key']] = {
            'diff': leaf['diff'],
            'value': get_output_plain_format(leaf['value'])
            }

    for child in node['children']:
        if child['node'] in unique_property.keys():
            old_value, new_value = get_updated_plain_values(
                child['diff'],
                get_output_plain_format(child),
                get_output_plain_format(
                    unique_property.pop(child['node'])['value']
                )
            )
            updated_property[child['node']] = {
                    'old_value': old_value,
                    'new_value': new_value
                    }
            continue
        if child['diff'] == 'no change':
            no_change_node_property.append(child)
        else:
            unique_property[child['node']] = {
                'diff': child['diff'],
                'value': get_output_plain_format(child)
                }

    return (no_change_node_property, unique_property, updated_property)


def get_plain_node_rows(node, path=[]):
    node_rows = []
    no_change_node_property, unique_property, updated_property = (
        _get_plain_status_property(node)
        )
    for key, prop in unique_property.items():
        if prop['diff'] == 'added':
            node_rows.append(
                "Property '{path}' was added with value: {value}".format(
                    path=get_path(path, key),
                    value=prop['value']
                )
            )
        elif prop['diff'] == 'removed':
            node_rows.append(
                "Property '{path}' was removed".format(
                    path=get_path(path, key)
                    )
            )
    for key, value in updated_property.items():
        node_rows.append(
                ("Property '{path}' was updated. "
                    "From {old_value} to {new_value}").format(
                    path=get_path(path, key),
                    old_value=get_output_plain_format(value['old_value']),
                    new_value=get_output_plain_format(value['new_value'])
                )
            )
    if no_change_node_property:
        for child in no_change_node_property:
            new_path = path.copy()
            new_path.append(child['node'])
            node_rows.extend(get_plain_node_rows(child, new_path))
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


def get_json_leafs(leafs, offset):
    space = ' ' * offset
    result_leafs = []
    for leaf in leafs:
        result_leafs.append('{space}{dump},'.format(
            space=space,
            dump=json.dumps(leaf)
            )
        )
    result_leafs[-1] = result_leafs[-1][:-1]
    return result_leafs


def get_json_rows(node, offset=4):
    space = ' ' * offset
    min_space = ' ' * (offset-4)
    node_name = '{space}"node": "{node}",'.format(
        node=node['node'],
        space=space
    )
    leafs_title = '{space}"leafs": ['.format(space=space)
    empty_leafs_title = '{space}"leafs": [],'.format(space=space)
    children_title = '{space}"children": ['.format(space=space)
    empty_children_title = '{space}"children": [],'.format(space=space)
    node_diff = '{space}"diff": "{diff_status}"'.format(
        diff_status=node['diff'],
        space=space
    )
    end_list = '{space}],'.format(space=space)
    output = [min_space + '{']
    output.append(node_name)
    if node['leafs']:
        output.append(leafs_title)
        output.extend(get_json_leafs(node['leafs'], offset+2))
        output.append(end_list)
    else:
        output.append(empty_leafs_title)
    if node['children']:
        output.append(children_title)
        for child in node['children']:
            output.extend(get_json_rows(child, offset+4))
        output[-1] = output[-1][:-1]
        output.append(end_list)
    else:
        output.append(empty_children_title)
    output.append(node_diff)
    output.append(min_space + '},')
    return output


def json_diff_formater(diff: dict) -> str:
    """Format diff data dict to json.
    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """
    output = get_json_rows(diff)
    output[-1] = output[-1][:-1]
    return '\n'.join(output)
