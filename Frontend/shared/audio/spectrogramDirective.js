angular.module('audio').directive('spectrogramDirective', function () {
    
    function link(scope, element, attrs) {
    	//see https://github.com/vlandham/spectrogramJS
    	var container = element[0];
		var d3Container = d3.select(container);
        
        var canvas  = d3Container.append("canvas")
            // .style("position", "absolute");

        var svg = d3Container.append("svg")
            .style("position", "absolute");
        
        var xAxis = svg.append("g")
            .attr("class", "x axis")
            .style("fill", "none");
            
        var yAxis = svg.append("g")
            .attr("class", "y axis")
            .style("fill", "none");

        var maxValue = 0;
        var minValue = 0;
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
                canvasHeight = 400;

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

            //todo: takes the last column in the data, wich is not enough robust if we don't update with only the las column changing
            maxValue = 0.5//Math.max.apply(null, Array.prototype.slice.call(data[data.length - 1]).concat(maxValue));
            minValue = 0//Math.min.apply(null, Array.prototype.slice.call(data[data.length - 1]).concat(minValue));
            var rangeValue = maxValue - minValue;
            var color = d3.scale.linear()
                .domain([minValue, minValue + 0.05/5 * rangeValue, minValue + 0.25/5 * rangeValue, minValue + 1/5 * rangeValue, minValue + 3/5 * rangeValue, maxValue])
                .range(["black", "purple", "blue", "green", "yellow", "red"]);

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
                for (var imageX = 0; imageX < imageWidth; imageX++) {
                    for (var imageY = 0; imageY < imageHeight; imageY++) {
                        
                        var intensity = -1;
                        
                        var x = Math.floor((imageX * depth) / imageWidth);
                        var y = Math.floor((imageY * data[0].length) / imageHeight);
                        if(x in data && y in data[x])
                            intensity = data[x][y];
                        
                        intensity = 0
                        
                        if(imageX % 6 == 0)
                            intensity+=0.25;
                        if(imageY % 12 == 0)
                            intensity+= 0.25;
                            
                        var c = d3.rgb(color(intensity));
                        
                    
                            
                        var p = (imageY * imageWidth + imageX) * 4;
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
        var depth =  50;


    	scope.$watchCollection("slice", function(value, oldValue){

            if(!value) return;
            

            //copy the array
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

