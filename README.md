# PyCryptoScraper

PyCryptoScraper is an script to scrape detailed crypto-currency informations 
from the page [CoinGecko](https://www.coingecko.com).

This version was forked from [patrick0585/PyCryptoScraper](https://github.com/patrick0585/PyCryptoScraper) 
on 2018-05-01. We fixed a couple of issues with parsing of CoinGecko results. We might add some other features later on.

## Dependencies

* [python-lxml](http://lxml.de)

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

or you can list all currencies from CoinGecko by running **Scraper.py** with no parameters.
As of 2018-05-02 this was 1735 currencies and takes about 45 minutes to complete.

    python Scraper.py


## Run Tests

Test can be executed by the following command-line command:
    
    python -m unittest discover -v


## Authors

* **Patrick Kowalik** - *Initial work* - [Crypto-Scraper](https://github.com/patrick0585/PyCryptoScraper)
* **Glenn Wood** - *Debugging and usability improvements* - [PyCrypto-Scraper](https://github.com/GlennWood/PyCryptoScraper)



