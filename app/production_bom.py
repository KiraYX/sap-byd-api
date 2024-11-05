import os
import pandas as pd
import warnings
from tabulate import tabulate


# Suppress specific UserWarning from Pandas
warnings.filterwarnings("ignore", category=UserWarning, message="Data Validation extension is not supported")

# Set base path to the script's directory
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "../data/bom275.xlsx")
sheet_name = "BOM"
df_bom_origin = pd.read_excel(file_path, sheet_name=sheet_name, header=1)

# Drop rows where all cells are NaN
df_bom_origin = df_bom_origin.dropna(how="all")
# Drop columns where all values are NaN
df_bom_origin = df_bom_origin.dropna(axis=1, how="all")

# Display the total number of rows and columns
print("Original Total rows and columns:", df_bom_origin.shape)

# Specify the columns you want to keep
columns_to_keep = ['所属装配体', 'PLM编号', '层级深度', 'T1','T2', 'T3', 'T4', '整套总数', 'ERP编号', '物料描述', '单位', '物料种类']
# Select only these columns
df_bom_origin = df_bom_origin[columns_to_keep]
# Convert all values in 'PLM编号' to string before filtering
df_bom_origin['PLM编号'] = df_bom_origin['PLM编号'].astype(str)
# Drop rows where 'PLM编号' is NaN
df_bom_cleaned = df_bom_origin[df_bom_origin['ERP编号'].notna()]
# Drop rows where 'ERP编号' does not match the 8-digit pattern
df_bom_cleaned = df_bom_cleaned[df_bom_cleaned['ERP编号'].str.match(r'^\d{8}$')]
# Drop rows where 'PLM编号' not start with 1
df_bom_cleaned = df_bom_cleaned[df_bom_cleaned['PLM编号'].str.startswith('1')]
# Replace specific values in the '单位' column
df_bom_cleaned['单位'] = df_bom_cleaned['单位'].replace({
    'EA - 个': 'EA',
    'M - 米': 'MTR'
})
# Divide each value in the '整套总数' column by 4
df_bom_cleaned['整套总数'] = df_bom_cleaned['整套总数'] / 4

# Step 1: Count the occurrences of each value in T2
value_counts = df_bom_cleaned['T2'].value_counts()

# Step 2: Create a mapping for T3 based on counts in T2
# Set T3 to 0 if the count of T2 is less than 20
df_bom_cleaned['T3'] = df_bom_cleaned.apply(lambda row: 0 if value_counts[row['T2']] < 20 else row['T3'], axis=1)

# Step 1: Count the occurrences of each value in T3
value_counts_t3 = df_bom_cleaned['T3'].value_counts()

# Step 2: Set T3 to 0 if its count is less than 3
# df_bom_cleaned['T3'] = df_bom_cleaned['T3'].apply(lambda x: 0 if value_counts_t3[x] < 2 else x)

# Step 1: Count occurrences of each T3 value within each T2 group
t2_t3_counts = df_bom_cleaned.groupby(['T2', 'T3']).size().reset_index(name='T3_Count')

# Step 2: Merge the counts back into the original DataFrame
df_bom_cleaned = df_bom_cleaned.merge(t2_t3_counts[['T2', 'T3', 'T3_Count']], on=['T2', 'T3'], how='left')

# Step 3: Apply the transformation: if count is less than 2, set T3 to 0
df_bom_cleaned['T3'] = df_bom_cleaned.apply(lambda row: 0 if row['T3_Count'] < 2 else row['T3'], axis=1)

# Drop the temporary T3_Count column
df_bom_cleaned.drop(columns=['T3_Count'], inplace=True)

# Step 1: Combine T2 and T3 into a new column 'T2_T3_Combined'
df_bom_cleaned['Group'] = df_bom_cleaned['T2'].astype(str) + df_bom_cleaned['T3'].astype(str)

# Step 2: Insert 'T2_T3_Combined' before 'T1'
cols = df_bom_cleaned.columns.tolist()  # Get the current column order
new_col_index = cols.index('T1')  # Find the index of 'T1' to insert before it
cols.insert(new_col_index, cols.pop(cols.index('Group')))  # Move the new column before 'T1'
df_bom_cleaned = df_bom_cleaned[cols]  # Reorder DataFrame with new column order

# Step 1: Count occurrences of each value in the 'Group' column
group_counts = df_bom_cleaned['Group'].value_counts()

# Step 2: Map the count back to a new column 'Group_Count'
df_bom_cleaned['Group_Count'] = df_bom_cleaned['Group'].map(group_counts)

# Step 3: Insert the new 'Group_Count' column right after 'Group'
df_bom_cleaned.insert(df_bom_cleaned.columns.get_loc('Group') + 1, 'Group_Count', df_bom_cleaned.pop('Group_Count'))

