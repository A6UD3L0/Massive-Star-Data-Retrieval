# Web Scraping and Data Processing Project

## Introduction

This project involves web scraping star data, downloading and processing the data, and merging it into a comprehensive DataFrame. The primary purpose is to create a valuable dataset for further analysis. The code includes error handling for timeouts and missing elements during the scraping process. The resulting DataFrame is saved as a pickle file for easy access and further exploration.

## Project Details

- **Author(s):** Juan Felipe Agudelo Rios
- **Created on:** 10/09/2022
- **Last modified on:** 14/09/2022

## Usage Instructions

1. **Data Loading and URL Generation:**
   - The script begins by loading star data from a CSV file (`DF_Links.csv`).
   - The function `generara_url` generates URLs based on RA and DEC coordinates.

2. **Web Scraping:**
   - The function `op1` uses Selenium to scrape star data from the generated URLs.
   - The script handles timeouts, missing elements, and saves the downloaded data.

3. **Data Merging:**
   - The function `merge` merges the downloaded data into a single DataFrame (`main_df`).
   - The merged DataFrame is then cleaned and saved as a pickle file (`DataFrame.pkl`).

4. **Additional Processing:**
   - The script includes a function (`quitar_elpunto`) to remove the last character from the 'DEC' column.

5. **Dependencies and Setup:**
   - Ensure the required libraries are installed (`pandas`, `selenium`, `webdriver`, `glob`, `time`, `random`).
   - Adjust the file paths in the script to match your local environment.

6. **Execution:**
   - Run the script to initiate the web scraping, data merging, and processing pipeline.

## Project Completion

Upon successful execution, the script will print "DONE," indicating the completion of the web scraping and data processing tasks. The resulting DataFrame (`DataFrameRafael.pkl`) is ready for further analysis.

Feel free to explore and adapt the code for your specific use case. If you have any questions or encounter issues, refer to the script comments or contact the author.

---

**Note:** This project is part of the author's exploration into data science and web scraping, showcasing techniques for handling real-world data extraction challenges.
