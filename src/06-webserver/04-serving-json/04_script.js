/**
 * Created by alexcomu on 30/03/16.
 */

/*
    At begin we just fill data with 0, so that we
  start with a flat line that gets updated as soon
  as we load the page
*/
var n = 40,
    data = [];
for (var i=n; i--;) data.push(0);

var width = 960,
    height = 500;

var x = d3.scale.linear().domain([0, n - 1]).range([0, width]);
var y = d3.scale.linear().domain([0, 100]).range([height, 0]);

var line = d3.svg.line()
    .x(function(d, i) { return x(i); })
    .y(function(d, i) { return y(d); });

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g");

var path = svg.append("g")
  .append("path")
    .data([data])
    .attr("class", "line")
    .attr("d", line);

//We call the tick function to start the update process
tick();

function tick() {
  /*The tick function is the one actually in charge of
    retrieving data from our controller and updating the graph.
    This is done by using d3.json to call the /data controller
  */
  d3.json("/data", function(json, error) {
      //Append to our array of graph data the new usage value
      data.push(json.usage);

      //Shift our whole graph left by 1 unit so that we can
      //show at the right end the newly added value
      path
          .attr("d", line)
          .attr("transform", "")
        .transition()
          .duration(500)
          .ease("linear")
          .attr("transform", "translate(" + x(-1) + ")")
          .each("end", tick); //The tick function gets called again after the transition

      //Just throw away the oldest value we don't need anymore
      data.shift();
  });
}