odoo.define('volunteer_management.form_enhancements', function (require) {
    'use strict';

    $(document).ready(function () {
        // Fix scrolling issues
        $('html, body').css({
            'height': 'auto',
            'overflow-y': 'auto'
        });

        // Remove any fixed positioning that might prevent scrolling
        $('.o_main_content').css({
            'position': 'relative',
            'height': 'auto',
            'overflow': 'visible'
        });

        // Add focus effects
        $('.form-control').focus(function() {
            $(this).parent().addClass('focused');
        }).blur(function() {
            $(this).parent().removeClass('focused');
        });

        // Form submission handling
        $('form').submit(function(e) {
            var $btn = $(this).find('button[type="submit"]');
            $btn.addClass('btn-loading');
            $btn.prop('disabled', true);
        });

        // Date input improvements
        if (typeof Modernizr !== 'undefined') {
            $('input[type="date"]').each(function() {
                if (!Modernizr.inputtypes.date) {
                    $(this).attr('type', 'text').datepicker({
                        format: 'yyyy-mm-dd',
                        autoclose: true,
                        todayHighlight: true
                    });
                }
            });
        }
    });
});