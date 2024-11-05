# src/data_quality_checker.py

import argparse
import pandas as pd
import yaml
import os
from datetime import datetime
from pathlib import Path
import json
import numpy as np

def generate_detailed_report(df, original_df):
    """Generate a detailed report of all data quality checks"""
    report_sections = []
    
    # Report Header
    report_sections.append("DATA QUALITY ANALYSIS REPORT")
    report_sections.append("=========================")
    report_sections.append(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Basic Dataset Information
    report_sections.append("1. DATASET OVERVIEW")
    report_sections.append("-----------------")
    report_sections.append(f"Original rows: {len(original_df)}")
    report_sections.append(f"Cleaned rows: {len(df)}")
    report_sections.append(f"Number of columns: {len(df.columns)}")
    report_sections.append(f"Memory usage: {df.memory_usage().sum() / 1024 / 1024:.2f} MB\n")
    
    # Column Information
    report_sections.append("2. COLUMN INFORMATION")
    report_sections.append("-------------------")
    for col in df.columns:
        dtype = str(df[col].dtype)
        report_sections.append(f"\nColumn: {col}")
        report_sections.append(f"Type: {dtype}")
    report_sections.append("")
    
    # Missing Values Analysis
    report_sections.append("3. MISSING VALUES ANALYSIS")
    report_sections.append("------------------------")
    missing_vals = original_df.isnull().sum()
    missing_percentages = (missing_vals / len(original_df)) * 100
    for col, count in missing_vals.items():
        if count > 0:
            report_sections.append(f"Column '{col}': {count} missing values ({missing_percentages[col]:.2f}%)")
    report_sections.append("")
    
    # Duplicate Analysis
    report_sections.append("4. DUPLICATE ANALYSIS")
    report_sections.append("-------------------")
    duplicates = original_df.duplicated().sum()
    report_sections.append(f"Total duplicate rows: {duplicates}")
    report_sections.append(f"Percentage of duplicates: {(duplicates/len(original_df))*100:.2f}%\n")
    
    # Statistical Summary
    report_sections.append("5. STATISTICAL SUMMARY")
    report_sections.append("--------------------")
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    
    if len(numeric_columns) > 0:
        for col in numeric_columns:
            report_sections.append(f"\nColumn: {col}")
            report_sections.append("Basic Statistics:")
            report_sections.append(f"- Count: {df[col].count()}")
            report_sections.append(f"- Mean: {df[col].mean():.2f}")
            report_sections.append(f"- Std: {df[col].std():.2f}")
            report_sections.append(f"- Min: {df[col].min()}")
            report_sections.append(f"- 25%: {df[col].quantile(0.25):.2f}")
            report_sections.append(f"- Median: {df[col].median():.2f}")
            report_sections.append(f"- 75%: {df[col].quantile(0.75):.2f}")
            report_sections.append(f"- Max: {df[col].max()}")
    
    # Categorical Columns Analysis
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        report_sections.append("\n6. CATEGORICAL COLUMNS ANALYSIS")
        report_sections.append("----------------------------")
        for col in categorical_columns:
            report_sections.append(f"\nColumn: {col}")
            value_counts = df[col].value_counts()
            report_sections.append(f"Unique values: {df[col].nunique()}")
            report_sections.append("Top 5 most frequent values:")
            for val, count in value_counts.head().items():
                report_sections.append(f"- {val}: {count} ({(count/len(df))*100:.2f}%)")
    
    # Data Cleaning Summary
    report_sections.append("\n7. DATA CLEANING SUMMARY")
    report_sections.append("----------------------")
    rows_removed = len(original_df) - len(df)
    report_sections.append(f"Rows in original dataset: {len(original_df)}")
    report_sections.append(f"Rows in cleaned dataset: {len(df)}")
    report_sections.append(f"Total rows removed: {rows_removed}")
    report_sections.append(f"Percentage of data retained: {(len(df)/len(original_df))*100:.2f}%")
    
    return "\n".join(report_sections)

def run_data_quality_checks(df):
    """Run data quality checks and clean the data"""
    # Store original dataframe for comparison
    original_df = df.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values (example strategy - you can modify this)
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].mean())
    
    # Generate the report
    report_text = generate_detailed_report(df, original_df)
    
    return df, report_text

def main():
    parser = argparse.ArgumentParser(description='Data Quality Checker')
    parser.add_argument('--input-csv', required=True, help='Path to input CSV file')
    parser.add_argument('--output-csv', required=True, help='Path to output CSV file')
    parser.add_argument('--report-path', required=True, help='Path to save the report')
    parser.add_argument('--config-path', required=True, help='Path to config file')
    
    args = parser.parse_args()
    
    try:
        print("\nStarting data quality analysis...")
        
        # Check if input file exists
        if not os.path.exists(args.input_csv):
            raise FileNotFoundError(f"Input file not found: {args.input_csv}")
        
        # Create output directories if they don't exist
        os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
        os.makedirs(os.path.dirname(args.report_path), exist_ok=True)
        
        # Read input data
        df = pd.read_csv(args.input_csv)
        print(f"Successfully loaded data with {len(df)} rows and {len(df.columns)} columns")
        
        # Run quality checks and get report
        cleaned_df, report_text = run_data_quality_checks(df)
        
        # Save cleaned data
        cleaned_df.to_csv(args.output_csv, index=False)
        print(f"\nCleaned data saved to: {args.output_csv}")
        
        # Save report
        with open(args.report_path, 'w') as f:
            f.write(report_text)
        
        print(f"Detailed quality report saved to: {args.report_path}")
        print("\nData quality analysis completed successfully!")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()