unique_values = df_bom_cleaned['所属装配体'].unique()
print(unique_values)

# Dictionary of translations with abbreviations
translation_dict = {
    'Flipper翻转机构': 'FLIPPER_FLIP_MECH',
    '机架': 'FRAME',
    '输送模组基座板': 'CONVEYOR_MOD_BASE_PLATE',
    '驱动轮组': 'DRIVE_WHEEL_ASS',
    '被动轮组': 'PASSIVE_WHEEL_ASS',
    '输送带支撑桥': 'CONVEYOR_BELT_SUPPORT_BRIDGE',
    '输送带模组': 'CONVEYOR_BELT_MOD',
    '驱动传动轮组A（带张紧调整）\n（两种装配体配置）': 'DRIVE_TRANSMISSION_WHEEL_GROUP_A',
    '轴承座': 'BEARING_SEAT',
    '驱动传动轮组B': 'DRIVE_TRANSMISSION_WHEEL_GROUP_B',
    '输送驱动电机模组（带张紧调整）': 'CONVEYOR_DRIVE_MOTOR_MOD',
    '输送机壳体': 'CONVEYOR_HOUSING',
    '侧护板模组': 'SIDE_GUARD_MOD',
    '传感器及支架': 'SENSOR_AND_BRACKET',
    '传感器支撑': 'SENSOR_SUPPORT',
    '传感器模组': 'SENSOR_MOD',
    '传感器侧': 'SENSOR_SIDE',
    '反射器模组': 'REFLECTOR_MOD',
    '反射器侧': 'REFLECTOR_SIDE',
    '翻转轴座90度侧': 'FLIP_AXIS_SEAT',
    '翻转轴座45度侧': 'FLIP_AXIS_SEAT',
    '90度翻齿': '90_DEGREE_FLIP_TEETH',
    '90度翻齿2': '90_DEGREE_FLIP_TEETH_2',
    '链轮模组D24': 'SPROCKET_MOD_D24',
    '转轴模组': 'PIVOT_MOD',
    '90度翻齿组': '90_DEGREE_FLIP_TEETH_GROUP',
    '45度翻齿': '45_DEGREE_FLIP_TEETH',
    '翻转驱动电机模组（带张紧调整）': 'FLIP_DRIVE_MOTOR_MOD',
    '链轮模组D32': 'SPROCKET_MOD_D32',
    '直线轴承座模组': 'LINEAR_BEARING_SEAT_MOD',
    '齿轮箱支撑模组': 'GEARBOX_SUPPORT_MOD',
    '翻齿模组': 'FLIP_TEETH_MOD',
    '连杆模块': 'LINK_MOD',
    '定心连杆模块': 'CENTERING_LINK_MOD',
    '左凸轮滑动模块': 'LEFT_CAM_SLIDING_MOD',
    '右凸轮滑动模块': 'RIGHT_CAM_SLIDING_MOD',
    '滑动模块': 'SLIDING_MOD',
    '底板': 'BOTTOM_PLATE',
    '驱动电机模块': 'DRIVE_MOTOR_MOD',
    '导轴板': 'GUIDE_SHAFT_PLATE',
    '凸轮板': 'CAM_PLATE',
    '轴支撑': 'AXIS_SUPPORT',
    '凸轮导向': 'CAM_GUIDANCE',
    '升降驱动模组': 'LIFTING_DRIVE_MOD',
    'Flipper电气': 'FLIPPER_ELECTRICAL',
    'Flipper伺服柜': 'FLIPPER_SERVO_CABINET'
}

# Translate the 所属装配体 column using the translation dictionary
df_bom_cleaned['所属装配体_English'] = df_bom_cleaned['所属装配体'].map(translation_dict)

# Ensure that 'Group' and '所属装配体_English' are both strings for proper concatenation
df_bom_cleaned['Group'] = df_bom_cleaned['Group'].astype(str)
df_bom_cleaned['所属装配体_English'] = df_bom_cleaned['所属装配体_English'].astype(str)

# Combine 'Group' and '所属装配体_English' with an underscore in between
df_bom_cleaned['Combined_Group_Assembly'] = df_bom_cleaned['Group'] + "_" + df_bom_cleaned['所属装配体_English']

# Drop the specified columns and update the DataFrame in place
df_bom_cleaned.drop(columns=['所属装配体', '所属装配体_English', 'Group'], inplace=True)

# Generate the HTML table without inline styles
html_output = df_bom_cleaned.to_html(index=False)  # Convert DataFrame to HTML without row indices

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

# Write the HTML with linked CSS to a file
with open(os.path.join(base_path, "../html/bom_data_preview.html"), "w") as f:
    f.write(html_output)


# Call the function to write the DataFrame to Excel
# write_df_to_excel(df_bom_basic, 'BOM模板.xlsx', '物料清单基本信息', start_row=8, start_col=1)