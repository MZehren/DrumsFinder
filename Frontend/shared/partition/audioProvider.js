angular.module('partition')
    .factory('audio', [function featuresFactory() {

  //   	var channel_max = 1;										// number of channels
		// audiochannels = new Array();
		// for (a=0;a<channel_max;a++) {									// prepare the channels
		// 	audiochannels[a] = new Array();
		// 	audiochannels[a]['channel'] = new Audio();						// create a new audio object
		// 	audiochannels[a]['finished'] = -1;		
		// 	audiochannels[a]['channel'].src = document.getElementById("kick").src;					// expected end time for this channel
		// 	audiochannels[a]['channel'].play();
		// }

		// this.play = function(s) {
		// 	for (a=0;a<audiochannels.length;a++) {
		// 		//thistime = new Date();
		// 		if (true) {			// is this channel finished? audiochannels[a]['finished'] < thistime.getTime()
		// 			//audiochannels[a]['finished'] = thistime.getTime() + document.getElementById(s).duration*1000;
		// 			//audiochannels[a]['channel'].src = document.getElementById(s).src;
		// 			//audiochannels[a]['channel'].load();
		// 			audiochannels[a]['channel'].currentTime = 0;
					
		// 			break;
		// 		}
		// 	}
		// }

		this.Enum = ["Kick", "Snare", "OpenHiHat"];
		audioChannels = {};
		
		for(var i in this.Enum){
			var sound = this.Enum[i];
			audioChannels[sound] = new Audio("Data/Samples/" + sound + ".wav");
		}

		this.play = function(s){
			audioChannels[s].currentTime = 0;
			audioChannels[s].play();
		}

		return this;

    }]);