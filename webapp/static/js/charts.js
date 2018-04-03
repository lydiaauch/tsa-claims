var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 550 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

var x = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
var y = d3.scaleLinear()
          .range([height, 0]);

var svg = d3.select("#barchart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

var svg2 = d3.select("#airline_barchart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom + 50)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

var tooltip = d3.select("body").append("div").attr("class", "toolTip");

// Airport Visualization
d3.json("/data", function(error, dataset) {
  if (error) throw error;

  data = dataset.vis_data.airport_data;

  data.forEach(function(d) {
    d.claims_count = +d.claims_count;
  });

  x.domain(data.map(function(d) { return d.airport_code; }));
  y.domain([0, d3.max(data, function(d) { return d.claims_count; })]);

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.airport_code); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.claims_count); })
      .attr("height", function(d) { return height - y(d.claims_count); })
      .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.airport_code) + "<br>" + "Claims:" + (d.claims_count));
            })
    		.on("mouseout", function(d){ tooltip.style("display", "none");});

  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  svg.append("g")
      .call(d3.axisLeft(y));

});

// Airline Visualization
d3.json("/data", function(error, dataset) {
  if (error) throw error;

  data = dataset.vis_data.airline_data.bad_airlines;

  console.log(data);

  data.forEach(function(d) {
    d.claims_count = +d.claims_count;
  });

  x.domain(data.map(function(d) { return d.airline_name; }));
  y.domain([0, d3.max(data, function(d) { return d.claims_count; })]);

  svg2.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.airline_name); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.claims_count); })
      .attr("height", function(d) { return height - y(d.claims_count); })
      .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.airline_name) + "<br>" + "Claims:" + (d.claims_count));
            })
    		.on("mouseout", function(d){ tooltip.style("display", "none");});

  svg2.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(30)")
      .style("text-anchor", "start");

  svg2.append("g")
      .call(d3.axisLeft(y));

});
