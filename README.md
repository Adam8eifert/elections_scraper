# Projekt Elections Scraper

Třetí projekt do Engeto Online Python Akademie - scraper výsledků voleb z roku 2017.

## Popis projektu

Tento program stahuje výsledky parlamentních voleb z roku 2017 pro vybraný územní celek z webu [volby.cz](https://volby.cz/). Data ukládá do CSV souboru pro další zpracování.

## Instalace knihoven

Pro správný běh programu je potřeba mít nainstalované knihovny uvedené v souboru `requirements.txt`. Pro instalaci použijte příkaz:

```
pip install -r requirements.txt
```

## Spuštění programu

Program se spouští z příkazové řádky dvěma povinnými argumenty:

```
python main.py "url_uzemniho_celku" <vystupni_soubor.csv>
```

### Argumenty programu

1. `<url_uzemniho_celku>` - URL adresa stránky s výsledky voleb pro územní celek z webu [volby.cz](https://volby.cz/)
2. `<vystupni_soubor.csv>` - Název výstupního CSV souboru

### Příklad spuštění

```
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky.csv
```

## Ukázka výstupu

Po spuštění programu s výše uvedenými argumenty bude výstup v konzoli vypadat přibližně takto:

```
Start scrapování: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Nalezeno obcí: 114
Zpracovávám (1/114) Benešov
Zpracovávám (2/114) Bernartice

...
Zpracovávám (113/114) Zdislavice
Zpracovávám (114/114) Zvěstov
Data uložena do: C:\Users\seife\Documents\engeto\projekty\main\vysledky.csv
```

Výstupní CSV soubor bude obsahovat následující sloupce:
- kód obce
- název obce
- počet registrovaných voličů
- počet vydaných obálek
- počet platných hlasů
- sloupce pro jednotlivé kandidující strany s počty hlasů




