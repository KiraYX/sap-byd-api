# Archived the code

import os

def find_project_root(project_name='my_project'):
    current_path = os.path.dirname(os.path.abspath(__file__))
    
    while os.path.basename(current_path) != project_name:
        parent_path = os.path.dirname(current_path)
        if current_path == parent_path:  # If we've reached the filesystem root
            raise FileNotFoundError(f"Project folder '{project_name}' not found.")
        current_path = parent_path
    
    return current_path

def find_project_subfolder(project_name, folder_name):
    project_root = find_project_root(project_name=project_name)
    subfolder_path = os.path.join(project_root, folder_name)
    return subfolder_path

if __name__ == '__main__':

    # Example usage
    project_root = find_project_root('sap-byd-api')  # Replace 'my_project' with your actual project folder name
    print(f"Project root: {project_root}")

    json_dir = os.path.join(project_root, 'project', 'json')
    print(f"JSON directory: {json_dir}")

    sub_folder = find_project_subfolder('sap-byd-api', 'utils')
    print(f"Subfolder: {sub_folder}")

    sub_sub_folder = find_project_subfolder('sap-byd-api', 'api/sap')
    print(f"Sub-subfolder: {sub_sub_folder}")
