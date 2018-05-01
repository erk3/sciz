angular
  .module('app')
  .controller('HeaderCtrl', ['$scope', '$uibModal', headerCtrl]);

function headerCtrl($scope, $uibModal) {
  var vm = this;

  vm.updateUserData = function (newVal) {
    $scope.user = newVal.user;
  };

  $scope.$watch('authService.dataWrap', vm.updateUserData, true);

  $scope.openCreateGroupModal = function () {
    var modalInstance = $uibModal.open({
      templateUrl: 'app/views/createGroupModal.html',
      controller: 'CreateGroupCtrl',
      resolve: {}
    });

    modalInstance.result.then(function () {
      return;
    }, function () {
      return;
    });
  };
}
