import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from functions import *

'''This program will take the data that is stored and repeatedly parse through
it using the optimal setting for rolling averages and using the intersection
of these rolling averages, it will prompt the user to buy or sell a certain
stock'''

def main():
    
    '''Takes the optimal settings for rolling averages'''
    settings = optimal_settings()
    for file in os.listdir("../../stored_data/"):
        if file.endswith(".csv"):
            ticker = file[:file.find(".csv")]
            parse_old_data(settings,ticker)

while True:
    main()
