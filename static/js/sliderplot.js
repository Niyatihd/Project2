//##########################################################
//Get the values for slider dropdown
//##########################################################
d3.json('/sliderdropdownlist', (error, response) => {
    if (error) return console.warn(error);

    var todoList = document.querySelector("#selectddl");
    todoHTML = "<option value='Development Plans' selected='selected'>Development Plans</option>";
    for (var i = 0; i < response.length; i++) {
        todoHTML += "<option>" + response[i] + "</option>";
    }
    todoList.innerHTML = todoHTML;
});


//##########################################################
//Post and get the values for sliderplot to and from app.py
//##########################################################
/** Update table from user selected options called at each dropdown selection  */
// function updateSliderPlot_test(){
//     // change event
//     $('#selectddl').change(function(){
//         console.log($(this).find(':selected').text());
//         console.log($(this).find(':selected').val());
//     });
//   }




function optionChanged(ddl1) {

    console.log("on selection")
    console.log(ddl1)
    var development = (ddl1 == "Development Plans")?"":ddl1;
    console.log(development)
    var selection = { developmentPlan: development}
    console.log(selection) 
    console.log( JSON.stringify(selection)) 

    fetch('/sliderdata1', {
        body: JSON.stringify(selection), // must match 'Content-Type' header
        headers: {
          'content-type': 'application/json'
        },
        method: 'POST', 
      }).then((response) => { 
        console.log(response)})
    //   }).then(text => {
        //  html  (bare table) --> flask app must return to_html()
    //     var table = document.querySelector("#table");
    //     textclean = text.replace(/"/g,' ');
    //     textclean2 = textclean.replace(/\\n/g,'');
    //     table.innerHTML = textclean2;
    //   });
  
    
    // }).then((response) => { 
    //     return response
    //     console.log(response)
    //   return response.text();
    // }).then(text => {
    //   //  html  (bare table) --> flask app must return to_html()
    //   var table = document.querySelector("#table");
    //   textclean = text.replace(/"/g,' ');
    //   textclean2 = textclean.replace(/\\n/g,'');
    //   table.innerHTML = textclean2;
    // });
}

// function updateSliderPlot(){
//     var ddl1 = document.querySelector("#selectddl");
//     drawSliderPlot(ddl1);
// }

// updateSliderPlot();



// function configureDropDownLists() {
$(document).ready(function () {
    function getExportServer() {
        return 'https://www.jqwidgets.com/export_server/export.php';
    }

    // prepare chart data
    var sampleData = [
        { Category: 'Non-Residential(sq.ft)', MarketShare: 0 },
        { Category: 'Residential(sq.ft)', MarketShare: 0 },
        { Category: 'Jobs', MarketShare: 0 },
        { Category: 'People', MarketShare: 0 },
        { Category: 'Students', MarketShare: 0 }
    ]

    // prepare jqxChart settings
    var settings = {
        title: "Development Plan Overview",
        description: "",
        showLegend: false,
        enableAnimations: true,
        padding: { left: 20, top: 5, right: 20, bottom: 5 },
        titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
        source: sampleData,
        xAxis:
            {
                dataField: 'Category',
                showGridLines: true,
                flip: false
            },
        colorScheme: 'scheme01',
        seriesGroups:
            [
                {
                    type: 'column',
                    columnsGapPercent: 100,
                    toolTipFormatSettings: { thousandsSeparator: ',' },
                    valueAxis:
                    {
                        unitInterval: 10,
                        maxValue: 100,
                        minValue: 0,
                    },
                    series: [
                            { dataField: 'MarketShare', displayText: 'Market share', formatSettings: { prefix: "%"} }
                        ]
                }
            ]
    };

    // setup the chart
    $('#chartContainer').jqxChart(settings);

    $("#jqxslider1").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });
    $("#jqxslider2").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });
    $("#jqxslider3").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });
    $("#jqxslider4").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });
    $("#jqxslider5").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });
    $("#jqxslider6").jqxSlider({ width: 700, min: 0, max: 100, value: 0, step: 5 });

    $('#jqxslider1').on('change', function (event) {
        var value = event.args.value;
        sampleData[0].MarketShare = value;
        sampleData[2].MarketShare = value;
        $('#chartContainer').jqxChart("update");
    });
    
    $('#jqxslider2').on('change', function (event) {
        var value = event.args.value;
        sampleData[1].MarketShare =value;
        $('#chartContainer').jqxChart("update");
    });
    
    $('#jqxslider3').on('change', function (event) {
        var value = event.args.value;
        sampleData[2].MarketShare =value;
        $('#chartContainer').jqxChart("update");
    });
    
    $('#jqxslider4').on('change', function (event) {
        var value = event.args.value;
        sampleData[3].MarketShare =value;
        $('#chartContainer').jqxChart("update");
    });
    
    $('#jqxslider5').on('change', function (event) {
        var value = event.args.value;
        sampleData[4].MarketShare =value;
        $('#chartContainer').jqxChart("update");
    });

    $('#jqxslider6').on('change', function (event) {
        var value = event.args.value;
        sampleData[4].MarketShare =value;
        $('#chartContainer').jqxChart("update");
    });

    $("#jpegButton").jqxButton({});
    $("#pngButton").jqxButton({});
    $("#pdfButton").jqxButton({});
    $("#jpegButton").click(function () {
        // call the export server to create a JPEG image
        $('#chartContainer').jqxChart('saveAsJPEG', 'myChart.jpeg', getExportServer());
    });
    $("#pngButton").click(function () {
        // call the export server to create a PNG image
        $('#chartContainer').jqxChart('saveAsPNG', 'myChart.png', getExportServer());
    });
    $("#pdfButton").click(function () {
        // call the export server to create a PNG image
        $('#chartContainer').jqxChart('saveAsPDF', 'myChart.pdf', getExportServer());
    });
});

// }
