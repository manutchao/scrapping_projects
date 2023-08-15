# OuiFM Scrapper

OuiFM Scrapper is a Python Script for extract the songs streamed on the radio

## Installation

```bash
pipenv install
```

## Usage

```python
# Extract songs on the radio OUI FM BRING THE NOISE 1st january 2023 between 12h and 13h
pipenv run python main.py --radio="OUI FM BRING THE NOISE" --horodatage="2023-01-01 12:50"

# Extract songs on the radio OUI FM 1st january 2023 between 12h and 13h
pipenv run python main.py --horodatage="2023-01-01 12:50"
