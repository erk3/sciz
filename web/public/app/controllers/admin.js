angular
  .module('app')
  .controller('AdminCtrl', ['$http', 'authService', adminCtrl]);

function adminCtrl($http, authService) {
  var vm = this;
  vm.newHook = null;
  vm.hooks = [];

  vm.addHook = addHook;
  vm.getHooks = getHooks;
  vm.revokeHook = revokeHook;

  vm.user = authService.refreshLocalData();

  vm.updateError = false;
  vm.updateErrorMessage = null;
  vm.updateStatus = false;
  vm.updateStatusMessage = null;

  vm.getHooks();

  function getHooks() {
    $http({
      method: 'GET',
      url: '/api/admin/hooks',
      params: {
        groupID: vm.user.currentGroupID
      }
    })
    .then(handleSuccessfulGet);
  }

  function handleSuccessfulGet(response) {
    if (response && response.data) {
      var hooks = angular.fromJson(response.data);
      vm.hooks = hooks;
    }
  }

  function revokeHook(hook) {
    $http({
      method: 'DELETE',
      url: '/api/admin/hooks',
      params: {id: hook.id, groupID: vm.user.currentGroupID}
    })
    .then(handleSuccessfulDelete)
    .catch(handleFailedDelete);
  }

  function handleFailedDelete(response) {
    vm.updateError = true;
    vm.updateErrorMessage = 'Erreur';
    vm.updateStatus = false;
    vm.updateStatusMessage = null;
    if (response && response.data) {
      vm.updateErrorMessage += ': ' + response.data.message;
    }
  }

  function handleSuccessfulDelete() {
    vm.getHooks();
    vm.updateError = false;
    vm.updateErrorMessage = null;
    vm.updateStatus = true;
    vm.updateStatusMessage = 'Hook révoqué';
  }

  function addHook() {
    $http({
      method: 'POST',
      url: '/api/admin/hooks',
      data: {
        name: vm.newHook,
        groupID: vm.user.currentGroupID
      }
    })
    .then(handleSuccessfulAdd)
    .catch(handleFailedAdd);
  }

  function handleSuccessfulAdd() {
    vm.getHooks();
    vm.newHook = null;
    vm.updateError = false;
    vm.updateErrorMessage = null;
    vm.updateStatus = true;
    vm.updateStatusMessage = 'Hook ajouté';
  }

  function handleFailedAdd(response) {
    vm.newHook = null;
    vm.updateError = true;
    vm.updateErrorMessage = 'Erreur';
    vm.updateStatus = false;
    vm.updateStatusMessage = null;
    if (response && response.data) {
      vm.updateErrorMessage += ': ' + response.data.message;
    }
  }
}
