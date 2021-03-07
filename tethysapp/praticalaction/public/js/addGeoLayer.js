function addMainLayer(ecmwfData1) {
    ecmwfLayer = L.geoJson(ecmwfData1,
        {
            style: function (feature) {
                switch (feature.properties.risk) {
                    case 0.0:
                        return {color: 'blue'};
                    case 4.0:
                        return {color: 'red'};
                    case 3.0:
                        return {color: 'orange'};
                    case 2.0:
                        return {color: 'yellow'};
                }
            },
            onEachFeature: function (feature, layer) {
                if (feature.properties && feature.properties.comid) {
                    layer.on('click', function (e) {
                        $.ajax({
                            type: "GET",
                            data: {
                                "stID": feature.properties.comid,
                            },
                            url: "chartHiwat",
                            dataType: 'json',
                            "beforeSend": function (xhr, settings) {
                                console.log("Before Send");
                                $.ajaxSettings.beforeSend(xhr, settings);
                            },
                            "success": function (data) {
                                $('#long-term-chart').empty();
                                $('#historical-chart').empty();
                                $('#fdc-chart').empty();
                                json_response = data;
                                var dates = [];
                                var values = [];
                                var hdate = []
                                var hval = []

                                // get_forecast_percent(feature.properties.comid);

                                if (json_response.success == "success") {
                                    json_response.dates.forEach(function (element) {
                                        dates.push(element);
                                    });
                                    for (i in json_response.values) {
                                        values.push(parseFloat(json_response.values[i]));
                                    }
                                    for (i in json_response.hval) {
                                        hval.push(parseFloat(json_response.hval[i]));
                                    }
                                    for (i in json_response.hdate) {
                                        hdate.push(json_response.hdate[i]);
                                    }
                                }
                                var avg_series = {
                                    name: 'Forecast Values',
                                    x: dates,
                                    y: values,
                                    type: 'scatter',
                                    line: {
                                        color: 'blue',
                                        width: 2
                                    }
                                };

                                // // Annotation variables
                                var anMax = "Max: " + Math.round(json_response.return_max * 100) / 100;
                                var an20 = "20-yr: " + Math.round(json_response.return_20 * 100) / 100;
                                var an10 = "10-yr: " + Math.round(json_response.return_10 * 100) / 100;
                                var an2 = "2-yr: " + Math.round(json_response.return_max * 100) / 100;
                                var anX = json_response.datetime_end;
                                //
                                var annotation_series = {
                                    x: [anX, anX, anX, anX],
                                    y: [json_response.return_max, json_response.return_20, json_response.return_10, json_response.return_2],
                                    text: [anMax, an20, an10, an2],
                                    mode: 'text',
                                    textposition: 'right',
                                };

                                var annotation_seriesF = {
                                    x: [dates[dates.length - 1], dates[dates.length - 1], dates[dates.length - 1], dates[dates.length - 1]],
                                    y: [json_response.return_max, json_response.return_20, json_response.return_10, json_response.return_2],
                                    text: [anMax, an20, an10, an2],
                                    mode: 'text',
                                    textposition: 'right',
                                };

                                var layout1 = {
                                    title: 'Forecast at Date (Time Zone: UTC) ' + json_response.rundate + ', River ID: ' + json_response.riverID,
                                    autosize: true,
                                    shapes: [{
                                        type: 'rect',
                                        xref: 'x',
                                        yref: 'y',
                                        x0: dates[0],
                                        y0: json_response.return_20,
                                        x1: dates[dates.length - 1],
                                        y1: json_response.return_max,
                                        line: {
                                            width: 0
                                        },
                                        fillcolor: 'rgba(128, 0, 128, 0.4)'
                                    },
                                        {
                                            type: 'rect',
                                            xref: 'x',
                                            yref: 'y',
                                            x0: dates[0],
                                            y0: json_response.return_10,
                                            x1: dates[dates.length - 1],
                                            y1: json_response.return_20,
                                            line: {
                                                width: 0
                                            },
                                            fillcolor: 'rgba(255, 0, 0, 0.4)'
                                        },
                                        {
                                            type: 'rect',
                                            xref: 'x',
                                            yref: 'y',
                                            x0: dates[0],
                                            y0: json_response.return_2,
                                            x1: dates[dates.length - 1],
                                            y1: json_response.return_10,
                                            line: {
                                                width: 0
                                            },
                                            fillcolor: 'rgba(255, 255, 0, 0.4)'
                                        },],
                                    xaxis: {
                                        title: 'Dates',
                                    },
                                    yaxis: {
                                        title: 'Streamflow',
                                        range: [0, json_response.range]
                                    },
                                };
                                var data = [avg_series, annotation_seriesF];

                                var hplot_series = {
                                    name: 'ERA_Interim',
                                    x: hdate,
                                    y: hval,
                                    type: 'scatter'
                                };
                                //

                                //
                                var layout2 = {
                                    title: 'Historical Streamflow (Time Zone: UTC) ' + json_response.rundate + ', River ID: ' + json_response.riverID,
                                    autoSize: true,
                                    showlegend: false,
                                    shapes: [{
                                        type: 'rect',
                                        xref: 'x',
                                        yref: 'y',
                                        x0: json_response.datetime_start,
                                        y0: json_response.return_20,
                                        x1: json_response.datetime_end,
                                        y1: json_response.return_max,
                                        line: {
                                            width: 0
                                        },
                                        fillcolor: 'rgba(128, 0, 128, 0.4)'
                                    },
                                        {
                                            type: 'rect',
                                            xref: 'x',
                                            yref: 'y',
                                            x0: json_response.datetime_start,
                                            y0: json_response.return_10,
                                            x1: json_response.datetime_end,
                                            y1: json_response.return_20,
                                            line: {
                                                width: 0
                                            },
                                            fillcolor: 'rgba(255, 0, 0, 0.4)'
                                        },
                                        {
                                            type: 'rect',
                                            xref: 'x',
                                            yref: 'y',
                                            x0: json_response.datetime_start,
                                            y0: json_response.return_2,
                                            x1: json_response.datetime_end,
                                            y1: json_response.return_10,
                                            line: {
                                                width: 0
                                            },
                                            fillcolor: 'rgba(255, 255, 0, 0.4)'
                                        },],
                                    xaxis: {
                                        title: 'Dates',
                                    },
                                    yaxis: {
                                        title: 'Streamflow'
                                    }
                                };
                                var hdata = [hplot_series, annotation_series];

                                $('#graph').on('shown.bs.modal', function () {
                                    Plotly.newPlot('long-term-chart', data, layout1);
                                    Plotly.newPlot('historical-chart', hdata, layout2);
                                    // Plotly.newPlot('fdc-chart', fdata, layout3);
                                });
                                $('#graphTab a').on('shown.bs.tab', function (e) {
                                    var id = $(this).attr('id');

                                    if (id == 'forecast_tab_link') {
                                        Plotly.newPlot('long-term-chart', data, layout1);
                                    } else if (id == 'historical_tab_link') {
                                        Plotly.newPlot('historical-chart', hdata, layout2);
                                    } else if (id == 'flow_duration_tab_link') {
                                        Plotly.newPlot('fdc-chart', fdata, layout3);
                                    }
                                })
                                // $('#historical_tab_link').click(function () {
                                //     Plotly.newPlot('historical-chart', hdata, layout2);
                                // })
                                //
                                $('#graph').modal('show');

                                var params = {
                                    comid: feature.properties.comid,
                                    cty: 'nepal'

                                }
                                $('#submit-download-forecast').attr({
                                    target: '_blank',
                                    href: 'getForecastCSV?' + jQuery.param(params)
                                });

                                $('#submit-download-interim-csv').attr({
                                    target: '_blank',
                                    href: 'getHistoricCSV?' + jQuery.param(params)
                                });

                            },
                            "error": function (data) {
                                alert("Return Error: " + data.status);
                                alert(data.responseJSON.error);
                            }
                        }) //ajaxCall end
                    });  //Layer on click
                }
            }
            // });
        });
    return ecmwfLayer;
}