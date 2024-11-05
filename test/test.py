import pandas as pd
import re

# Sample data for df_bom_cleaned
data = {
    'PLM编号': [
        '1.1', '1.1', '1.1', '1.1', '1.2', '1.2', '1.3', '1.3', '1.3', '1.3', 
        '1.3.1', '1.3.1', '1.3.2', '1.3.2', '1.4', '1.4', '1.4', '1.4', '1.4', 
        '1.4.1', '1.4.1'
    ],
    'Value': range(21)
}
df_bom_cleaned = pd.DataFrame(data)

# Function to assign group numbers based on PLM编号 with custom grouping
def assign_group_numbers(df, group_column, max_items_per_group=20):
    # Step 1: Extract primary groups and subgroup identifiers
    df['PrimaryGroup'] = df[group_column].apply(lambda x: '.'.join(x.split('.')[:2]))  # e.g., '1.1', '1.2', etc.
    
    # Initialize Group column
    df['GroupNumber'] = None
    
    # Step 2: Assign primary group numbers based on grouping logic
    group_number = 10  # Starting from 10, 20, etc., per rule
    for primary, primary_group in df.groupby('PrimaryGroup'):
        primary_idx = primary_group.index.tolist()
        
        # If primary group size is within the limit, assign directly
        if len(primary_idx) <= max_items_per_group:
            df.loc[primary_idx, 'GroupNumber'] = group_number
        else:
            # Step 3: Create sub-groups if primary group size exceeds the limit
            # Extract subgroups within the primary group
            sub_number = group_number  # e.g., start with 10, 20
            subgroup_count = 1
            
            # Group by '1.3.1', '1.3.2' etc., after the first level in '1.3'
            for subgroup, subgroup_df in primary_group.groupby(group_column):
                subgroup_idx = subgroup_df.index.tolist()
                
                # Split into smaller chunks if subgroup itself is too large
                for i in range(0, len(subgroup_idx), max_items_per_group):
                    df.loc[subgroup_idx[i:i+max_items_per_group], 'GroupNumber'] = sub_number + subgroup_count
                    subgroup_count += 1
        
        # Move to next primary group number
        group_number += 10

    return df

# Apply the function to your DataFrame
df_bom_cleaned = assign_group_numbers(df_bom_cleaned, 'PLM编号')
print(df_bom_cleaned[['PLM编号', 'GroupNumber']])
