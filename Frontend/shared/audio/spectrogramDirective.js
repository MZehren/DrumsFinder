angular.module('audio').directive('spectrogramDirective', function () {
    
    function link(scope, element, attrs) {
    	//see https://github.com/vlandham/spectrogramJS
    	var container = element[0];
		var d3Container = d3.select(container);
        
        var canvas  = d3Container.append("canvas")
            .style("position", "absolute");

        var svg = d3Container.append("svg")
            .style("position", "absolute");
        
        var xAxis = svg.append("g")
            .attr("class", "x axis")
            .style("fill", "none");
            
        var yAxis = svg.append("g")
            .attr("class", "y axis")
            .style("fill", "none");

        function reduceDimensions(array, dimensions){
            if(array.length <= dimensions) return array;
            
            var step =  parseInt(array.length/dimensions);
            
            var result = []
            for(var i = 0; i < dimensions; i ++)
                result.push(array[i*step]);
            
            
            return result;
        }

  

    	function update(data){
            var width = 960,
                height = 500;

            var dx = depth,
                dy = data[0].length;
           
           // Fix the aspect ratio.
            // var ka = dy / dx, kb = height / width;
            // if (ka < kb) height = width * ka;
            // else width = height / ka;

            var x = d3.scale.linear()
                .domain([0, dx])
                .range([0, width]);

            var y = d3.scale.linear()
                .domain([0, dy])
                .range([height, 0]);

            var color = d3.scale.linear()
                .domain([-0.1, 0.1])
                .range(["#0a0", "#fff"]);

            var xAxisScale = d3.svg.axis()
                .scale(x)
                .orient("top")
                .ticks(20);

            var yAxisScale = d3.svg.axis()
                .scale(y)
                .orient("right");

            canvas.attr("width", dx)
                .attr("height", dy)
                .style("width", width + "px")
                .style("height", height + "px")
                .call(function(cavas){ drawImage(canvas, data, dx, dy, color); });

            svg.attr("width", width)
            .attr("height", height);
            
            xAxis.attr("transform", "translate(0," + height + ")")
            .call(xAxisScale);
            
            yAxis.call(yAxisScale);
            

            
            // Compute the pixel colors; scaled by CSS.
            function drawImage(canvas) {
                var context = canvas.node().getContext("2d"),
                    image = context.createImageData(width, height);
                

                for (var x = 0; x < width; ++x) {
                    if(!data[x]) break;
                    
                    var reducedArray = reduceDimensions(data[x], height);
                    for (var y = 0; y < height; ++y) {
                        var c = d3.rgb(color(reducedArray[y]));
                        var p = (x * width + y) * 4;
                        
                        image.data[p++] = c.r;
                        image.data[p++] = c.g;
                        image.data[p++] = c.b;
                        image.data[p++] = 255;
                    

                    }
                }
                context.putImageData(image, 0, 0);
            }
    	}

        var allData = [];
        var depth =  scope.depth ? scope.depth : 900;
    	scope.$watchCollection("slice", function(value, oldValue){
            if(!value) return;
            

            
            allData.push(value.slice(0));
            if(allData.length > depth)
                allData = allData.slice(1);
                
            update(allData)
        });
    	    
    }
    return {
        restrict: 'E',
        scope : {
        	slice : '=',
            depth : "=?",
            maxFrequency : "=?",
            minFrequency : "=?"
        },
        link: link
    };
});

