# Split the input string by underscores
# For Mujin sap naming convention

def split_material_description(description):
    # Split the input string by underscores
    parts = description.split('_')

    # Extract the name, brand, and model based on your naming convention
    name = parts[0] if len(parts) > 0 else ''
    brand = parts[1] if len(parts) > 1 else ''
    model = '_'.join(parts[2:]) if len(parts) > 2 else ''

    # Return tunple
    return name, brand, model

# Function to concatenate name, brand, and model with underscores
def concat_material_description(name, brand, model):
    # Filter out empty strings to avoid extra underscores
    return '_'.join([part for part in [name, brand, model] if part])

if __name__ == "__main__":
    old_description = "视觉控制器_MUJIN_MC9000-3DV-RS-LOGI"
    print("old_description:", old_description)

    name, brand, model = split_material_description(old_description)

    print("name:", name)
    print("brand:", brand)
    print("model:", model)

    new_description = concat_material_description(name, brand, model)
    print("new_description:", new_description)