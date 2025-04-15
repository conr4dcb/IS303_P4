# IS 303 Section 003
# Team 2: Elise Chapman, Haley Sommer, Rebecca Mecham, Blake Rogers

# This program will extract, transform, and load sales data into a postgres database using python.
# From postgres, data will be then be fetched, analyzed, and vizualized using python.

# import libraries
import sys
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plot
import openpyxl
import psycopg2 as pg2

# postgre connection information
username = "is303_p4"
password = "is303"
host = "localhost"
port = "5432"
database = "is303"

# import the excel file
df = pd.read_excel ("Retail_Sales_Data.xlsx")

# Create the menu
menu_select = input("Menu: \nIf you want to import data, enter 1. \nIf you want to see summaries of stored data, enter 2. \nEnter any other value to exit the program: ")

# set up menu loop
menu_select = 1

while menu_select == 1 or menu_select ==2 :

    try:
        # get user input to select menu option. close program if 1 or 2 is not entered.
        # Create the menu
        menu_select = int(input("\nMenu: \nIf you want to import data, enter 1. \nIf you want to see summaries of stored data, enter 2. \nEnter any other value to exit the program: "))
        if menu_select < 1 or menu_select > 2:
            sys.exit()
    except ValueError:
        sys.exit()

    # execute code for user menu select option 1
    if menu_select == 1:
        # import the excel file
        df = pd.read_excel("Retail_Sales_Data.xlsx")

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

        # connect to postgre database
        engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

        # push dataframe of sales to postgre database and print out successful import
        df.to_sql('sale', con=engine, if_exists="replace", index=False)
        print("\nYou've imported the excel file into your postgres database.")

    # execute code for user menu select option 2
    elif menu_select == 2: 

        # create connection to database
        conn = pg2.connect(dbname=database, user=username, password=password, host=host, port=port)
        
        # create a cursor
        cur_sale = conn.cursor()

        # execute a query to pull unique categories from sale
        query = """
            SELECT DISTINCT category FROM sale
            ORDER BY category;
        """
        cur_sale.execute(query)

        # fetch the query results from the cursor and convert list of single element tuples to list.
        categories = cur_sale.fetchall()
        list_categories = [row[0] for row in categories]

        # print out list of categories for user to select from
        print("\nThe following categories have been sold")
        for i, category in enumerate(list_categories, start=1):
            print(f"{i}: {category}")
        
        # get user request for data output and check for invalid data
        valid_input = False
        while not valid_input:
            try:
                user_data_request = int(input("Please enter the number of the category you want to see summarized: "))
                if 1 <= user_data_request <= (len(list_categories) + 1) :
                    valid_input = True
                else:
                    print("Number out of range. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

        selected_category = list_categories[user_data_request - 1]

        # get data from postgre into a dataframe
        # REBECCA's query here
        # close connection to postgre
        conn.close()

        #Blake's code here