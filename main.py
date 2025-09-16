"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Adam Seifert
email: seifert.promotion@gmail.com
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup
import time
import os

def zkontroluj_argumenty():
    """
    Kontroluje a validuje vstupní argumenty programu.
    
    Returns:
        tuple: (url, vystup) - URL adresa a název výstupního souboru
        
    Raises:
        SystemExit: Pokud argumenty nejsou validní
    """
    if len(sys.argv) != 3:
        print("Použití: python main.py \"url\" název_souboru.csv")
        sys.exit(1)
    
    url = sys.argv[1]
    vystup = sys.argv[2]
    
    if not url.startswith(("https://volby.cz/pls/ps2017nss/", "https://www.volby.cz/pls/ps2017nss/")):
        print("Chyba: Neplatná URL, musí být z volby.cz")
        sys.exit(1)
    
    if not vystup.endswith('.csv'):
        print("Chyba: Výstupní soubor musí mít příponu .csv")
        sys.exit(1)
    
    return url, vystup

def nacti_stranku(url):
    """
    Načte obsah webové stránky a vrátí parsovaný HTML objekt.
    
    Args:
        url (str): URL adresa stránky k načtení
        
    Returns:
        BeautifulSoup: Parsovaný HTML obsah
        
    Raises:
        SystemExit: Pokud se nepodaří stránku načíst
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)

def ziskej_obce(soup):
    """
    Získává seznam obcí z hlavní stránky.
    
    Args:
        soup (BeautifulSoup): Parsovaný HTML obsah hlavní stránky
        
    Returns:
        dict: Slovník obcí ve formátu {kód: {'nazev': název, 'url': odkaz}}
    """
    obce = {}
    tables = soup.find_all('table')
    
    for table in tables:
        for row in table.find_all('tr')[2:]:  # Přeskočit hlavičku
            cells = row.find_all('td')
            if len(cells) >= 3:
                kod = cells[0].get_text(strip=True)
                nazev = cells[1].get_text(strip=True)
                odkaz = cells[0].find('a')['href'] if cells[0].find('a') else None
                
                if kod and nazev and odkaz:
                    obce[kod] = {
                        'nazev': nazev,
                        'url': f"https://volby.cz/pls/ps2017nss/{odkaz}"
                    }
    return obce

def zpracuj_obec(obec_url):
    """
    Zpracuje detailní data pro jednu obec.
    
    Args:
        obec_url (str): URL adresa detailní stránky obce
        
    Returns:
        dict: Slovník s daty obce ve formátu:
              {'volici': počet, 'obalky': počet, 'platne': počet, 'strany': {strana: hlasy}}
    """
    try:
        soup = nacti_stranku(obec_url)
        data = {
            'volici': None,
            'obalky': None,
            'platne': None,
            'strany': {}
        }

        # Získání základních údajů
        base_table = soup.find('table', {'class': 'table'})
        if base_table:
            rows = base_table.find_all('tr')
            data['volici'] = rows[2].find_all('td')[3].get_text().replace('\xa0', '')
            data['obalky'] = rows[2].find_all('td')[4].get_text().replace('\xa0', '')
            data['platne'] = rows[2].find_all('td')[7].get_text().replace('\xa0', '')

        # Získání výsledků stran - projdeme všechny tabulky s výsledky
        results_tables = soup.find_all('table', {'class': 'table'})
        for table in results_tables:
            for row in table.find_all('tr')[2:]:  # Přeskočit hlavičku
                cells = row.find_all('td')
                if len(cells) >= 4:  # Zkontrolujeme, zda má řádek dostatek buněk
                    strana = cells[1].get_text(strip=True)
                    hlasy = cells[2].get_text(strip=True).replace('\xa0', '')
                    if strana and hlasy.isdigit():
                        data['strany'][strana] = hlasy
        
        return data
    except Exception as e:
        print(f"Chyba u obce: {e}")
        return None
    
def uloz_csv(data, filename):
    """
    Ukládá data do CSV souboru.
    
    Args:
        data (dict): Data obcí k uložení
        filename (str): Název výstupního souboru
        
    Raises:
        SystemExit: Pokud se nepodaří soubor uložit
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Příprava hlavičky
            strany = sorted({strana for obec in data.values() for strana in obec['strany']})
            header = ['Kód obce', 'Název obce', 'Voliči', 'Obálky', 'Platné hlasy'] + strany
            writer.writerow(header)
            
            # Zápis dat
            for kod, info in data.items():
                row = [
                    kod,
                    info['nazev'],
                    info['volici'],
                    info['obalky'],
                    info['platne']
                ]
                row += [info['strany'].get(strana, '0') for strana in strany]
                writer.writerow(row)
        
        print(f"Data uložena do: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Chyba při ukládání: {e}")
        sys.exit(1)

def main():
    """
    Hlavní funkce programu. Řídí celý proces scrapování a ukládání dat.
    """
    url, vystup = zkontroluj_argumenty()
    print(f"Start scrapování: {url}")
    
    # Získání seznamu obcí
    soup = nacti_stranku(url)
    obce = ziskej_obce(soup)
    print(f"Nalezeno obcí: {len(obce)}")
    
    # Zpracování jednotlivých obcí
    results = {}
    for i, (kod, info) in enumerate(obce.items(), 1):
        print(f"Zpracovávám ({i}/{len(obce)}) {info['nazev']}")
        data = zpracuj_obec(info['url'])
        if data:
            results[kod] = {
                'nazev': info['nazev'],
                **data
            }
        time.sleep(0.5)  # Respektujme robots.txt
    
    uloz_csv(results, vystup)

if __name__ == "__main__":
    main()