# IS 303 Section 003
# Team 2: Elise Chapman, Haley Sommer, Rebecca Mecham, Blake Rogers

# This program will extract, transform, and load sales data into a postgres database using python.
# From postgres, data will be then be fetched, analyzed, and vizualized using python.

# import libraries
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import text
import matplotlib.pyplot as plot
import openpyxl
import psycopg2 as pg2

# import the excel file
# pd.read_excel (r"C:\Users\Elise\Desktop\IS303\IS303_P4.xlsx")

# Create the menu
input("Menu: \nIf you want to import data, enter 1. \nIf you want to see summaries of stored data, enter 2. \nEnter any other value to exit the program: ")
