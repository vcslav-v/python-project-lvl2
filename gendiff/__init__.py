"""Differences evaluator."""
from gendiff.diff_builder import (STATUS_ADDED, STATUS_NO_CHANGE, STATUS_NODE,
                                  STATUS_REMOVED, STATUS_UPDATED)
from gendiff.evaluator import generate_diff

__all__ = (
    'generate_diff',
    'STATUS_ADDED',
    'STATUS_NO_CHANGE',
    'STATUS_NODE',
    'STATUS_REMOVED',
    'STATUS_UPDATED',
)
