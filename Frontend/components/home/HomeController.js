angular.module('home')
    .controller("HomeController", function ($scope, userMediaProvider) {

	userMediaProvider.toggleLiveInput();
  
   

})
