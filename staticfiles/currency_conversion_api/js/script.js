$(document).ready(function () {
    $('input[name="source_currency"], input[name="final_currency"], #source_amount').on('change', function () {
        // let _url = 'http://127.0.0.1:8000/api/v1/currency_conversion/convert_currencies/EUR:9.99-PLN'
		// https://currency-conversion-calculator.herokuapp.com/
        let _url = 'http://127.0.0.1:8000/api/v1/currency_conversion/convert_currencies/'
		let source_currency = ''
        let final_currency = ''
        let source_amount = ''
        $('input[name="source_currency"]:checked').each(function () {
            source_currency = $(this).next().text()
        });

        $('input[name="final_currency"]:checked').each(function () {
            final_currency = $(this).next().text()
        })

        $('#source_amount').each(function () {
            source_amount = $(this).val();
        });
        let url = _url + String(source_currency) + ":" + String(source_amount) + "-" + String(final_currency)
        $.ajax({
            url: url,
            contentType: "application/json",
            dataType: 'json',
            success: function (result) {
                $('#result').text(result.final_amount);
            }
        });

    })
});