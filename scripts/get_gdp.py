from bs4 import BeautifulSoup
import requests
import os
import csv


# Get GDP PPP data from Wikipedia
URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita'
soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
table = soup.find('table', {'class': 'wikitable'})

countries = {}
for row in table.find_all('tr')[1:]:
    cell = [cell.get_text(strip=True) for cell in row.find_all('td')]
    if cell:
        country = cell[0].strip('\u202f*')
        gdp_per_capita = cell[2].replace(',', '')
        if gdp_per_capita.isnumeric():
            countries[country] = int(gdp_per_capita)


# Write GDP data to CSV
TEMPFILE = 'temp.csv'
WRITEFILE = 'country_artists.csv'

os.chdir('../data')

with open(WRITEFILE) as csvfile:
    reader = csv.reader(csvfile)

    with open(TEMPFILE, 'w') as tempfile:
        writer = csv.writer(tempfile)

        for row, data in enumerate(reader):
            if row == 0:
                writer.writerow(data)
                continue
            
            country, ratio, _, artists = data
            if country not in countries:
                print(f"Warning: {country} not found in GDP data")
            writer.writerow([country, ratio, countries.get(country, ''), artists])

os.replace(TEMPFILE, WRITEFILE)
