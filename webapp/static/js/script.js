function createChart(each_season) {
		var barData = {
                   labels : [{% for season in each_season %}
                                  "{{season.season}}",
                              {% endfor %}],
                   datasets : [
                      {
                            fillColor: "rgba(151,187,205,0.2)",
                            strokeColor: "rgba(151,187,205,1)",
                            pointColor: "rgba(151,187,205,1)",
                         data : [{% for season in  each_season %}
                                      {{season.data.pts}},
                                    {% endfor %}]
                      }
                      ]
                   }
                   // get bar chart canvas
                   var mychart = document.getElementById("chart").getContext("2d");
                   steps = 10;
                   max = Math.ceil({{each_season[3].data.pts}} + 10);
                   min = Math.ceil({{each_season[0].data.pts}} - 10);
                   // draw bar chart
                   new Chart(mychart).Line(barData, {
                        scaleOverride: false,
                        scaleSteps: steps,
                        scaleStepWidth: Math.ceil((max - min ) / steps),
                        scaleStartValue: min,
                        scaleShowVerticalLines: false,
                        scaleShowGridLines : false,
                        barShowStroke : false,
                        scaleShowLabels: true
                   });
}