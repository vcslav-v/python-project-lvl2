"""Json formater."""
from json import dumps as json_dumbs


def json(diff: dict) -> str:
    """Format diff data dict to json.
    Parameters:
        diff: differences data representation
    Returns:
        formated string
    """
    output = json_dumbs(diff)
    return output
