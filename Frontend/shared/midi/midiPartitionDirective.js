angular.module('midi').directive('midiPartitionDirective', function () {
    
    function link(scope, element, attrs) {
    	//see http://bl.ocks.org/mbostock/6232620
    	var container = element[0];
		var svg = d3.select(container)
            .append("svg")



    	function update(value, oldValue){
            if(value == oldValue) return;

            var events = scope.midiFile.getMidiEvents().slice(0,100);
            console.log(events);

            var width = element.parent().width();
            var height = width/2;//element.parent().height() || element.parent().width();;
            var maxWidth = d3.max(events, function(d){return d.playTime;});
            var maxHeight = d3.max(events, function(d){return d.param1;});

            var x = d3.scale.linear()
                .domain([0, maxWidth])
                .range([0, width]);

            var y = d3.scale.linear()
                .domain([0, maxHeight])
                .range([0, height]);

            svg.attr("width", width)
                .attr("height", height);

            svg.selectAll(".bar")
                .data(events)
                .enter().append("g")
                    .attr("class", "bar")
                    .attr("transform", function(d) { 
                        return "translate(" + x(d.playTime) + "," + y(d.param1) + ")"; 
                    })
                    .on("click", function(d){ console.log(d)})
                .append("rect")
                    .attr("width", function(d){ return 10 })
                    .attr("height", function(d){ return 10});



    	}

    	scope.$watch("midiFile", update);
    	    
    }
    return {
        restrict: 'E',
        scope : {
        	midiFile : '='
        },
        link: link
    };
});

