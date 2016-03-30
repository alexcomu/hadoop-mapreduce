/**
 * Created by alexcomu on 30/03/16.
 */
var load_data = function(minimum) {
    d3.json("/data/"+minimum, function(json, error) {
        d3.select('#chart').selectAll('div').remove();
        d3.select('#chart')
            .selectAll('div')
                .data(json.data)
            .enter().append('div')
                .style("width", function(d) { return d[1] * 150 + "px" })
                .text(function(d) { return d[0] + ' ('+d[1]+')'; });
    });
};