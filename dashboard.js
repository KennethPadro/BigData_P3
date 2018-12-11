/**
 * Created by manuel on 5/8/18.
 */

// Load the Visualization API and the piechart package.
google.charts.load('current', {'packages': ['corechart', 'bar', 'table']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawModelTotalChart);
google.charts.setOnLoadCallback(drawModel1TotalChart);
google.charts.setOnLoadCallback(drawModel2TotalChart);

function drawModelTotalChart() {
    var allText = "Model 1\t0.7551209359837\nModel 2\t0.7512754854645"

    console.log(allText);

    var allTextLines = allText.split("\n");
    console.log(allTextLines);
    var arrayData = [];
    for (var j=0; j<allTextLines.length; j++) {
            var row = allTextLines[j].split("\t");
            arrayData.push([row[0], parseFloat(row[1], 10)*100]);
    }

    console.log(arrayData);

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Models');
    data.addColumn('number', 'Accuracy');
    data.addRows(arrayData);

    var options = {
        chartArea: {width: '100%'},
        hAxis: {
            title: 'Accuracy',
            minValue: 0,
            maxValue: 100
        },
        vAxis: {
            title: 'Models'
        }
    };

    var chart = new google.charts.Bar(document.getElementById('totalModelCount'));

    chart.draw(data, options);
}

function drawModel1TotalChart() {
   var allText = "0-Does not talk about a medical condition\t543\n1-Does talk about a medical condition\t1564\n2-Ambiguous\t106"

    console.log(allText);

    var allTextLines = allText.split("\n");
    console.log(allTextLines);
    var arrayData = [];
    for (var j=0; j<allTextLines.length; j++) {
            var row = allTextLines[j].split("\t");
            arrayData.push([row[0], parseInt(row[1], 10)]);
    }

    console.log(arrayData);

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Models');
    data.addColumn('number', 'Accuracy');
    data.addRows(arrayData);


    var options = {
      title: 'Model 1'
    };

    var chart = new google.visualization.PieChart(document.getElementById('model1'));

    chart.draw(data, options);
}

function drawModel2TotalChart() {

      var allText = "0-Does not talk about a medical condition\t684\n1-Does talk about a medical condition\t1783\n2-Ambiguous\t97"

    console.log(allText);

    var allTextLines = allText.split("\n");
    console.log(allTextLines);
    var arrayData = [];
    for (var j=0; j<allTextLines.length; j++) {
            var row = allTextLines[j].split("\t");
            arrayData.push([row[0], parseInt(row[1], 10)]);
    }

    console.log(arrayData);

    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Models');
    data.addColumn('number', 'Accuracy');
    data.addRows(arrayData);


    var options = {
      title: 'Model 2'
    };

    var chart = new google.visualization.PieChart(document.getElementById('model2'));

    chart.draw(data, options);
}
