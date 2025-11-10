odoo.define('bitcoin.snippet_currency_chart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    var _t = core._t;

    var CurrencyChartSnippet = Widget.extend({
        template: 'bitcoin.snippet_currency_chart_template',

        start: function () {
            this._fetchCurrencyData();
        },

        _fetchCurrencyData: function () {
            var currency = 'EUR';  // Replace with your default currency
            var start_date = '2022-01-01';  // Replace with your default start date
            var end_date = '2022-12-31';    // Replace with your default end date

            ajax.jsonRpc('/btcendpoint', 'call', {
                'currency': currency,
                'start_date': start_date,
                'end_date': end_date,
            }).then(this._renderCurrencyChart.bind(this));
        },

        _renderCurrencyChart: function (data) {
            var ctx = this.$('#currencyChart')[0].getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Closing Prices',
                        data: data.closing_prices,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    title: {
                        display: true,
                        text: 'Currency Chart'
                    }
                }
            });
        },
    });

    core.action_registry.add('snippet_currency_chart', CurrencyChartSnippet);

    return {
        CurrencyChartSnippet: CurrencyChartSnippet
    };
});