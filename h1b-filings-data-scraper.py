#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
This script fetches and displays the count of H1B filings by companies based on user input.

Author: Aniruddha Joshi
Date: 10/04/2023

Note: The displayed counts are in descending order.
"""


# In[2]:


# Import the necessary libraries
import requests
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd


# In[3]:


class H1BScraper:
    """
    A scraper class to fetch H1B filing data from h1bdata.info based on user input.
    """
    BASE_URL = "https://h1bdata.info/index.php"
    
    def __init__(self, employer="", job="", city="", year=""):
        """
        Initialize the H1BScraper with optional search parameters.

        Args:
            employer (str): Name of the employer.
            job (str): Job or position title.
            city (str): City of interest.
            year (str): Year of interest.
        """
        self.employer = employer
        self.job = job
        self.city = city
        self.year = year
    
    def build_url(self):
        """
        Constructs the URL for the H1B data search based on the provided input parameters.

        Returns:
            str: The full URL with search parameters.
        """
        params = {
            "em": self.employer,
            "job": self.job.replace(" ", "+"),
            "city": self.city,
            "year": self.year
        }
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{self.BASE_URL}?{query_string}"

    def fetch_data(self):
        """
        Fetch the employer data based on the provided search parameters.

        Returns:
            list: List of employers from the scraped webpage.
        """
        url = self.build_url()
        response = requests.get(url)
    
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to get the page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Extract employer names from the table
        employer_names = [cell.text.strip() for row in soup.find_all('tr') for cell in row.find_all('td', limit=1)]
    
        return employer_names

    def get_dataframe(self):
        """
        Get a DataFrame representation of the fetched data, displaying counts of filings by companies.

        Returns:
            pd.DataFrame: DataFrame containing the employer names and their respective counts.
        """
        employer_names = self.fetch_data()
        employer_count = Counter(employer_names)
    
        # Sort the employers based on the count in descending order
        sorted_employers = sorted(employer_count.items(), key=lambda x: x[1], reverse=True)
    
        # Create and return the DataFrame
        df = pd.DataFrame(sorted_employers, columns=["Employer", "Occurrence"])
        return df


# In[4]:


# Takes user inputs for the search parameters
employer_input = input("Enter the employer (leave empty if not specific): ").lower()
job_input = input("Enter the job/position (leave empty if not specific): ").lower()
city_input = input("Enter the city (leave empty if not specific): ").lower()
year_input = input("Enter the year (leave empty if not specific): ").lower()

# Instantiates the scraper and fetch the data
scraper = H1BScraper(employer_input, job_input, city_input, year_input)

# Displays the DataFrame in Jupyter Notebook
df = scraper.get_dataframe()
df


# In[ ]:




