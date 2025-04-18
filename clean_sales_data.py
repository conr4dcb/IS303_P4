# IS 303 Section 003
# Team 2: Elise Chapman, Haley Sommer, Rebecca Mecham, Blake Rogers, Conrad Bradford

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

# Elise Chapman: import the excel file
df = pd.read_excel ("Retail_Sales_Data.xlsx")

# set up menu loop
while True:

    try:
        # get user input to select menu option. close program if 1 or 2 is not entered.
        # Elise Chapman: Create the menu
        menu_select = int(input("\nMenu: \nIf you want to import data, enter 1. \nIf you want to see summaries of stored data, enter 2. \nEnter any other value to exit the program: "))
        if menu_select < 1 or menu_select > 2:
            print("\nClosing the program.\n")
            sys.exit()
    except ValueError:
        print("Closing the program.\n")
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

        #  Conrad Bradford: connect to postgre database
        engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

        # push dataframe of sales to postgre database and print out successful import
        df.to_sql('sale', con=engine, if_exists="replace", index=False)
        print("\nYou've imported the excel file into your postgres database.")

    # Conrad Bradford: execute code for user menu select option 2
    elif menu_select == 2: 

        # create connection to database
        engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
        conn = engine.connect()


        # execute a query to pull unique categories from sale
        query = """
            SELECT DISTINCT category FROM sale
            ORDER BY category;
        """

        # read query into a dataframe using sqlalchemy
        df_categories = pd.read_sql(text(query), conn)
        # turn category column into series
        categories = df_categories["category"]
        # turn category series into list
        list_categories = categories.tolist()

        # print out list of categories for user to select from
        print("\nThe following categories have been sold")
        for i, category in enumerate(list_categories, start=1):
            print(f"{i}: {category}")
        
        # get user request for data output and check for invalid data
        valid_input = False
        while not valid_input:
            try:
                user_data_request = int(input("Please enter the number of the category you want to see summarized: "))
                if 1 <= user_data_request <= len(list_categories) :
                    valid_input = True
                else:
                    print("Number out of range. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

        selected_category = list_categories[user_data_request - 1]
        #Prints out the sum of total_price, the average total_price, and the sum of quantity_sold for the selected category

        # REBECCA MECHAM get data from postgre into a dataframe
        df_category = pd.read_sql(f"Select * from sale WHERE category = '{selected_category}';", conn)

        print(f"\nSales Summary for {selected_category}: ")

        query1 = """
        SELECT product, SUM(total_price) AS total_sales 
        FROM sale
        WHERE category = :category
        GROUP BY product;"""

        df_total = pd.read_sql( text(query1), conn, params={"category":selected_category})
        cat_sales = df_total["total_sales"].sum()
        print(f"Total Sales:  ${cat_sales:.2f}")

        query2 = """
        SELECT product, AVG(total_price) AS average_sales 
        FROM sale
        WHERE category = :category
        GROUP BY product; """
        df_average = pd.read_sql( text(query2), conn, params={"category":selected_category})
        cat_avg = df_average["average_sales"].mean()
        print(f"Average Sales: ${cat_avg:.2f}")

        query3 = """
        SELECT product, SUM(quantity_sold) AS total_quantity_sold 
        FROM sale
        WHERE category = :category
        GROUP BY product;
        """
        df_qty = pd.read_sql( text(query3), conn, params={"category":selected_category})
        cat_qty = df_qty["total_quantity_sold"].sum()
        print(f"Total Quantity Sold: {cat_qty:.0f} units")

        # close connection to postgre
        conn.close()

        # BLAKE ROGERS Using group by on the product to get one row for each product,
        # and then calculating the sum of total prices for each of those products
        dfProductSales = df_category.groupby('product')['total_price'].sum()

        # Creating the chart
        dfProductSales.plot(kind='bar')  # creates the chart
        plot.title(f"Total Sales in {selected_category}")  # dynamic title
        plot.xlabel("Product")  # label for the x-axis
        plot.ylabel("Total Sales ($)")  # label for the y-axis
        plot.tight_layout()  # avoids label cut-off
        plot.show()  # makes the chart pop up on the screen