#!/usr/bin/env python3

import sys
import json

in_path = sys.argv[1]
out_path = sys.argv[2]


# From https://gist.github.com/nvie/f304caf3b4f1ca4c3884
def traverse(obj, path=None, callback=None):
    """
    Traverse an arbitrary Python object structure (limited to JSON data
    types), calling a callback function for every element in the structure,
    and inserting the return value of the callback as the new value.
    """
    if path is None:
        path = []

    if isinstance(obj, dict):
        value = {k: traverse(v, path + [k], callback) for k, v in obj.items()}
    elif isinstance(obj, list):
        value = [traverse(elem, path + [[]], callback) for elem in obj]
    else:
        value = obj

    if callback is None:
        return value
    else:
        return callback(path, value)


def update_dashboard(path, value):
    # Disable 'editable'
    if path and path[-1] == "editable" and value:
        value = False

    # Add 'infra' tag
    if len(path) == 1 and path[0] == "tags":
        if 'infra' not in value:
            value.insert(0, 'infra')

    return value


with open(in_path) as f_in:
    dashboard_json = json.load(f_in)
    dashboard_json_updated = traverse(dashboard_json,
                                      callback=update_dashboard)
    formatted_json = json.dumps(dashboard_json_updated,
                                indent=4,
                                sort_keys=True)
    with open(out_path, 'w') as f_out:
        f_out.write(formatted_json)
