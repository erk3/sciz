angular
  .module('app')
  .controller('HeaderCtrl', ['$scope', headerCtrl]);

function headerCtrl($scope) {
  var vm = this;

  vm.updateUserData = function (newVal) {
    $scope.user = newVal.user;
  };

  $scope.$watch('authService.dataWrap', vm.updateUserData, true);
}
