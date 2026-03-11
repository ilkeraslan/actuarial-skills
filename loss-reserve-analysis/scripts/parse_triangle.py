"""
Parse loss development triangles from Excel or CSV files.
Handles standard triangle layout, columnar layout, and common variations.
"""
import pandas as pd
import numpy as np
import sys
import json
import argparse


def detect_triangle_format(df):
    """Detect whether data is in triangle format or columnar format."""
    if df.shape[1] >= 3 and df.shape[0] > df.shape[1] * 1.5:
        return "columnar"
    numeric_cols = df.select_dtypes(include=[np.number]).shape[1]
    if numeric_cols >= 3 and df.shape[0] <= numeric_cols + 5:
        return "triangle"
    return "triangle"


def parse_triangle_format(df):
    """Parse a standard triangle: rows=accident periods, cols=development periods."""
    df = df.copy()

    # Find the first row where column 0 looks like a year/period label
    # and remaining columns are numeric (this is the data start)
    data_start = None
    for i in range(min(10, len(df))):
        row_vals = df.iloc[i, 1:].dropna()
        numeric_count = sum(1 for v in row_vals if _is_numeric(v))
        if numeric_count >= 2 and _looks_like_period(df.iloc[i, 0]):
            data_start = i
            break

    if data_start is None:
        # Fallback: skip rows until we find numeric data
        for i in range(min(10, len(df))):
            row_vals = df.iloc[i, 1:].dropna()
            numeric_count = sum(1 for v in row_vals if _is_numeric(v))
            if numeric_count >= 2:
                data_start = i
                break
        if data_start is None:
            data_start = 1  # skip header

    result = df.iloc[data_start:].copy()
    result.columns = range(result.shape[1])

    # First column = accident period labels
    acc_periods = result.iloc[:, 0].astype(str).str.strip()
    # Clean year strings
    acc_periods = acc_periods.apply(lambda x: str(int(float(x))) if _is_numeric(x) and '.' in str(x) else x)

    # Remaining columns = loss values by development period
    triangle_data = result.iloc[:, 1:]
    triangle_data = triangle_data.apply(pd.to_numeric, errors='coerce')

    # Remove rows that are all NaN or look like summary/total rows
    valid_mask = triangle_data.notna().any(axis=1)
    acc_periods = acc_periods[valid_mask].reset_index(drop=True)
    triangle_data = triangle_data[valid_mask].reset_index(drop=True)

    # Filter out rows where acc_period doesn't look like a period label
    keep_mask = acc_periods.apply(_looks_like_period)
    acc_periods = acc_periods[keep_mask].reset_index(drop=True)
    triangle_data = triangle_data[keep_mask].reset_index(drop=True)

    # Create development period labels (1, 2, 3, ...)
    dev_periods = list(range(1, triangle_data.shape[1] + 1))
    triangle_data.columns = dev_periods

    return acc_periods.tolist(), dev_periods, triangle_data


def _is_numeric(val):
    """Check if a value is numeric."""
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def _looks_like_period(val):
    """Check if a value looks like an accident period (year, quarter, date)."""
    s = str(val).strip()
    # Year-like: 2016, 2017, etc.
    if s.isdigit() and 1970 <= int(s) <= 2050:
        return True
    # Float year: 2016.0
    try:
        f = float(s)
        if 1970 <= f <= 2050:
            return True
    except ValueError:
        pass
    # Contains a year
    import re
    if re.search(r'(19|20)\d{2}', s):
        return True
    # Quarter format: 2016Q1, 2016-Q1, etc.
    if re.search(r'Q[1-4]', s, re.IGNORECASE):
        return True
    return False


def parse_columnar_format(df, acc_col=0, dev_col=1, val_col=2):
    """Parse columnar format: columns for accident period, dev period, and value."""
    df = df.copy()
    acc = df.iloc[:, acc_col]
    dev = df.iloc[:, dev_col]
    val = pd.to_numeric(df.iloc[:, val_col], errors='coerce')

    pivot = val.groupby([acc, dev]).sum().unstack()
    acc_periods = [str(x) for x in pivot.index.tolist()]
    dev_periods = pivot.columns.tolist()
    triangle_data = pivot.reset_index(drop=True)
    triangle_data.columns = dev_periods

    return acc_periods, dev_periods, triangle_data


def read_triangle(filepath, sheet_name=None):
    """
    Read a triangle from Excel or CSV.
    Returns: (accident_periods, dev_periods, triangle_df, metadata)
    """
    ext = filepath.lower().split('.')[-1]

    if ext == 'csv':
        df = pd.read_csv(filepath, header=None)
    elif ext in ('xlsx', 'xls', 'xlsm'):
        if sheet_name:
            df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
        else:
            xls = pd.ExcelFile(filepath)
            sheets = xls.sheet_names
            df = pd.read_excel(xls, sheet_name=sheets[0], header=None)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    fmt = detect_triangle_format(df)

    if fmt == "triangle":
        acc_periods, dev_periods, triangle_data = parse_triangle_format(df)
    else:
        acc_periods, dev_periods, triangle_data = parse_columnar_format(df)

    metadata = {
        "format_detected": fmt,
        "n_accident_periods": len(acc_periods),
        "n_dev_periods": len(dev_periods),
        "accident_periods": acc_periods,
        "dev_periods": [str(d) for d in dev_periods],
        "has_negative_values": bool((triangle_data < 0).any().any()),
        "sparsity": float(triangle_data.isna().sum().sum() / triangle_data.size),
    }

    return acc_periods, dev_periods, triangle_data, metadata


def read_premium(filepath, sheet_name=None):
    """Read earned premium data. Expects accident period and premium columns."""
    ext = filepath.lower().split('.')[-1]
    if ext == 'csv':
        df = pd.read_csv(filepath)
    else:
        if sheet_name is None:
            sheet_name = 0
        df = pd.read_excel(filepath, sheet_name=sheet_name)

    # Assume first col = accident period, second col = premium
    premiums = {}
    for _, row in df.iterrows():
        key = str(row.iloc[0]).strip()
        # Clean up float-like year strings (e.g., "2016.0" -> "2016")
        if '.' in key:
            try:
                key = str(int(float(key)))
            except ValueError:
                pass
        premiums[key] = float(row.iloc[1])
    return premiums


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a loss development triangle")
    parser.add_argument("--input", required=True, help="Path to triangle file")
    parser.add_argument("--sheet", default=None, help="Sheet name for Excel files")
    args = parser.parse_args()

    acc, dev, tri, meta = read_triangle(args.input, args.sheet)
    print(json.dumps(meta, indent=2))
    print("\nTriangle Preview:")
    print(tri.to_string())
