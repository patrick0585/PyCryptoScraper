# PyCryptoScraper

PyCryptoScraper is an script to scrape detailed crypto-currency informations 
from the page [CoinGecko](https://www.coingecko.com).

## Dependencies

* [python-lxml](lxml.de)

apt-get -y install python-lxml

* [marshmallow](https://marshmallow.readthedocs.io/en/latest/)

marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.

marshmallow can be installed with pip:

    pip install -U marshmallow --pre
    
## Usage

To run PyCryptScraper you need to instantiate the class **CryptoScraper**.

    cryptoscraper = CryptoScraper(currencies_to_scrape=[dict(name='bitcoin', tags=['usd', 'eur'])])
    
or you can execute the python script **Scraper.py** with certain parameters

    python Scraper.py -c "[{'name':'bitcoin','tags':['usd','eur']}]"

## Run Tests

Test can be executed by the following command-line command:
    
    python -m unittest discover -v


## Authors

* **Patrick Kowalik** - *Initial work* - [Crypto-Scraper](https://github.com/patrick0585/PyCryptoScraper)



