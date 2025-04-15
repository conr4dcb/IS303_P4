# IS 303 Section 003
# Team 2: Elise Chapman, Haley Sommer, Rebecca Mecham, Blake Rogers

# This program will extract, transform, and load sales data into a postgres database using python.
# From postgres, data will be then be fetched, analyzed, and vizualized using python.

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import text
import matplotlib.pyplot as plot
import openpyxl
import psycopg2 as pg2

# Haley Sommer: Clean up data
splitNames = df['name'].str.split('_', expand=True) # create the split of first and last names

df.insert(1, 'first_name', splitNames[0]) # insert first_name into the second column

df.insert(2, 'last_name', splitNames[1]) # insert last_name into the third column

df.drop(columns='name', inplace=True) # delete the names column

# form dictionary for categories
productCategoriesDict = {
    'Camera': 'Technology',
    'Laptop': 'Technology',
    'Gloves': 'Apparel',
    'Smartphone': 'Technology',
    'Watch': 'Accessories',
    'Backpack': 'Accessories',
    'Water Bottle': 'Household Items',
    'T-shirt': 'Apparel',
    'Notebook': 'Stationery',
    'Sneakers': 'Apparel',
    'Dress': 'Apparel',
    'Scarf': 'Apparel',
    'Pen': 'Stationery',
    'Jeans': 'Apparel',
    'Desk Lamp': 'Household Items',
    'Umbrella': 'Accessories',
    'Sunglasses': 'Accessories',
    'Hat': 'Apparel',
    'Headphones': 'Technology',
    'Charger': 'Technology'
}

df['category'] = df['product'].map(productCategoriesDict) # use map() to categorize according to the dictionary

df.to_excel("Retail_Sales_Data_Cleaned.xlsx", index=False)