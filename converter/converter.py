"""
Author: Peter Hamran
Date : 25.06.2019
Project : Currency converter for job application at Kiwi
Task link : https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c
Module: Converter class of currency converter project.
"""
import json
import os
import requests

from forex_python.converter import CurrencyCodes

SOURCE_URL = 'https://api.exchangeratesapi.io/latest'


class BadCurrencyFormat(Exception):
    pass


class RatesNotAvailableError(Exception):
    pass


class TooManyInputCurrencies(Exception):
    pass


class Converter():
    """
    Currency converter class. Builds internal data structures as proccess of currency conversion.
    ____________________________________________________________________________________________
    Usage:
    converter = Converter(amount, input_currency, output_currency)

    try:
        converter.convert()     # conversion, will return json structure of converted currencies
    except (RatesNotAvailableError, TooManyInputCurrencies) as e:
        print(e)                # your exception handler here
    """

    def __init__(self, amount, input_currency, output_currency):
        self.input_amount = amount
        self.input_currency = input_currency
        self.output_currency = output_currency
        self.output_amounts = []
        self.rates = {}

    def __str__(self):
        if self.output_currency is None:
            return " ".join([str(self.input_amount), str(self.input_currency), ' -> All currencies'])
        else:
            return " ".join([str(self.input_amount), str(self.input_currency), ' -> ', str(self.output_currency)])

    def convert(self):
        """
        Makes conversion based on provided information from user.

        :return: Json formatted output representing inner state of converter class.
        """
        cr = CurrencyRates()

        self.input_currency = self.__resolve_currency_code(self.input_currency, 'IN')

        if self.output_currency is not None:
            self.output_currency = self.__resolve_currency_code(self.output_currency, 'OUT')
            self.rates = cr.get_rates(self.input_currency, self.output_currency)
        else:
            self.rates = cr.get_rates(self.input_currency)

        for rate in self.rates.values():
            self.output_amounts.append(self.input_amount * rate)

        if self.output_currency is None:
            self.output_currency = []
            for currency in self.rates.keys():
                self.output_currency.append(currency)

        return self.__to_json()

    def __to_json(self):
        """
        Method puts together individual information into final json formatted output.

        :return: Json formatted output representing inner state of converter class.
        """
        app_input = {'amount': self.input_amount, 'currency': self.input_currency}
        app_output = {}

        for currency, amount in zip(self.output_currency, self.output_amounts):
            app_output[currency] = amount

        result = {'input': app_input, 'output': app_output}
        return result

    @staticmethod
    def __resolve_currency_code(currency, currency_type):
        """
        Resolution between input and output currency codes is different due to implementation design. Input currency has
        to be deterministic for the application, therefore closer specification may be needed. In case of output
        currency, in case multiple matches are found, all are included in output of application.

        :param currency: Potentially currency symbol to resolve to currency code.
        :param currency_type: Specifies input or output currency.
        :return: Single currency code (as list due to consistency), or list of currency codes.
        """
        cc = MyCurrencyCodes()
        res_currency = currency

        if currency_type is 'IN':
            # Input currency resolution
            currency_codes = cc.get_currency_code_from_symbol(currency)
            if len(currency_codes) > 1:
                # Currency was given as symbol but matched multiple currency codes
                raise TooManyInputCurrencies(
                    ' '.join(['Given symbol represents multiple currencies. This format is not supporterd',
                              'for input currency. Please choose only one from provided currency code list.',
                              'Currencies:', str(currency_codes)]))
            elif len(currency_codes) is not 0:
                res_currency = currency_codes
        elif currency_type is 'OUT':
            # Output currency resolution
            currency_codes = cc.get_currency_code_from_symbol(currency)

            if currency_codes is not None and len(currency_codes) is not 0:
                return currency_codes
            else:
                # Return currency codes as a list containing single element
                currency_codes.append(res_currency)
                return currency_codes

        return res_currency


class MyCurrencyCodes(CurrencyCodes):
    """
    Class derived from forex_python converter class, used for currency symbol to currency code translation based on
    *currencies.json* file. It´s funcionality is altered to return list of all found conversion matches between symbol
    and code.
    """

    def _get_data_from_symbol(self, symbol):
        """
        Modified method for search in mapping file of currency symbols to currency codes.

        :param symbol: Currency symbol for which currency code is looked for.
        :return: List of currency codes matching given currency symbol.
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        with open(file_path + '/currencies.json') as f:
            currency_data = json.loads(f.read())
        currency_list = (item for item in currency_data if item["symbol"] == symbol)
        return currency_list

    def get_currency_code_from_symbol(self, symbol):
        """
        Modified method used for conversion of currency symbol to currency code.

        :param symbol: Currency symbol to convert.
        :return: Currency code matched to currency symbol provided.
        """
        currency_list = self._get_data_from_symbol(symbol)
        if currency_list:
            result = []
            for currency in currency_list:
                result.append(currency.get('cc'))
            return result
        return None


class CurrencyRates():
    """
    Class for retrieving data structure of conversion rates from API.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_rates(base_currency, symbols=None):
        """
        Handles the communication and parsing of conversion rates provided by selected API.

        :param base_currency: Base currency code for API.
        :param symbols: Currency codes of selected output currencies.
        :return: Dict of conversion rates for selected symbols.
        """
        payload = {'base': base_currency}

        if symbols is not None:
            payload['symbols'] = ','.join(symbols)

        response = requests.get(SOURCE_URL, params=payload)

        if response.status_code == 200:
            return response.json().get('rates', {})
        raise RatesNotAvailableError(" ".join(["Rates for provided currency not found.", response.json().get('error')]))
