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
    def _get_output_plain_format(value):
        if value is False:
            return 'false'
        elif value is True:
            return 'true'
        elif value is None:
            return 'null'
        elif value == '':
            return "''"
        else:
            return value

    def _get_path(path, key):
        if not path:
            return key
        return '{path}.{key}'.format(path='.'.join(path), key=key)

    def _get_updated_values(property_diff, property_value, other_value):
        if property_diff == 'added':
            old_value, new_value = other_value, property_value
        else:
            old_value, new_value = property_value, other_value
        return old_value, new_value

    def _get_status_property(node):
        no_change_node_property = []
        unique_property = {}
        updated_property = {}

        for leaf in node['leafs']:
            if leaf['diff'] == 'no change':
                continue
            if leaf['key'] in unique_property.keys():
                print(leaf)
                old_value, new_value = _get_updated_values(
                    leaf['diff'],
                    leaf['value'],
                    unique_property.pop(leaf['key'])['value']
                )
                updated_property[leaf['key']] = {
                    'old_value': old_value,
                    'new_value': new_value
                    }
                continue
            unique_property[leaf['key']] = leaf

        for child in node['children']:
            if child['diff'] == 'no change':
                no_change_node_property.append(child)
            elif child['node'] in unique_property.keys():
                if child['diff'] == 'added':
                    updated_property[child['node']] = {
                        'old_value': unique_property.pop(
                            child['node']
                            )['value'],
                        'new_value': '[complex value]'
                        }
                else:
                    updated_property[child['node']] = {
                        'old_value': '[complex value]',
                        'new_value': unique_property.pop(
                            child['node']
                            )['value']
                        }
                continue
        return (no_change_node_property, unique_property, updated_property)

    def _get_plain_node_rows(node, path=[]):
        node_rows = []
        no_change_node_property, unique_property, updated_property = (
            _get_status_property(node)
            )
        for leaf in unique_property.values():
            if leaf['diff'] == 'added':
                node_rows.append(
                    "Property '{path}' was added with value: {value}".format(
                        path=_get_path(path, leaf['key']),
                        value=_get_output_plain_format(leaf['value'])
                    )
                )
            elif leaf['diff'] == 'removed':
                node_rows.append(
                    "Property '{path}' was removed".format(
                        path=_get_path(path, leaf['key'])
                        )
                )

        for key, value in updated_property.items():
            node_rows.append(
                    ("Property '{path}' was updated. "
                        "From {old_value} to {new_value}").format(
                        path=_get_path(path, key),
                        old_value=_get_output_plain_format(value['old_value']),
                        new_value=_get_output_plain_format(value['new_value'])
                    )
                )
        if no_change_node_property:
            for child in no_change_node_property:
                new_path = path.copy()
                new_path.append(child['node'])
                node_rows.extend(_get_plain_node_rows(child, new_path))

        return node_rows
    output = []
    output.extend(_get_plain_node_rows(diff))
    return '\n'.join(output)
