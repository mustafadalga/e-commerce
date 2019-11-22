$(document).ready(function () {

    function renderChart(id, data, labels) {

        var ctx = $("#" + id);
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '# Sales Per Day',
                    data: data,
                    backgroundColor: 'rgba(0, 158, 29, 0.45)',
                    borderColor: 'rgba(0, 158, 29, 1)',
                    borderWidth: 1

                }]
            },
        });
    }

    function getSalesData(id, type) {
        var url = "/analytics/sales/data/";
        var method = "GET";
        var data = {"type": type};
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function (responseData) {
                renderChart(id, responseData.data, responseData.labels)
            },
            error: function (error) {
                $.alert("An error occurred")
            }
        });
    }

    var chartsToRender = $(".cfe-render-chart")
    $.each(chartsToRender, function (index, html) {
        var $this = $(this)
        getSalesData($this.attr("id"), $this.attr("data-type"))
    })

})