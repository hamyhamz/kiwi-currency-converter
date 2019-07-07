#!/usr/bin/env python
"""
Author : Peter Hamran
Date : 25.06.2019
Projecet : Currency converter for job application at Kiwi
Task link : https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c
Module : API interface for currency converter application.
"""
import json
import requests_cache

from flask import Flask, request, jsonify
from converter.converter import RatesNotAvailableError, TooManyInputCurrencies, Converter
from flask_api import status

app = Flask(__name__)

# Request cache set to 10 minutes to avoid server API spamming in case of occasional spike usage
requests_cache.install_cache('currency_conversion_cache', backend='sqlite', expire_after=600)


@app.route('/currency_converter', methods=['GET'])
def get():
    if request.args.get('amount') is not None:
        if request.args.get('input_currency') is not None and request.args.get('output_currency') is not None:
            try:
                # If all arguments are present
                converter = Converter(float(request.args.get('amount')), request.args.get('input_currency'),
                                      request.args.get('output_currency'))
                return jsonify(converter.convert()), status.HTTP_200_OK
            except (RatesNotAvailableError, TooManyInputCurrencies, ValueError) as e:
                return json.dumps({'error': str(e)}), status.HTTP_400_BAD_REQUEST
        elif request.args.get('input_currency') is not None:
            try:
                # If output_currency is ommited
                converter = Converter(float(request.args.get('amount')), request.args.get('input_currency'), None)
                return jsonify(converter.convert()), status.HTTP_200_OK
            except (RatesNotAvailableError, TooManyInputCurrencies, ValueError) as e:
                return json.dumps({'error': str(e)}), status.HTTP_400_BAD_REQUEST
        else:
            return jsonify({'error': 'Input argument was not set.'}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({'error': 'Amount was not specified in parameters.'}), status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':
    app.run(debug=True)