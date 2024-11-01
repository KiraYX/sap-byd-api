import pandas as pd
import warnings

# Temporarily display all columns

# Suppress specific UserWarning from Pandas
warnings.filterwarnings("ignore", category=UserWarning, message="Data Validation extension is not supported")

# Read the BOM sheet with header in row 2
file_path = "data/bom275.xlsx"
sheet_name = "BOM"
df_bom = pd.read_excel(file_path, sheet_name=sheet_name, header=1)


# Drop rows where all cells are NaN
df_bom = df_bom.dropna(how="all")
# Drop columns where all values are NaN
df_bom = df_bom.dropna(axis=1, how="all")


# Display the total number of rows and columns
print("Total rows and columns:", df_bom.shape)

# Replace 'ColumnName' with the actual name of the column up to which you want to keep
last_column_to_keep = "备注"

# List all column names
column_names = df_bom.columns.tolist()
# print(column_names)

# Specify the columns you want to keep
columns_to_keep = ['所属装配体', '布局号', 'PLM编号', '层级深度', '父层级', '整套总数', 'ERP编号', '物料描述', '单层数量', '单位', '物料种类']

# Select only these columns
df_bom = df_bom[columns_to_keep]

with pd.option_context('display.max_columns', None):
  print(df_bom.head())
