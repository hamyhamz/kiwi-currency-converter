"""
Author : Peter Hamran
Date : 26.06.2019
Projecet : Currency converter for job application at Kiwi
Task link : https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c
Modul : Unit tests for converter funcionality.
"""


import unittest
from converter.converter import MyCurrencyCodes, CurrencyRates, RatesNotAvailableError, Converter, TooManyInputCurrencies
from unittest.mock import patch


def my_simple_rates(input_currency, output_currency):
    if input_currency == 'EUR' and output_currency == ['CZK']:
        return {'CZK': 25.12}


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.cc = MyCurrencyCodes()
        self.cr = CurrencyRates()

    def test_convert_symbol_to_code(self):
        # symbol
        self.assertEqual(self.cc.get_currency_code_from_symbol('€'), ['EUR'], 'Should be EUR.')

    def test_convert_unicode_symbol_to_code(self):
        # unicode
        self.assertEqual(self.cc.get_currency_code_from_symbol(u'\u00a3'), ['GBP', 'SHP'], 'Should be GBP, SHP.')

    def test_nonexistent_symbol_to_code(self):
        # wrong input
        self.assertEqual(self.cc.get_currency_code_from_symbol('a'), [], 'Should be empty.')

    def test_incorrect_input_for_currency_rates(self):
        # incorrect input base currency
        with self.assertRaises(RatesNotAvailableError):
            self.cr.get_rates('AAA')

    def test_correct_input_for_currency_rates(self):
        # correct input
        self.assertIsInstance(self.cr.get_rates('EUR'), dict, 'Should return dictionary.')

    def test_correct_input_for_currency_rates_with_specified_symbols(self):
        # with specified symbols
        self.assertEqual(list(self.cr.get_rates('EUR', ['CAD', 'USD']).keys()), ['CAD', 'USD'], msg='Should be only'
                                                                                                    'CAD and USD.')

    def test_correct_json_format_contains_input_and_output_fields(self):
        amount = 100.5
        input_currency = 'CAD'
        output_currency = 'CZK'

        converter = Converter(amount, input_currency, output_currency)

        try:
            result = converter.convert()
            self.assertListEqual(list(result.keys()), ['input', 'output'], msg='Result json should contain input, and '
                                                                               'output fields.')
        except RatesNotAvailableError:
            self.assertTrue(False, 'Conversion failed. Should not have raised an exception.')

    def test_correct_json_format_input_field(self):
        amount = 100.5
        input_currency = 'CAD'
        output_currency = 'CZK'

        converter = Converter(amount, input_currency, output_currency)

        try:
            result = converter.convert()
            self.assertListEqual(list(result.get('input').keys()), ['amount', 'currency'], msg='Result json input field'
                                                                                               'should contain keys:'
                                                                                               'amount and currency.')
        except RatesNotAvailableError:
            self.assertTrue(False, 'Conversion failed. Should not have raised an exception.')

    def test_correct_json_format_output_field(self):
        amount = 100.5
        input_currency = 'CAD'
        output_currency = '$'

        converter = Converter(amount, input_currency, output_currency)

        try:
            result = converter.convert()
            self.assertListEqual(list(result.get('output').keys()), ['AUD', 'CAD', 'MXN', 'NZD', 'SGD', 'USD'],
                                 msg='Result json input field should contain keys: '
                                     '"AUD", "CAD", "MXN", "NZD", "SGD", "USD"')
        except RatesNotAvailableError:
            self.assertTrue(False, 'Conversion failed. Should not have raised an exception.')

    @patch('converter.converter.CurrencyRates.get_rates', side_effect=my_simple_rates)
    def test_conversion(self, mock_rates):
        amount = 100.0
        input_currency = 'EUR'
        output_currency = 'CZK'

        converter = Converter(amount, input_currency, output_currency)

        try:
            result = converter.convert()
            self.assertListEqual(list(result.get('output').values()), [2512.0])
        except RatesNotAvailableError:
            self.assertTrue(False, 'Conversion failed. Should not have raised an exception.')


if __name__ == '__main__':
    unittest.main()