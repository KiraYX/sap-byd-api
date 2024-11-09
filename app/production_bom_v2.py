# This script cannot work, rewrite by chatgpt in a class way, but not in a function way
# Will refactor later if necessary

import os
import pandas as pd
import numpy as np
from datetime import datetime
from helper.bom_template import write_df_to_excel

class BomDataTransformer:
    def __init__(self, file_name, sheet_name):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_path, f"../data/{file_name}.xlsx")
        self.sheet_name = sheet_name
        self.df_bom = self.load_data()

    def load_data(self):
        """Load data from Excel."""
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=1)
        df = df.dropna(how="all").dropna(axis=1, how="all")  # Clean NaN rows and columns
        columns_to_keep = ['所属装配体', 'PLM编号', '父层级', '整套总数', 'ERP编号', '物料描述', '单位', '物料种类']
        df = df[columns_to_keep]
        df['PLM编号'] = df['PLM编号'].astype(str)
        return df[df['ERP编号'].notna()]

    def clean_data(self):
        """Apply transformations to clean and process data."""
        self.df_bom['名称'] = self.df_bom['物料描述'].str.split('_', expand=True)[0]
        self.df_bom = self.df_bom[self.df_bom['PLM编号'].str.startswith('1')]
        self.df_bom['父层级'] = self.df_bom['父层级'].apply(self.truncate_plm)
        self.apply_parent_level_mapping()
        self.generate_group_number()
        self.df_bom['父层级名称'] = self.df_bom['父层级名称'].str.upper().str.replace(' ', '_')
        self.df_bom['父层级名称'] = self.df_bom['组编号'] + '-' + self.df_bom['父层级名称']
        self.df_bom['单位'] = self.df_bom['单位'].replace({'EA - 个': 'EA', 'M - 米': 'MTR'})
        self.df_bom['整套总数'] = self.df_bom['整套总数'] / 4
        self.df_bom = self.df_bom[self.df_bom['ERP编号'].str.match(r'^\d{8}$')]
        self.df_bom['工程变更单编号'] = 'IMP' + datetime.now().strftime('%Y%m%d')

    def truncate_plm(self, plm):
        """Truncate PLM编号 to the first three parts."""
        plm = str(plm)
        parts = plm.split('.')
        return '.'.join(parts[:3])

    def apply_parent_level_mapping(self):
        """Map PLM编号 to 名称 based on 父层级."""
        plm_name_mapping = self.df_bom.drop_duplicates(subset='PLM编号', keep='first').set_index('PLM编号')['名称']
        self.df_bom['父层级名称'] = self.df_bom['父层级'].map(plm_name_mapping)

    def generate_group_number(self):
        """Generate 组编号 based on 父层级."""
        self.df_bom['组编号'] = self.df_bom['父层级'].apply(self.generate_group_number_from_plm)

    def generate_group_number_from_plm(self, plm):
        """Helper function to generate group number."""
        parts = str(plm).split('.')
        second_part = parts[1] if len(parts) > 1 else '0'
        third_part = parts[2] if len(parts) > 2 else '0'
        return f"{second_part}{third_part}"

    def generate_serial_numbers(self):
        """Generate serial numbers for the DataFrame."""
        self.df_bom['父层级名称序号'] = self.df_bom.groupby('父层级名称').cumcount() * 10 + 10
        self.df_bom['变量编号'] = 1

    def transform_for_excel(self):
        """Create and rename columns for Excel output."""
        return self.df_bom[['产成品编号', '变量编号', '父层级名称', '父层级名称序号', 'ERP编号', '整套总数', '单位', '工程变更单编号']].rename(columns={
            '父层级名称': '行项目组编号',
            '父层级名称序号': '行项目编号',
            '整套总数': '数量'
        })

    def generate_html_preview(self):
        """Generate an HTML preview."""
        html_output = self.df_bom.to_html(index=False)
        css_link = '<link rel="stylesheet" type="text/css" href="../css/table_style.css">'
        html_output = f"""<!DOCTYPE html>
        <html>
        <head>{css_link}</head>
        <body>
            <div class="table-container">
                {html_output}
            </div>
        </body>
        </html>"""
        return html_output

    def save_html(self, html_content):
        """Save HTML to file."""
        with open(os.path.join(self.base_path, "../html/bom_data_preview.html"), "w") as f:
            f.write(html_content)

    def save_to_excel(self):
        """Save DataFrame to Excel."""
        df_sheet_pairs = [
            (self.df_bom, '用料'),
        ]
        for df, sheet_name in df_sheet_pairs:
            write_df_to_excel(df, 'BOM模板.xlsx', sheet_name)

# Usage
if __name__ == "__main__":
    bom_transformer = BomDataTransformer("bom275", "BOM")
    bom_transformer.clean_data()
    bom_transformer.generate_serial_numbers()
    html_preview = bom_transformer.generate_html_preview()
    bom_transformer.save_html(html_preview)
    bom_transformer.save_to_excel()
