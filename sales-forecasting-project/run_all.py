#!/usr/bin/env python
"""
One-Click Sales Forecasting Pipeline
"""

import os
import pandas as pd
import shutil
from datetime import datetime

PROJECT_ROOT = '/home/sundhar/projects/data-science/sales-forecasting-project'
WINDOWS_DATA_PATH = '/mnt/c/Users/hemas/Desktop/SalesDashboard'

def print_header(message):
    print("\n" + "="*80)
    print(f" {message}")
    print("="*80)

def generate_powerbi_data():
    print_header("GENERATING POWER BI DATA FILES")
    
    df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'cleaned_sales_data.csv'), parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    daily = df.groupby(df.index)['Sales_Amount_Capped'].sum().reset_index()
    daily.columns = ['Date', 'Daily_Sales']
    daily.to_csv(os.path.join(PROJECT_ROOT, 'data', 'daily_summary.csv'), index=False)
    print("✓ daily_summary.csv")
    
    category = df.groupby('Product_Category')['Sales_Amount_Capped'].agg(['sum', 'mean']).reset_index()
    category.columns = ['Category', 'Total_Sales', 'Avg_Sales']
    category.to_csv(os.path.join(PROJECT_ROOT, 'data', 'category_summary.csv'), index=False)
    print("✓ category_summary.csv")
    
    region = df.groupby('Region')['Sales_Amount_Capped'].agg(['sum', 'mean']).reset_index()
    region.columns = ['Region', 'Total_Sales', 'Avg_Sales']
    region.to_csv(os.path.join(PROJECT_ROOT, 'data', 'region_summary.csv'), index=False)
    print("✓ region_summary.csv")
    
    monthly = df.resample('M')['Sales_Amount_Capped'].sum().reset_index()
    monthly.columns = ['Date', 'Monthly_Sales']
    monthly.to_csv(os.path.join(PROJECT_ROOT, 'data', 'monthly_summary.csv'), index=False)
    print("✓ monthly_summary.csv")
    
    df['Weekday'] = df.index.dayofweek
    weekday = df.groupby('Weekday')['Sales_Amount_Capped'].mean().reset_index()
    weekday.columns = ['Weekday', 'Avg_Sales']
    weekday.to_csv(os.path.join(PROJECT_ROOT, 'data', 'weekday_summary.csv'), index=False)
    print("✓ weekday_summary.csv")
    
    print("✓ All files generated")

def copy_to_windows():
    print_header("COPYING FILES TO WINDOWS")
    os.makedirs(WINDOWS_DATA_PATH, exist_ok=True)
    
    data_dir = os.path.join(PROJECT_ROOT, 'data')
    count = 0
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            src = os.path.join(data_dir, file)
            dst = os.path.join(WINDOWS_DATA_PATH, file)
            shutil.copy2(src, dst)
            print(f"✓ {file}")
            count += 1
    print(f"✓ Copied {count} files")

def main():
    start_time = datetime.now()
    print_header("SALES FORECASTING PIPELINE")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    os.chdir(PROJECT_ROOT)
    generate_powerbi_data()
    copy_to_windows()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("PIPELINE COMPLETE")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Data location: {WINDOWS_DATA_PATH}")

if __name__ == "__main__":
    main()
