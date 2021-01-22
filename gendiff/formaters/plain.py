"""Formaters."""
from typing import Any, List

STATUS_ADDED = 'added'
STATUS_REMOVED = 'removed'
STATUS_UPDATED = 'updated'
STATUS_NO_CHANGE = 'no change'
STATUS_NODE = 'node'

ADDED_MSG = "Property '{path}' was added with value: {value}"
REMOVED_MSG = "Property '{path}' was removed"
UPDATED_MSG = "Property '{path}' was updated. From {old_value} to {new_value}"
PATH_SEPARATOR = '.'

FALSE_FORMAT = 'false'
TRUE_FORMAT = 'true'
NONE_FORMAT = 'null'
COMPLEX_VALUE_FORMAT = '[complex value]'
STRING_FORMAT = "'{value}'"


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

    output = get_rows(diff)
    return '\n'.join(output)


def get_rows(node: dict, path: List[str] = []) -> List[str]:
    """Formats the diff to a list of strings plain."""
    node_rows = []

    for value in node['values']:
        status, key = value['diff'], value['key']
        if status == STATUS_NODE:
            new_path = [*path, key]
            node_rows.extend(get_rows(value, new_path))

        elif status == STATUS_UPDATED:
            node_rows.append(
                UPDATED_MSG.format(
                    path=get_path(path, value['key']),
                    old_value=get_output_format(value['old_values']),
                    new_value=get_output_format(value['new_values'])
                )
            )

        elif status == STATUS_ADDED:
            node_rows.append(
                ADDED_MSG.format(
                    path=get_path(path, key),
                    value=get_output_format(value['values'])
                )
            )

        elif status == STATUS_REMOVED:
            node_rows.append(
                REMOVED_MSG.format(
                    path=get_path(path, key)
                )
            )

    return node_rows


def get_output_format(value: Any) -> str:
    """Returns the values to the form plain."""
    if isinstance(value, (dict, list)):
        new_value = COMPLEX_VALUE_FORMAT
    elif isinstance(value, str):
        new_value = STRING_FORMAT.format(value=value)
    elif value is True:
        new_value = TRUE_FORMAT
    elif value is False:
        new_value = FALSE_FORMAT
    elif value is None:
        new_value = NONE_FORMAT
    else:
        new_value = value
    return new_value


def get_path(path: List[str], key: str) -> str:
    """Make path string."""
    if not path:
        return key
    return '{path}{sep}{key}'.format(
        path='.'.join(path),
        sep=PATH_SEPARATOR,
        key=key)
