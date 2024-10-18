import os

os.sys.path.append(os.path.join(os.getcwd(), "src"))

import pandas as pd
import json


def normalize(df):
    for col in df.columns:
        try:
            df[col] = df[col].str.replace("’", "'")
        except:
            pass
    return df


level_0_df = normalize(
    pd.read_csv("src/data/themes_step_0.csv", sep=",", header=None, skiprows=1)
)
level_1_df = normalize(
    pd.read_csv("src/data/themes_step_1.csv", sep=",", header=None, skiprows=1)
)
level_2_df = normalize(
    pd.read_csv("src/data/themes_step_2.csv", sep=",", header=None, skiprows=1)
)
level_3_df = normalize(
    pd.read_csv("src/data/themes_step_3.csv", sep=",", header=None, skiprows=1)
)


def build_hierarchy(parent_theme, current_level, df_list):
    current_df = df_list[current_level]
    children = []

    for _, row in current_df[current_df[1] == parent_theme].iterrows():
        child_name = row[0]
        child_total = 0

        if current_level > 0:
            child_children = build_hierarchy(child_name, current_level - 1, df_list)
            children.append(
                {
                    "name": child_name,
                    "total": child_total,
                    "level": current_level,
                    "children": child_children,
                }
            )
        else:
            children.append(
                {
                    "name": child_name,
                    "total": child_total,
                    "level": current_level,
                }
            )

    return children


if __name__ == "__main__":
    df_list = [level_0_df, level_1_df, level_2_df, level_3_df]

    hierarchy = []
    for _, row in level_3_df.iterrows():
        top_parent_name = row[0]
        top_parent_total = 0

        top_parent_children = build_hierarchy(top_parent_name, 2, df_list)

        hierarchy.append(
            {
                "name": top_parent_name,
                "total": top_parent_total,
                "level": 3,
                "children": top_parent_children,
            }
        )

    for _, row in level_1_df[level_1_df[1] == "vide"].iterrows():
        orphan_name = row[0]
        orphan_total = 0

        orphan_children = build_hierarchy(orphan_name, 0, df_list)

        hierarchy.append(
            {
                "name": orphan_name,
                "total": orphan_total,
                "level": 1,
                "children": orphan_children,
            }
        )

    with open("src/data/hierarchy.json", "w") as file:
        json.dump(hierarchy, file)
