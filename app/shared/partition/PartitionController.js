angular.module('partition')
    .controller("PartitionController", function ($scope, $http, $interval, $timeout, audio) {

    function Note(length, type){
    	this.Length = length || 4;
    	this.Doted = false;
    	this.Triple = false;
    	this.Type = type || ["Kick"]

    	this.Play = function(){
            for(var i in this.Type)
    		  audio.play(this.Type[i]);
    	}

    	this.Increase = function(){
    		if(this.length < 32)
    			this.length *= 2;
    	}

    	this.Decrease = function(){
    		if(this.length > 1)
    			this.length /= 2;
    	}
    }

    function TimeSignature(beatNumber, beatUnit){
    	this.BeatNumber = beatNumber || 4;
    	this.BeatUnit = beatUnit || new Note();

    	this.GetBeatFraction = function (note){
    		var fraction = this.BeatUnit.Length / note.Length;
    		if(note.Doted)
    			fraction *= 1.5;
    		if(note.Triple)
    			fraction *= 2/3;

    		return fraction
    	}
    }

    function Bar(timeSignature, tempo){
    	this.TimeSignature = timeSignature || new TimeSignature();
    	this.Tempo = tempo | 90;
    	this.Notes = [
            new Note(8, ["OpenHiHat", "Kick"]),
            new Note(8, ["OpenHiHat"]),
            new Note(8, ["OpenHiHat", "Snare"]),
            new Note(8, ["OpenHiHat"]),
            new Note(8, ["OpenHiHat", "Kick"]),
            new Note(8, ["OpenHiHat"]),
            new Note(8, ["OpenHiHat", "Snare"]),
            new Note(8, ["OpenHiHat"])
        ];
        
 

    	this.GetNoteDelay = function(note){
    		var beatFraction = this.TimeSignature.GetBeatFraction(note);
    		var bpm = this.Tempo / beatFraction;
    		return 60000 / bpm;
    	}
    }

    function Partition(){
    	this.Bars = [new Bar()];
    	this.BarCursor = null;
    	this.NoteCursor = null;
    	this.Play = false;
    	this.Promise = null;
        this.Loop = false;

    	var that = this;

        this.Stop = function(){
            that.Play = false
            that.BarCursor = null;
            that.NoteCursor = null;
        }

    	this.GetNote = function(){
    		try{
	    		return that.Bars[that.BarCursor].Notes[that.NoteCursor];
	    	}
	    	catch(e){
	    		return null;
	    	}
    	}

        this.isEmpty = function(){
            if(that.Bars.length > 0 && that.Bars[0].Notes.length > 0)
                return false;
            return true;
        }

    	//Go to the next (or first if not initialized) note.
    	//Set the cursor to null if the note doesn't exit.
    	this.IncrementCursor = function(){
    		if(that.BarCursor === null){
    			that.BarCursor = 0;
    			that.NoteCursor = 0;
    		}
    		else if(that.NoteCursor < that.Bars[that.BarCursor].Notes.length){
    			that.NoteCursor ++;
    		}
    		else if(that.BarCursor < that.Bars.length){
    			that.BarCursor ++;
    			that.NoteCursor = 0;
    		}
    		
    		if(!that.GetNote()){

                that.BarCursor = null;
                that.NoteCursor = null;

                if(that.Loop){ //TODO: not safe if there is no notes.
                    that.IncrementCursor();              
                }
                else{
                    that.Play = false;
                }

    		}
    	}


    	// TODO: IDK if it's the good place to do this
    	$scope.$watch("partition.Play", function(play){
    		if(!play && $scope.partition.Promise){
    			$timeout.cancel($scope.partition.Promise);
    		}
    		if(play){
    			$scope.partition.PlayNote();
    		}
    	})


    	this.PlayNote = function(){
            
            if(that.Play && !that.isEmpty()){
                if(that.BarCursor === null)
                    that.IncrementCursor();

                var note = that.GetNote();
                if(note){
                    note.Play();
                    var delay = that.Bars[that.BarCursor].GetNoteDelay(note);
                    that.IncrementCursor();
                    that.Promise = $timeout(that.PlayNote, delay)
                }
            }
    	}
    }


    $scope.partition = new Partition();


});