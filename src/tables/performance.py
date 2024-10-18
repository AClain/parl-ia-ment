from great_tables import GT, system_fonts, loc, style
from utils.helpers import find_src_directory
from charts.performance import (
    compute_precision_to_df_from_run_ids,
    compute_recall_to_df_from_run_ids,
    compute_fscore_to_df_from_run_ids,
)
from typing import List
from copy import deepcopy


def plot_precisions_table(
    run_ids: List[str],
    title: str = "Precision of different prompt settings per topic label",
    save_folder: str = "images/charts",
) -> None:
    precisions_df = compute_precision_to_df_from_run_ids(run_ids)

    precisions_df = precisions_df.transpose()
    precisions_df["Labels"] = precisions_df.index

    columns = precisions_df.columns.to_list()
    precisions_df.rename(
        columns={
            column: column.replace("zero shot", "0-shot")
            .replace("few shot (n=5)", "5-shot")
            .replace("few-shot (n=5)", "5-shot")
            for column in columns
        },
        inplace=True,
    )
    columns = precisions_df.columns.to_list()

    columns_without_run_names = deepcopy(columns)
    columns_without_run_names.remove("Labels")

    column_new_order = deepcopy(columns)
    column_new_order = column_new_order[-1:] + column_new_order[:-1]

    precisions_df = precisions_df[column_new_order]

    ciep_gt_tbl = GT(data=precisions_df)

    col_widths = {column: "58px" for column in columns}
    col_widths["Labels"] = "180px"

    hexes = [
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "#B5DCFF",
        "#AED9FF",
        "#86C2F7",
        "#5DAAEE",
        "#3386CE",
        "#0961AE",
    ]

    gt_tbl = (
        ciep_gt_tbl.fmt_number(
            columns=columns_without_run_names,
            decimals=2,
        )
        .data_color(
            columns=columns_without_run_names,
            palette=hexes,
            domain=[0.0, 1.0],
        )
        # .tab_header(title=md(title))
        .cols_width(col_widths)
        .tab_style(
            locations=loc.body(columns=["Labels"]), style=[style.text(weight="bold")]
        )
        .tab_options(
            source_notes_font_size="x-small",
            source_notes_padding=3,
            table_font_names=system_fonts("humanist"),
            column_labels_font_weight="bold",
            data_row_padding="1px",
            heading_background_color="antiquewhite",
            source_notes_background_color="antiquewhite",
            column_labels_background_color="antiquewhite",
            table_background_color="snow",
            data_row_padding_horizontal=3,
            column_labels_padding_horizontal=58,
        )
        .cols_align(align="center")
        .cols_align(align="left", columns=["Labels"])
    )

    folder = f"{find_src_directory()}/{save_folder}/{title}"

    gt_tbl.save(folder)

    gt_tbl.show()


def plot_recalls_table(
    run_ids: List[str],
    title: str = "Recall of different prompt settings per topic label",
    save_folder: str = "images/charts",
) -> None:
    recalls_df = compute_recall_to_df_from_run_ids(run_ids)

    recalls_df = recalls_df.transpose()
    recalls_df["Labels"] = recalls_df.index

    columns = recalls_df.columns.to_list()
    recalls_df.rename(
        columns={
            column: column.replace("zero shot", "0-shot")
            .replace("few shot (n=5)", "5-shot")
            .replace("few-shot (n=5)", "5-shot")
            for column in columns
        },
        inplace=True,
    )
    columns = recalls_df.columns.to_list()

    columns_without_run_names = deepcopy(columns)
    columns_without_run_names.remove("Labels")

    column_new_order = deepcopy(columns)
    column_new_order = column_new_order[-1:] + column_new_order[:-1]

    recalls_df = recalls_df[column_new_order]

    ciep_gt_tbl = GT(data=recalls_df)

    col_widths = {column: "58px" for column in columns}
    col_widths["Labels"] = "180px"

    hexes = [
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "#B5DCFF",
        "#AED9FF",
        "#86C2F7",
        "#5DAAEE",
        "#3386CE",
        "#0961AE",
    ]

    gt_tbl = (
        ciep_gt_tbl.fmt_number(
            columns=columns_without_run_names,
            decimals=2,
        )
        .data_color(
            columns=columns_without_run_names,
            palette=hexes,
            domain=[0.0, 1.0],
        )
        # .tab_header(title=md(title))
        .cols_width(col_widths)
        .tab_style(
            locations=loc.body(columns=["Labels"]), style=[style.text(weight="bold")]
        )
        .tab_options(
            source_notes_font_size="x-small",
            source_notes_padding=3,
            table_font_names=system_fonts("humanist"),
            column_labels_font_weight="bold",
            data_row_padding="1px",
            heading_background_color="antiquewhite",
            source_notes_background_color="antiquewhite",
            column_labels_background_color="antiquewhite",
            table_background_color="snow",
            data_row_padding_horizontal=3,
            column_labels_padding_horizontal=58,
        )
        .cols_align(align="center")
        .cols_align(align="left", columns=["Labels"])
    )

    folder = f"{find_src_directory()}/{save_folder}/{title}"

    gt_tbl.save(folder)

    gt_tbl.show()


def plot_fscores_table(
    run_ids: List[str],
    title: str = "F1 score of different prompt settings per topic label",
    save_folder: str = "images/charts",
) -> None:
    fscores_df = compute_fscore_to_df_from_run_ids(run_ids)

    fscores_df = fscores_df.transpose()
    fscores_df["Labels"] = fscores_df.index

    columns = fscores_df.columns.to_list()
    fscores_df.rename(
        columns={
            column: column.replace("zero shot", "0-shot")
            .replace("few shot (n=5)", "5-shot")
            .replace("few-shot (n=5)", "5-shot")
            for column in columns
        },
        inplace=True,
    )
    columns = fscores_df.columns.to_list()

    columns_without_run_names = deepcopy(columns)
    columns_without_run_names.remove("Labels")

    column_new_order = deepcopy(columns)
    column_new_order = column_new_order[-1:] + column_new_order[:-1]

    fscores_df = fscores_df[column_new_order]

    ciep_gt_tbl = GT(data=fscores_df)

    col_widths = {column: "58px" for column in columns}
    col_widths["Labels"] = "180px"

    hexes = [
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "snow",
        "#B5DCFF",
        "#AED9FF",
        "#86C2F7",
        "#5DAAEE",
        "#3386CE",
        "#0961AE",
    ]

    gt_tbl = (
        ciep_gt_tbl.fmt_number(
            columns=columns_without_run_names,
            decimals=2,
        )
        .data_color(
            columns=columns_without_run_names,
            palette=hexes,
            domain=[0.0, 1.0],
        )
        # .tab_header(title=md(title))
        .cols_width(col_widths)
        .tab_style(
            locations=loc.body(columns=["Labels"]), style=[style.text(weight="bold")]
        )
        .tab_options(
            source_notes_font_size="x-small",
            source_notes_padding=3,
            table_font_names=system_fonts("humanist"),
            column_labels_font_weight="bold",
            data_row_padding="1px",
            heading_background_color="antiquewhite",
            source_notes_background_color="antiquewhite",
            column_labels_background_color="antiquewhite",
            table_background_color="snow",
            data_row_padding_horizontal=3,
            column_labels_padding_horizontal=58,
        )
        .cols_align(align="center")
        .cols_align(align="left", columns=["Labels"])
    )

    folder = f"{find_src_directory()}/{save_folder}/{title}"

    gt_tbl.save(folder)

    gt_tbl.show()
