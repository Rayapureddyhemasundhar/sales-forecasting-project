"""
Realistic Retail Sales Dataset Generator
Simulates 3 years of daily sales data for multiple categories and regions
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

def generate_sales_data(start_date='2021-01-01', end_date='2023-12-31'):
    """
    Generate realistic retail sales data with:
    - Seasonality (yearly, monthly, weekly)
    - Holiday effects
    - Promotion impacts
    - Regional differences
    - Category-specific patterns
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Product categories with different seasonal patterns
    categories = {
        'Electronics': {'base_trend': 1.2, 'seasonal_amplitude': 0.3, 'holiday_multiplier': 2.0},
        'Clothing': {'base_trend': 1.1, 'seasonal_amplitude': 0.4, 'holiday_multiplier': 1.8},
        'Home & Garden': {'base_trend': 1.05, 'seasonal_amplitude': 0.25, 'holiday_multiplier': 1.6},
        'Sports & Outdoors': {'base_trend': 1.08, 'seasonal_amplitude': 0.35, 'holiday_multiplier': 1.7},
        'Books': {'base_trend': 1.02, 'seasonal_amplitude': 0.2, 'holiday_multiplier': 1.4}
    }
    
    # Regions with different growth rates
    regions = {
        'North': {'population_factor': 0.22, 'growth_rate': 1.05},
        'South': {'population_factor': 0.28, 'growth_rate': 1.08},
        'East': {'population_factor': 0.25, 'growth_rate': 1.06},
        'West': {'population_factor': 0.25, 'growth_rate': 1.07}
    }
    
    # Define holidays and festivals
    holidays = {
        'New Year': '01-01',
        'Valentine Day': '02-14',
        'Independence Day': '07-04',
        'Black Friday': '11-27',
        'Christmas': '12-25',
        'Labor Day': '09-01',
    }
    
    # Generate data
    data = []
    
    for date in dates:
        # Calculate time features
        year = date.year
        month = date.month
        day = date.day
        weekday = date.weekday()
        day_of_year = date.dayofyear
        
        # Base seasonal patterns
        yearly_seasonal = np.sin(2 * np.pi * day_of_year / 365) * 0.3
        
        # Monthly patterns (end of month spike)
        month_end_effect = 1.3 if day >= 25 else 1.0
        
        # Weekly patterns (weekend boost)
        weekend_effect = 1.4 if weekday >= 5 else 1.0
        
        for category, cat_params in categories.items():
            for region, region_params in regions.items():
                
                # Base sales
                base_sales = 1000
                
                # Time trend
                days_since_start = (date - dates[0]).days
                trend = 1 + (days_since_start / 1095) * cat_params['base_trend']
                
                # Category-specific seasonality
                if category == 'Electronics':
                    cat_seasonal = 0.5 if month in [11, 12] else 0
                elif category == 'Clothing':
                    cat_seasonal = 0.3 if month in [3, 4, 9, 10] else 0
                elif category == 'Home & Garden':
                    cat_seasonal = 0.4 if month in [5, 6, 7, 8] else 0
                elif category == 'Sports & Outdoors':
                    cat_seasonal = 0.45 if month in [6, 7, 8] else 0
                else:
                    cat_seasonal = 0.1
                
                # Holiday effect
                holiday_effect = 1.0
                for holiday, holiday_date in holidays.items():
                    if date.strftime('%m-%d') == holiday_date:
                        holiday_effect = cat_params['holiday_multiplier']
                        break
                    elif holiday == 'Black Friday' and month == 11 and 25 <= day <= 30:
                        holiday_effect = cat_params['holiday_multiplier'] * 1.5
                        break
                
                # Promotion
                promotion_active = random.random() < 0.15
                promotion_effect = 1.25 if promotion_active else 1.0
                
                # Calculate final sales
                sales = (base_sales * 
                        trend *
                        (1 + yearly_seasonal * cat_params['seasonal_amplitude']) *
                        month_end_effect *
                        weekend_effect *
                        (1 + cat_seasonal) *
                        holiday_effect *
                        promotion_effect *
                        region_params['population_factor'])
                
                # Add random noise
                noise = np.random.normal(1, 0.05)
                sales = sales * noise
                
                # Units sold
                if category == 'Electronics':
                    avg_price = 500
                elif category == 'Clothing':
                    avg_price = 50
                elif category == 'Home & Garden':
                    avg_price = 75
                elif category == 'Sports & Outdoors':
                    avg_price = 60
                else:
                    avg_price = 20
                
                units_sold = int(sales / avg_price * np.random.uniform(0.8, 1.2))
                
                # Add to dataset
                data.append({
                    'Date': date,
                    'Year': year,
                    'Month': month,
                    'Day': day,
                    'Weekday': weekday,
                    'Product_Category': category,
                    'Region': region,
                    'Sales_Amount': round(sales, 2),
                    'Units_Sold': units_sold,
                    'Promotion_Active': promotion_active,
                    'Holiday': holiday_effect > 1.0,
                    'Weekend': weekday >= 5,
                    'Month_End': day >= 25
                })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating sales data...")
    df = generate_sales_data()
    print(f"Generated {len(df):,} records")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Unique categories: {df['Product_Category'].nunique()}")
    print(f"Unique regions: {df['Region'].nunique()}")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/retail_sales_data.csv', index=False)
    print("\n✓ Data saved to 'data/retail_sales_data.csv'")
    
    # Display sample
    print("\nSample data:")
    print(df.head(10))
    
    # Display summary statistics
    print("\nSummary Statistics:")
    print(f"Total Sales: ${df['Sales_Amount'].sum():,.2f}")
    print(f"Average Daily Sales: ${df.groupby('Date')['Sales_Amount'].sum().mean():,.2f}")
    print(f"Peak Sales Day: ${df.groupby('Date')['Sales_Amount'].sum().max():,.2f}")
