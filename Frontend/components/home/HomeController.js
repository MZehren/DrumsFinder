angular.module('home')
    .controller("HomeController", function ($scope, userMediaProvider) {
 
    userMediaProvider.toggleLiveInput();
    $scope.fftBuffer = userMediaProvider.fftBuffer;
    $scope.$watchCollection("fftBuffer", function(value){
  
    })

})
