import os
import numpy as np
import pandas as pd
import warnings
from helper.bom_template import write_df_to_excel

# Suppress specific UserWarning from Pandas
warnings.filterwarnings("ignore", category=UserWarning, message="Data Validation extension is not supported")

# Load the Excel file to dataframe
def load_data_frame_from_excel(file_name, sheet_name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, f"../data/{file_name}.xlsx")
    sheet_name = sheet_name
    df_bom = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
    return df_bom

df_bom_origin = load_data_frame_from_excel("bom275","BOM")

# Drop rows where all cells are NaN
df_bom_origin = df_bom_origin.dropna(how="all")
# Drop columns where all values are NaN
df_bom_origin = df_bom_origin.dropna(axis=1, how="all")


# Display the total number of rows and columns
print("Original Total rows and columns:", df_bom_origin.shape)

# Specify the columns you want to keep
columns_to_keep = ['所属装配体', 'PLM编号', '父层级', '整套总数', 'ERP编号', '物料描述', '单位', '物料种类']
# Select only these columns
df_bom_origin = df_bom_origin[columns_to_keep]
# Convert all values in 'PLM编号' to string before filtering
df_bom_origin['PLM编号'] = df_bom_origin['PLM编号'].astype(str)
# Drop rows where 'PLM编号' is NaN
df_bom_cleaned = df_bom_origin[df_bom_origin['ERP编号'].notna()]

# Ensure df_bom_cleaned is a proper independent copy while keeping all columns
df_bom_cleaned = df_bom_cleaned.copy()

# Now you can add the new column without the warning
df_bom_cleaned['名称'] = df_bom_cleaned['物料描述'].str.split('_', expand=True)[0]

# Drop rows where 'PLM编号' not start with 1
df_bom_cleaned = df_bom_cleaned[df_bom_cleaned['PLM编号'].str.startswith('1')]

# Function to remove the part after the 3rd dot, with string conversion
def truncate_plm(plm):
    plm = str(plm)  # Convert the value to string to avoid errors
    parts = plm.split('.')
    return '.'.join(parts[:3])  # Keep only the first 3 parts

# Apply this function to the '父层级' column
df_bom_cleaned['父层级'] = df_bom_cleaned['父层级'].apply(truncate_plm)

# Step 1: Remove duplicates and keep only the first `名称` for each unique `PLM编号`
plm_name_mapping = df_bom_cleaned.drop_duplicates(subset='PLM编号', keep='first').set_index('PLM编号')['名称']

# Step 2: Use the 父层级 value to lookup PLM编号 and return the corresponding 名称
df_bom_cleaned['父层级名称'] = df_bom_cleaned['父层级'].map(plm_name_mapping)

# Function to create 组编号
def generate_group_number(plm):
    parts = str(plm).split('.')  # Convert to string and split by '.'
    
    # If there are at least two parts, join the second and third
    # Otherwise, set them as '0'
    second_part = parts[1] if len(parts) > 1 else '0'
    third_part = parts[2] if len(parts) > 2 else '0'
    
    return f"{second_part}{third_part}"

# Apply this function to the '父层级' column to create '组编号'
df_bom_cleaned['组编号'] = df_bom_cleaned['父层级'].apply(generate_group_number)

# Step 1: Create '父层级名称' by applying the necessary transformations
df_bom_cleaned['父层级名称'] = df_bom_cleaned['父层级名称'].str.upper()  # Convert to uppercase
df_bom_cleaned['父层级名称'] = df_bom_cleaned['父层级名称'].str.replace(' ', '_')  # Replace spaces with '_'

# Step 2: Combine '组编号' and '父层级名称' with an underscore
df_bom_cleaned['父层级名称'] = df_bom_cleaned['组编号'] + '-' + df_bom_cleaned['父层级名称']

# Replace specific values in the '单位' column
df_bom_cleaned['单位'] = df_bom_cleaned['单位'].replace({
    'EA - 个': 'EA',
    'M - 米': 'MTR'
})
# Divide each value in the '整套总数' column by 4
df_bom_cleaned['整套总数'] = df_bom_cleaned['整套总数'] / 4

# Drop the specified columns and update the DataFrame in place
df_bom_cleaned.drop(columns=['名称', '组编号', '父层级'], inplace=True)

# Drop rows where 'ERP编号' does not match the 8-digit pattern
df_bom_cleaned = df_bom_cleaned[df_bom_cleaned['ERP编号'].str.match(r'^\d{8}$')]

# Function to find the ERP编号 of the 产成品 based on PLM编号
def find_finished_product(plm编号):
    # Convert PLM编号 to string and split it by dot to get parts of the hierarchy
    parts = str(plm编号).split('.')
    
    # Step 1: Check if the current PLM编号 is already a 产成品 at the parent level
    # Check the parent level (one level above)
    if len(parts) > 1:
        parent_level = '.'.join(parts[:-1])  # Parent level by removing the last part
        match = df_bom_cleaned[df_bom_cleaned['PLM编号'] == parent_level]
        
        # If parent level is a 产成品, return the ERP编号
        if not match.empty and match['物料种类'].iloc[0] == '产成品':
            return match['ERP编号'].iloc[0]

    # Step 2: Check progressively higher levels (from the full PLM编号 to higher levels)
    for i in range(len(parts), 0, -1):
        # Form the current higher level PLM编号
        higher_level = '.'.join(parts[:i])
        
        # Avoid looking up itself at the highest level (if it's already 产成品 at this level)
        if higher_level == str(plm编号):
            continue
        
        # Check if this level corresponds to 产成品
        match = df_bom_cleaned[df_bom_cleaned['PLM编号'] == higher_level]
        
        if not match.empty and match['物料种类'].iloc[0] == '产成品':
            # Return the ERP编号 of the finished product
            return match['ERP编号'].iloc[0]
    
    # If no 产成品 found at any higher level, return NaN
    return float('nan')

