def flatten_json(nested_json, parent_key="", sep="."):
    flat_dict = {}

    if isinstance(nested_json, dict):
        for key, value in nested_json.items():
            full_key = f"{parent_key}{sep}{key}" if parent_key else key
            flat_dict.update(flatten_json(value, full_key, sep))
    elif isinstance(nested_json, list):
        for i, item in enumerate(nested_json):
            full_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            flat_dict.update(flatten_json(item, full_key, sep))
    else:
        flat_dict[parent_key] = nested_json

    return flat_dict


