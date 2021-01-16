"""Differences evaluator."""
from differences_evaluator import file_parser, formaters


def generate_diff(
    first_file_path: str,
    second_file_path: str,
    format_output_file: str = None
) -> str:
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    diff = get_diff(first_file_path, second_file_path)

    if format_output_file is None or format_output_file == 'stylish':
        return(formaters.stylish(diff))
    elif format_output_file == 'plain':
        return formaters.plain(diff)


def get_diff(
    first_file_path: str,
    second_file_path: str
) -> dict:

    first_file_data = file_parser.get_repr(
        file_parser.get_data(first_file_path)
    )
    second_file_data = file_parser.get_repr(
        file_parser.get_data(second_file_path)
    )

    return get_node_diff(first_file_data, second_file_data)


def get_node_diff(
    start_data: dict = None,
    end_data: dict = None,
    node: str = 'root'
) -> dict:
    """Generate differences data.

    Parameters:
        start_data: formated dict with data
        end_data: formated dict with data

    Returns:
        formated data with key "diff": add/remove/no change

    """
    def _get_children(
        start_children,
        start_children_keys,
        end_children,
        end_children_keys
    ):
        start_set_children_keys = set(start_children_keys)
        end_set_children_keys = set(end_children_keys)

        removed_children_key = start_set_children_keys - end_set_children_keys
        added_children_key = end_set_children_keys - start_set_children_keys
        children = []

        start_data_no_change_node = {}
        end_data_no_change_node = {}
        for child in start_children:
            if child['node'] in removed_children_key:
                children.append(
                    _get_children_force(
                        data=child,
                        node=child['node'],
                        diff_status='removed'
                        )
                )
                continue
            start_data_no_change_node[child['node']] = child
        for child in end_children:
            if child['node'] in added_children_key:
                children.append(
                    _get_children_force(
                        data=child,
                        node=child['node'],
                        diff_status='added'
                        )
                )
                continue
            end_data_no_change_node[child['node']] = child

        for key in start_data_no_change_node:
            children.append(get_node_diff(
                node=key,
                start_data=start_data_no_change_node[key],
                end_data=end_data_no_change_node[key]))

        return children

    def _get_leafs_diff(start_leafs, end_leafs):
        start_set_leafs_keys = set(start_leafs.keys())
        end_set_leafs_keys = set(end_leafs.keys())
        leafs_diff = []

        for removed_leaf_key in start_set_leafs_keys - end_set_leafs_keys:
            leafs_diff.append(
                {
                    'key': removed_leaf_key,
                    'value': start_leafs[removed_leaf_key],
                    'diff': 'removed'
                }
                )

        for added_leaf_key in end_set_leafs_keys - start_set_leafs_keys:
            leafs_diff.append(
                {
                    'key': added_leaf_key,
                    'value': end_leafs[added_leaf_key],
                    'diff': 'added'
                }
                )

        for leaf_key in end_set_leafs_keys & start_set_leafs_keys:
            if start_leafs[leaf_key] == end_leafs[leaf_key]:
                leafs_diff.append(
                    {
                        'key': leaf_key,
                        'value': end_leafs[leaf_key],
                        'diff': 'no change'
                    }
                    )
            else:
                leafs_diff.append(
                    {
                        'key': leaf_key,
                        'value': start_leafs[leaf_key],
                        'diff': 'removed'
                    }
                    )
                leafs_diff.append(
                    {
                        'key': leaf_key,
                        'value': end_leafs[leaf_key],
                        'diff': 'added'
                    }
                    )
        return leafs_diff

    def _get_children_force(data: dict, node: str, diff_status: str):
        result = {
            'node': node, 'leafs': [], 'children': [], 'diff': diff_status
            }
        for key, value in data['leafs'].items():
            result['leafs'].append(
                {'key': key, 'value': value, 'diff': diff_status}
                )
        if data['children']:
            for child in data['children']:
                result['children'].append(_get_children_force(
                    data=child,
                    node=child['node'],
                    diff_status=diff_status
                ))
        return result

    diff = {'node': node, 'leafs': [], 'children': [], 'diff': 'no change'}
    if start_data['leafs'] or end_data['leafs']:
        diff['leafs'] = _get_leafs_diff(start_data['leafs'], end_data['leafs'])

    if start_data['set_of_children'] or end_data['set_of_children']:
        diff['children'] = _get_children(
            start_data['children'],
            start_data['set_of_children'],
            end_data['children'],
            end_data['set_of_children']
        )

    return diff
