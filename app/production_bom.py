import os
import pandas as pd
import warnings
from tabulate import tabulate
from helper.bom_template import write_df_to_excel

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
columns_to_keep = ['所属装配体', 'PLM编号', '层级深度', '父层级', '整套总数', 'ERP编号', '物料描述', '单层数量', '单位', '物料种类']
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