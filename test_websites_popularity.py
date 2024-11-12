import requests
import pytest
from bs4 import BeautifulSoup

'''Page URL'''
URL = "https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites"


'''Function to get data from a table'''
def fetch_table_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})

    data = []
    for row in table.find_all('tr')[1:]:  # Title skip
        cols = row.find_all('td')
        if len(cols) > 1:
            site = cols[0].text.strip()
            visitors_count = cols[1].text.strip()
            try:
                popularity = int(cols[4].text.strip().replace(',', ''))  # Remove commas and convert to int
                data.append((site, visitors_count, popularity))
            except ValueError:
                break
    return data


'''Parametrized test'''
@pytest.mark.parametrize("min_popularity",
                         [10 ** 7, int(1.5 * 10 ** 7), 5 * 10 ** 7, 10 ** 8, 5 * 10 ** 8, 10 ** 9, int(1.5 * 10 ** 9)])
def test_popularity(min_popularity):
    table_data = fetch_table_data()
    errors = []

    for site, language, popularity in table_data:
        if popularity < min_popularity:
            errors.append(
                f"{site} (Frontend:{language}) has {popularity} unique visitors per month. (Expected more than {min_popularity})")

    if errors:
        pytest.fail("\n".join(errors))
