from odoo import http
from odoo.http import request
from datetime import datetime

import yfinance as yf


class YourOdooController(http.Controller):
    @http.route('/btcendpoint', type='json', auth='public', website=True)
    def fetch_currency_data(self, currency, start_date, end_date):
        try:
            # Convert start_date and end_date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Fetch data for the selected currency and dates using yfinance
            data = self.get_currency_data(currency, start_date, end_date)

            return {
                'dates': data.index.strftime('%Y-%m-%d').tolist(),
                'closing_prices': data['Close'].tolist(),
            }
        except Exception as e:
            return {'error': str(e)}

    def get_currency_data(self, currency, start_date, end_date):
        # Use yfinance to fetch historical data for the selected currency
        # Replace 'USD' with the base currency if needed
        currency_pair = f'{currency}USD=X'
        currency_data = yf.download(currency_pair, start=start_date, end=end_date)

        return currency_data
