/**
 * Created by alexcomu on 30/03/16.
 */
/* DATA and N are now provided by the controller instead
       of being random values. Look at the index.html template
       to see how they are provided */

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