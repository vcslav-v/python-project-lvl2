"""Formaters."""
from gendiff.config import cfg


PLAIN_VALUE_FORMAT = {
    False: cfg['format']['plain']['value_format']['false'],
    True: cfg['format']['plain']['value_format']['true'],
    None: cfg['format']['plain']['value_format']['none']
}


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


def get_plain_node_rows(node, path=[]):
    node_rows = []

    for value in node['value']:
        if value['diff'] == cfg['diff_status']['node']:
            new_path = path.copy()
            new_path.append(value['key'])
            node_rows.extend(get_plain_node_rows(value, new_path))

        elif value['diff'] == cfg['diff_status']['updated']:
            node_rows.append(
                cfg['format']['plain']['updated_msg'].format(
                    path=get_path(path, value['key']),
                    old_value=get_output_plain_format(value['old_value']),
                    new_value=get_output_plain_format(value['new_value'])
                )
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

    return node_rows


def get_output_plain_format(value):
    if isinstance(value, (dict, list)):
        new_value = cfg['format']['plain']['value_format']['complex_value']
    elif value in PLAIN_VALUE_FORMAT:
        new_value = PLAIN_VALUE_FORMAT[value]
    elif isinstance(value, str):
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
