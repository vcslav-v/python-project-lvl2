"""Formaters."""
import json


def json_formater(diff: dict) -> str:
    """Format diff data dict to json.
    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """
    output = json.dumps(diff)
    return output
