def split_material_description(description):
    # Split the input string by underscores
    parts = description.split('_')

    # Extract the name, brand, and model based on your naming convention
    name = parts[0] if len(parts) > 0 else ''
    brand = parts[1] if len(parts) > 1 else ''
    model = '_'.join(parts[2:]) if len(parts) > 2 else ''

    return name, brand, model

