from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np

# Initialize the WebDriver (e.g., ChromeDriver)
driver = webdriver.Chrome()

# Define the start date
start_date = datetime(2020, 3, 3)

# Get the current date
current_date = datetime.now()

# Generate the range of dates
date_range = []
current = start_date
end_date = ""
while current <= current_date:
    date_range.append(current.strftime('%m/%d/%Y'))
    current += timedelta(days=1)

# Initialize an empty DataFrame
#columns = ['Date', 'Commodity', 'Unit', 'Minimum', 'Maximum', 'Average']
#df = pd.DataFrame(columns=columns)
df = pd.read_csv('commodity_prices.csv')

# Open the search page
driver.get('https://kalimatimarket.gov.np/price')

# Loop through each date and fetch data
for date in date_range:
    # Find the search input field and enter the search term
    date_input = driver.find_element(By.ID, 'datePricing')  # Adjust the selector as needed
    date_input.clear()  # Clear any existing input
    date_input.send_keys(date)  # Replace with the desired date

    # Submit the form
    submit_button = driver.find_element(By.CSS_SELECTOR, '.comment-btn')  # Adjust the selector as needed
    submit_button.click()

    # Wait for the results to load
    time.sleep(5)  # Adjust the sleep time as needed

    # Parse the results
    table = driver.find_element(By.ID, 'commodityPriceParticular')  # Adjust the selector as needed
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Fetch and store data in the DataFrame
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if cells:
            commodity = cells[0].text if len(cells) > 0 else np.nan
            unit = cells[1].text if len(cells) > 1 else np.nan
            minimum = cells[2].text if len(cells) > 2 else np.nan
            maximum = cells[3].text if len(cells) > 3 else np.nan
            average = cells[4].text if len(cells) > 4 else np.nan

            new_row = pd.DataFrame({'Date': [date], 'Commodity': [commodity], 'Unit': [unit], 'Minimum': [minimum], 'Maximum': [maximum], 'Average': [average]})
            df = pd.concat([df, new_row], ignore_index=True)
           

# Close the browser
driver.quit()

# Print the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('commodity_prices.csv', index=False)