# Currency Converter
A practical task for first round of interview at Kiwi.com for postion of Junior Python Dev.
All task information can be found here: https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c

## Introduction
Project's aim was to create currency converter application as a real-life production ready project. 
Created sollution contains two application standpoints. One built as CLI tool and another as a web 
API application. Both of them make heavy use of backend class providing conversion rates based on
accessible free web API https://ratesapi.io/ . 

## Technologies
Application was developed under python 3.7

### CLI application
CLI interface makes use of these python libraries:
* argparse - Parsing of command line options
* sys 
* json - Output format of application

### API application
API interface makes use of these python libraries:
* json - Output format of application
* requests_cache - To avoid potential request spamming during spike usage
* flask - API interface
* flask_api - API return status

### Converter (backend)
Backend class that makes the conversions happen
* json - Output format of application
* os - File handling
* requests - Communication with currency rates API
* forex_python - For currency symbol to currecy code translation (modified)

## Running an application
Run a `currency_converter.py` file with appropriate parameters, or `currency_converter_api.py` for appropriate behaviour.

## Parameters
* `amount` - Specifies amount for conversion. Type: *FLOAT*
* `input_currency` - Specifies input currency code. Format: *3 letters name or currency symbol*
* `output_currency` - Specifies requested/output currency. Format: *3 letters name or currency symbol*
*While using CLI version of application -h/--help option can be used for quick options listing.*

## Features
Some currency symbols may represent multiple currency codes. Therefore:
* When currency symbol with features mentioned above is set as `input_currency`, conversion ends with an error. 
Becouse application can not decide which of resulting currencies to use. Json format with list of potentially more specific
currency codes is returned.
* When currency symbol with features mentioned above is set as `output_currency`, specified `input_currency` is then
converted to all currencies yielded from provided `output_currency`.

## Usage example

### CLI
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2543.4
    }
}
```

### API
```
GET /currency_converter?amount=42.42&input_currency=USD HTTP/1.1
{
    {
  "input": {
    "amount": 42.42, 
    "currency": "USD"
  }, 
  "output": {
		"AUD": 60.413175054666, 
		"BGN": 73.49843728000201, 
		"BRL": 161.961123316986, 
		"CAD": 55.426344791202, 
		"CHF": 41.788660522686, 
		"CNY": 291.494697023544, 
		"CZK": 955.8028703055, 
        .
        .
        .
        }
}
```