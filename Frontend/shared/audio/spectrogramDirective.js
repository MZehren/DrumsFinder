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

        // function reduceDimensions(array, dimensions){
        //     if(array.length <= dimensions) return array;
            
        //     var step =  parseInt(array.length/dimensions);
            
        //     var result = []
        //     for(var i = 0; i < dimensions; i ++)
        //         result.push(array[i*step]);
            
            
        //     return result;
        // }

  

    	function update(data){
            var canvasWidth = 960,
                canvasHeight = 200;

            var imageWidth = depth,
                imageHeight = 100;
           
           // Fix the aspect ratio.
            // var ka = dy / dx, kb = height / width;
            // if (ka < kb) height = width * ka;
            // else width = height / ka;

            var scaleImageToCanvasWidth = d3.scale.linear() //from image width domain to canvas width
                .domain([0, imageWidth])
                .range([0, canvasWidth]);

            var scaleImageToCanvasHeight = d3.scale.linear()
                .domain([0, imageHeight])
                .range([canvasHeight, 0]);

            var color = d3.scale.linear()
                .domain([-0.1 , -0.05 , 0 , 0.05 ,0.1])
                .range(["#0a0", "#6c0", "#ee0", "#eb4", "#eb9", "#fff"]);

            var xAxis = d3.svg.axis()
                .scale(scaleImageToCanvasWidth)
                .orient("top")
                .ticks(20);

            var yAxis = d3.svg.axis()
                .scale(scaleImageToCanvasHeight)
                .orient("right");

            canvas.attr("width", imageWidth)
                .attr("height", imageHeight)
                .style("width", canvasWidth + "px")
                .style("height", canvasHeight + "px")
                .call(function(cavas){ drawImage(canvas); });

            svg.attr("width", canvasWidth)
            .attr("height", canvasHeight);
            
            // xAxis.attr("transform", "translate(0," + imageWidth + ")")
            //     .call(xAxis);
            
            // yAxis.call(yAxis);
            

            
            // Compute the pixel colors; scaled by CSS.
            function drawImage(canvas) {
                var context = canvas.node().getContext("2d"),
                    image = context.createImageData(imageWidth, imageHeight);
                
                //TODO: https://github.com/fullergalway/anispectrogram/blob/master/index.html create only the new pixels in the image !
                for (var x = 0; x < imageWidth; ++x) {
                    for (var y = 0; y < imageHeight; ++y) {
                        var imageX = scaleImageToCanvasWidth(x);
                        var imageY = scaleImageToCanvasHeight(y);

                        var intensity = -1;
                        if(x in data && y in data[x])
                            intensity = data[x][y];
                        var c = d3.rgb(color(intensity));

                        var p = (y * imageWidth + x) * 4;
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
        var depth =  96;


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