# Apply the function to the 'PLM编号' column to create the '产成品编号' column
df_bom_cleaned['产成品编号'] = df_bom_cleaned['PLM编号'].apply(find_finished_product)

# Add '_1' suffix only to non-NaN values in '产成品编号'
df_bom_cleaned['产成品编号'] = df_bom_cleaned['产成品编号'].apply(lambda x: str(x) + '_1' if pd.notna(x) else x)

from datetime import datetime

# Get current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y%m%d')

# Add the '工程变更单编号' column with "IMP" + current date
df_bom_cleaned['工程变更单编号'] = 'IMP' + current_date

# Create a function to generate serial numbers starting from 10 and increasing by 10
def generate_serial(group):
    group['父层级名称序号'] = range(10, 10 * (len(group) + 1), 10)
    return group

df_bom_product = df_bom_cleaned.copy()

# Filter rows where '物料种类' is '产成品'
df_bom_product = df_bom_product[df_bom_product['物料种类'] == '产成品']


# Drop rows where '产成品编号' is NaN
df_bom_cleaned = df_bom_cleaned.dropna(subset=['产成品编号'])

# Generate serial numbers without triggering the deprecation warning
df_bom_cleaned['父层级名称序号'] = df_bom_cleaned.groupby('父层级名称').cumcount() * 10 + 10

# Add the '变量编号' column with value 1 for all rows
df_bom_cleaned['变量编号'] = 1

# Create the new DataFrame by selecting and renaming columns
df_bom_material_detail = df_bom_cleaned[
    ['产成品编号', '变量编号', '父层级名称', '父层级名称序号', 'ERP编号', '整套总数', '单位', '工程变更单编号']
].rename(columns={
    '父层级名称': '行项目组编号',
    '父层级名称序号': '行项目编号',
    '整套总数': '数量'
})

# Extract unique values of '父层级名称' and '物料清单编号'
df_bom_group = df_bom_cleaned[['产成品编号', '父层级名称']].drop_duplicates()
df_bom_group_description = df_bom_group.copy()
df_bom_group_base = df_bom_group.copy()

# Add the new columns with default values
df_bom_group_description['语言'] = '中文'
df_bom_group_description['行项目组描述'] = '默认'
print(df_bom_group_description.shape)
df_bom_group_base['允许选择多个项目'] = 'X'
print(df_bom_group_base.shape)

df_bom_product = df_bom_product[['ERP编号','所属装配体','单位']]
df_bom_product['物料清单编号'] = df_bom_product['ERP编号'].astype(str) + '_1'

df_bom_base = df_bom_product.copy()
df_bom_variable = df_bom_product.copy()
df_bom_variable_description = df_bom_product.copy()

# Create the new structured DataFrame with required columns and values
df_bom_base = pd.DataFrame({
    '物料清单编号': df_bom_base['物料清单编号'],
    '语言': '中文',  # New column with constant value '中文'
    '所属装配体': df_bom_base['所属装配体'],
    'BOM类型': '临时'  # New column with constant value '临时'
})

df_bom_variable = pd.DataFrame({
    '物料清单编号': df_bom_variable['物料清单编号'],
    '变量编号': 1,  # New column with constant value 1
    '产品编号': df_bom_variable['ERP编号'],
    '产品规格编号': np.nan,
    '数量': 1,
    '单位': df_bom_variable['单位'],
})

df_bom_variable_description = pd.DataFrame({
    '物料清单编号': df_bom_variable_description['物料清单编号'],
    '变量编号': 1,  # New column with constant value 1
    '语言': '中文',
    '变量描述': '初始'
})

df_bom_preview = df_bom_variable

# Generate the HTML table without inline styles
html_output = df_bom_preview.to_html(index=False)  # Convert DataFrame to HTML without row indices

# Add a link to the external CSS file located in ../css
css_link = '<link rel="stylesheet" type="text/css" href="../css/table_style.css">'
html_output = f"""<!DOCTYPE html>
<html>
<head>
    {css_link}
</head>
<body>
    <div class="table-container">
        {html_output}
    </div>
</body>
</html>"""

base_path = os.path.dirname(os.path.abspath(__file__))

# Write the HTML with linked CSS to a file
with open(os.path.join(base_path, "../html/bom_data_preview.html"), "w") as f:
    f.write(html_output)

# List of (DataFrame, sheet_name) pairs
df_sheet_pairs = [
    (df_bom_material_detail, '用料'),
    (df_bom_group_description, '项目组描述'),
    (df_bom_group_base, '物料清单项目组'),
    (df_bom_base, '物料清单基本信息'),
    (df_bom_variable, '物料清单变量'),
    (df_bom_variable_description, '变量描述')
]

# Loop through the pairs and write each DataFrame to Excel
for df, sheet_name in df_sheet_pairs:
    write_df_to_excel(df, 'BOM模板.xlsx', sheet_name)
