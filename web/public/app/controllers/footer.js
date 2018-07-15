angular
  .module('app')
  .controller('FooterCtrl', ['$scope', '$http', footerCtrl]);

function footerCtrl($scope, $http) {
  var vm = this;
  $scope.stats = {};

  $http({
    method: 'GET',
    url: '/api/public/stats'
  })
  .then(successCallBack, errorCallBack);

  function successCallBack(response) {
    if (response.data) {
      $scope.stats = angular.fromJson(response.data);
    }
  }

  function errorCallBack() {}
}
