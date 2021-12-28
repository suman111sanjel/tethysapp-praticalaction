// This code generates table at the end of forecast chart in modal


function get_forecast_percent(comid) {
    $('#mytable').addClass('hidden');
    $.ajax({
        url: 'forecastpercent',
        type: 'GET',
        data: {
            comid: comid,
        },
        error: function() {
            $('#info').html(
                '<p class="alert alert-danger" style="text-align: center"><strong>An unknown error occurred while retrieving the forecast table</strong></p>'
            );
            $('#info').removeClass('hidden');

            setTimeout(function() {
                $('#info').addClass('hidden');
            }, 5000);
        },
        success: function(data) {
            $('#tbody').empty();
            var tbody = document.getElementById('tbody');

            var columNames = {
                two: 'Percent Exceedance (2-yr)',
                ten: 'Percent Exceedance (10-yr)',
                twenty: 'Percent Exceedance (20-yr)'
            };

            for (var object1 in data) {
                if (object1 == 'dates') {
                    cellcolor = '';
                } else if (object1 == 'two') {
                    cellcolor = 'yellow';
                } else if (object1 == 'ten') {
                    cellcolor = 'red';
                } else if (object1 == 'twenty') {
                    cellcolor = 'purple';
                }
                if (object1 == 'percdates') {
                    var tr = '<tr id=' + object1.toString() + '><th>Dates</th>';
                    for (var value1 in data[object1]) {
                        tr +=
                            '<th>' + data[object1][value1].toString() + '</th>';
                    }
                    tr += '</tr>';
                    tbody.innerHTML += tr;
                } else {
                    var tr =
                        '<tr id=' +
                        object1.toString() +
                        '><td>' +
                        columNames[object1.toString()] +
                        '</td>';
                    for (var value1 in data[object1]) {
                        if (parseInt(data[object1][value1]) == 0) {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'zero>' +
                                data[object1][value1].toString() +
                                '</td>';
                        } else if (parseInt(data[object1][value1]) <= 20) {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'twenty>' +
                                data[object1][value1].toString() +
                                '</td>';
                        } else if (parseInt(data[object1][value1]) <= 40) {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'fourty>' +
                                data[object1][value1].toString() +
                                '</td>';
                        } else if (parseInt(data[object1][value1]) <= 60) {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'sixty>' +
                                data[object1][value1].toString() +
                                '</td>';
                        } else if (parseInt(data[object1][value1]) <= 80) {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'eighty>' +
                                data[object1][value1].toString() +
                                '</td>';
                        } else {
                            tr +=
                                '<td class=' +
                                cellcolor +
                                'hundred>' +
                                data[object1][value1].toString() +
                                '</td>';
                        }
                    }
                    tr += '</tr>';
                    tbody.innerHTML += tr;
                }
            }

            $('#twenty').prependTo('#mytable');
            $('#ten').prependTo('#mytable');
            $('#two').prependTo('#mytable');
            $('#percdates').prependTo('#mytable');
            $('#mytable').removeClass('hidden');
        }
    });
}