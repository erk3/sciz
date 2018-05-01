angular
  .module('app')
  .controller('CreateGroupCtrl', ['$scope', '$http', '$uibModalInstance', 'authService', createGroupCtrl]);

function createGroupCtrl($scope, $http, $uibModalInstance, authService) {
  $scope.groupName = '';
  $scope.working = false;

  $scope.createGroup = function (groupName) {
    if (groupName !== '') {
      $scope.working = true;
      $http({
        method: 'POST',
        url: '/api/creategroup',
        data: {groupName: groupName},
        timeout: 120000 // 2 minute
      })
      .then(handleSuccessfulCreateGroup)
      .catch(handleFailedCreateGroup);
    }
  };

  $scope.closeCreateGroupModal = function () {
    $uibModalInstance.dismiss('cancel');
  };

  function handleSuccessfulCreateGroup() {
    $scope.resetAlerts();
    authService.refreshGroups();
    $uibModalInstance.close();
  }

  function handleFailedCreateGroup(response) {
    $scope.resetAlerts();
    $scope.createGroupError = true;
    $scope.createGroupErrorMessage = 'Erreur';
    if (response && response.data) {
      $scope.createGroupErrorMessage += ': ' + response.data.message;
    }
  }

  $scope.resetAlerts = function () {
    $scope.working = false;
    $scope.createGroupError = false;
    $scope.createGroupErrorMessage = null;
  };
}
