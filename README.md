🗳️ Elections Scraper (Czech Parliamentary Elections 2017)
A Python-based web scraping tool designed to extract and process election results from the official Czech Statistical Office website (volby.cz). It automates the collection of data for specific territorial units and exports it into a structured CSV format.

🇬🇧 English Version
🎯 Project Overview
This tool simplifies the acquisition of election data for the 2017 Parliamentary Elections. By providing a specific territorial URL, the script crawls through all municipalities within that unit, collects voter participation metrics, and tallies votes for all competing political parties.

✨ Key Features
Automated Data Extraction: Scrapes codes, names, and results for all municipalities in a selected region.

Complete Results: Captures registered voters, issued envelopes, and total valid votes.

Dynamic Party Mapping: Automatically identifies all competing parties and assigns their respective vote counts.

CSV Export: Generates a ready-to-use dataset for further statistical analysis.

🛠️ Tech Stack
Language: Python 3.x

Libraries: * requests (for HTTP requests)

beautifulsoup4 (for HTML parsing)

🚀 Usage
Install Dependencies:

Bash

pip install -r requirements.txt
Run the Scraper: Provide the territorial URL (from volby.cz) and the desired output filename as arguments:

Bash

python main.py "URL_ADDRESS" "output_filename.csv"
🇨🇿 Česká verze
📌 Popis projektu
Tento program automatizuje stahování výsledků parlamentních voleb z roku 2017. Uživatel zadá URL adresu konkrétního územního celku a program následně projde všechny obce, posbírá data o volební účasti a hlasy pro jednotlivé strany.

✨ Funkcionality
Hromadné zpracování: Automaticky identifikuje všechny obce v daném okrese.

Strukturovaný výstup: Data o voličích a obálkách jsou přehledně seřazena.

Dynamické sloupce: Program sám rozpozná kandidující strany a vytvoří pro ně sloupce v CSV.

📊 Ukázka výstupu / Output Example
Console:

Plaintext

Scraping: Benešov region...
Found municipalities: 114
Processing (1/114) Benešov
Processing (2/114) Bernartice
...
Data saved to: results_benesov.csv
CSV Structure: | code | location | registered | envelopes | valid | ODS | ČSSD | ... | | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | | 529303 | Benešov | 13125 | 8234 | 8192 | 1120 | 540 | ... |

💡 Tip pro sekci "About" na GitHubu:
Automated Python web scraper for the 2017 Czech Parliamentary Elections. Extracts voter statistics and party results into CSV using BeautifulSoup4 and Requests.

🐍 Příklad komentovaného kódu (v angličtině):
V části, kde získáváš data z tabulky, by kód mohl vypadat takto:

Python

import requests
from bs4 import BeautifulSoup

def get_municipality_data(url):
    # Fetch the HTML content from the given municipality URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract voter participation statistics from the specific table headers
    registered = soup.find('td', {'headers': 'sa2'}).text
    envelopes = soup.find('td', {'headers': 'sa3'}).text
    
    # Return a dictionary for easy mapping to CSV rows
    return {
        "registered": registered.replace('\xa0', ''), # Clean non-breaking spaces
        "envelopes": envelopes.replace('\xa0', '')
    }
👤 Autor / Author: Adam Seifert

Kontakt: seifert.promotion@gmail.com

Projekt vznikl v rámci kurzu Datový Analytik s Pythonem od Engeto.
