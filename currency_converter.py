#!/usr/bin/env python
"""
Author : Peter Hamran
Date : 25.06.2019
Projecet : Currency converter for job application at Kiwi
Task link : https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c
Module : CLI interface for currency converter application.
"""

import argparse
import sys
from converter.converter import Converter, RatesNotAvailableError, TooManyInputCurrencies
import json


def arg_parse():
    """Argument handler"""
    # Description for help print
    parser = argparse.ArgumentParser(description='Currency converter for job application at Kiwi')

    # Adding all possible arguments
    parser.add_argument('-a', '--amount', dest='currency_amount', metavar='VALUE', required=True, type=float,
                        help='Amount of currency to be converted in floating point format.')
    parser.add_argument('-i', '--input_currency ', dest='input_currency', metavar='CURRENCY', required=True,
                        help='Input currency code (3 letters) or symbol.')
    parser.add_argument('-o', '--output_currency  ', dest='output_currency', metavar='CURRENCY',
                        help='Output currency code (3 letters) or symbol.')

    # Calling actual parsing method
    arguments = parser.parse_args()

    return vars(arguments)


if __name__ == '__main__':
    # CLI arguments parse
    try:
        args = arg_parse()
    except (argparse.ArgumentError, SystemExit) as msg:
        print(json.dumps({'error': 'Argument parse error'}))
        sys.exit(-1)                                        # EXIT FAIL

    converter = Converter(args.get('currency_amount'), args.get('input_currency'), args.get('output_currency'))

    try:
        result = converter.convert()
        print(json.dumps(result, indent=4))
    except (RatesNotAvailableError, TooManyInputCurrencies) as e:
        print(json.dumps({'error': str(e)}))



