angular.module('partition').directive('partitionDirective', function () {
    
    function link(scope, element, attrs) {
    	//see http://bl.ocks.org/mbostock/6232620
    	var container = element[0];
		var svg = d3.select(container)
            .append("svg")



       

        var staff = null

     //    var bars = d3.time.scale()
	    // .domain([new Date(2013, 2, 1), new Date(2013, 2, 15) - 1])
	    // .range([0, width]);


    	function update(){
            var containerWith = element.parent().width();
            var containerHeight = element.parent().height();
            var margin = 10;
            svg.attr("width", containerWith)
                .attr("height", containerHeight);

        	var staff = svg.append("g")
        		.call(d3.svg.axis()
	        			.scale(d3.scale.linear().domain([0,4]).range([containerHeight - margin, margin]))
	        			.ticks(5)
	        			.tickFormat(function(d){return;})
	        			.orient("right")
                        .tickSize(containerWith)
        			);

        	staff.selectAll("path")
        		.attr("display", "none");
        	staff.selectAll("line")
        		.attr("stroke", "black");

    	}

    	update();
    	    
    }
    return {
        restrict: 'E',
        scope : {
        	'partition' : '='
        },
        link: link
    };
});

