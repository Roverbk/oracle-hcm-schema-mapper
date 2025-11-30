"""
Oracle HCM Schema Migration Tool
--------------------------------
Author: Bhakti Kalyankasture
Description: 
    Automates the mapping of legacy HR data columns to Oracle HDL format using 
    fuzzy string matching (Levenshtein Distance). Handles domain-specific 
    abbreviations and generates upload-ready artifacts.

Dependencies: pandas, thefuzz, openpyxl
"""

import pandas as pd
from thefuzz import process, fuzz
import os
import sys

# Configuration
INPUT_FILE = "legacy_data.xlsx"
OUTPUT_FILE = "Oracle_HDL_Ready.xlsx"
MATCH_THRESHOLD = 70  # Confidence score cutoff (0-100)

# Target Schema: Oracle Fusion HCM Person Object
ORACLE_COLUMNS = [
    "PersonNumber", 
    "PersonFirstName", 
    "PersonLastName", 
    "DateOfBirth",
    "AnnualSalary", 
    "PhoneNumber",
    "AddressLine1"
]

# Domain knowledge base for normalization
# Maps legacy abbreviations to standard business terms
ABBREVIATIONS = {
    "empl": "person",
    "emp": "person",
    "id": "number",
    "ph": "phone",
    "no": "number",
    "l": "last",
    "fname": "firstname",
    "lname": "lastname",
    "curr": "annual",
    "sal": "salary",
    "addr": "address",
    "dob": "dateofbirth"
}

def normalize_header(header):
    """
    Standardizes column headers to facilitate matching against CamelCase targets.
    
    Transformation Pipeline:
    1. Lowercase conversion
    2. Abbreviation expansion (e.g., 'curr' -> 'annual')
    3. Removal of non-alphanumeric characters (underscores/spaces)
    
    Args:
        header (str): Raw column header from legacy system.
        
    Returns:
        str: Normalized string ready for fuzzy comparison.
    """
    cleaned = str(header).lower()
    
    for abbr, full_term in ABBREVIATIONS.items():
        cleaned = cleaned.replace(abbr, full_term)
        
    # Remove delimiters to align with Oracle's CamelCase convention (e.g. PersonNumber)
    return cleaned.replace("_", "").replace(" ", "")

def execute_migration():
    if not os.path.exists(INPUT_FILE):
        print(f"[Error] Input file '{INPUT_FILE}' not found.")
        sys.exit(1)

    print(f"Reading source data: {INPUT_FILE}...")
    try:
        df_source = pd.read_excel(INPUT_FILE)
    except Exception as e:
        print(f"[Error] Failed to read Excel file: {e}")
        sys.exit(1)

    source_headers = df_source.columns.tolist()
    column_mapping = {}

    print("Initiating schema mapping analysis...")
    
    for col in source_headers:
        # Normalize header to improve matching accuracy
        normalized_col = normalize_header(col)
        
        # Extract best match using Token Set Ratio to handle partial strings
        best_match, score = process.extractOne(
            normalized_col, 
            ORACLE_COLUMNS, 
            scorer=fuzz.token_set_ratio
        )
        
        if score >= MATCH_THRESHOLD:
            column_mapping[col] = best_match
            # print(f"Mapped: {col} -> {best_match} ({score}%)") # Debug log
        else:
            # Log unmatched columns for manual review if needed
            continue

    if not column_mapping:
        print("[Warning] No valid column mappings found. Check abbreviation dictionary.")
        sys.exit(0)

    # Transform dataset
    print(f"Generating output. Mapped {len(column_mapping)}/{len(source_headers)} columns.")
    
    df_output = df_source[list(column_mapping.keys())].copy()
    df_output.rename(columns=column_mapping, inplace=True)
    
    # Export
    try:
        df_output.to_excel(OUTPUT_FILE, index=False)
        print(f"Success: Migration artifact saved to {OUTPUT_FILE}")
    except PermissionError:
        print(f"[Error] Could not save to {OUTPUT_FILE}. Is the file open?")

if __name__ == "__main__":
    execute_migration()