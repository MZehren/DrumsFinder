angular.module('midi').directive('midiPartitionDirective', function() {

    function link(scope, element, attrs) {
        //see http://www.vexflow.com/docs/tutorial.html
        //and see musicXML
        var container = element[0];
        // var canvas = d3.select(container)
        //           .append("canvas")
        //           .attr("width", 700)
        //           .attr("height", 100)

        var canvas = $("canvas")[0];
        var renderer = new Vex.Flow.Renderer(canvas, Vex.Flow.Renderer.Backends.CANVAS);

        var ctx = renderer.getContext();
        var stave = new Vex.Flow.Stave(10, 0, 500);
        stave.addClef("treble").setContext(ctx).draw();

        function update(value, oldValue) {
            if (value == oldValue) return;

            for (var barIdx in value) {
                var bar = value[barIdx];
               

                var notes = []
                for(var noteIdx in bar){
                  var note = bar[noteIdx]
                  notes.push( new Vex.Flow.StaveNote(note))
                }

            

                // Create a voice in 4/4
                var voice = new Vex.Flow.Voice({
                    num_beats: 4,
                    beat_value: 4,
                    resolution: Vex.Flow.RESOLUTION
                });

                // Add notes to voice
                voice.addTickables(notes);

                // Format and justify the notes to 500 pixels
                var formatter = new Vex.Flow.Formatter().
                joinVoices([voice]).format([voice], 500);

                // Render voice
                voice.draw(ctx, stave);

            }



        }

        scope.$watch("notes", update);

    }
    return {
        restrict: 'E',
        scope: {
            notes: '=',
            playNote: "="
        },
        template: '<canvas width=700 height=100></canvas>',
        link: link
    };
});