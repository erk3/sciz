angular
  .module('app')
  .controller('AdminCtrl', ['$http', '$window', 'authService', adminCtrl]);

function adminCtrl($http, $window, authService) {
  var vm = this;
  vm.newHook = null;
  vm.newHookURL = null;
  vm.hooks = [];

  vm.hostname = $window.location.protocol + '//' + $window.location.hostname + '/api/bot/hooks';
  vm.view = 'group';

  vm.addHook = addHook;
  vm.getHooks = getHooks;
  vm.revokeHook = revokeHook;
  vm.updateGroup = updateGroup;

  vm.user = authService.refreshLocalData();

  vm.updateErrorHook = false;
  vm.updateErrorHookMessage = null;
  vm.updateStatusHook = false;
  vm.updateStatusHookMessage = null;
  vm.updateErrorGroup = false;
  vm.updateErrorGroupMessage = null;
  vm.updateStatusGroup = false;
  vm.updateStatusGroupMessage = null;

  vm.getHooks();

  function getHooks() {
    $http({
      method: 'GET',
      url: '/api/admin/hooks',
      params: {
        groupID: vm.user.currentAssoc.group_id
      }
    })
    .then(handleSuccessfulGetHooks);
  }

  function handleSuccessfulGetHooks(response) {
    if (response && response.data) {
      var hooks = angular.fromJson(response.data);
      vm.hooks = hooks;
    }
  }

  function revokeHook(hook) {
    $http({
      method: 'DELETE',
      url: '/api/admin/hooks',
      params: {id: hook.id, groupID: vm.user.currentAssoc.group_id}
    })
    .then(handleSuccessfulDeleteHook)
    .catch(handleFailedDeleteHook);
  }

  function handleFailedDeleteHook(response) {
    vm.updateErrorHook = true;
    vm.updateErrorHookMessage = 'Erreur';
    vm.updateStatusHook = false;
    vm.updateStatusHookMessage = null;
    if (response && response.data) {
      vm.updateErrorHookMessage += ': ' + response.data.message;
    }
  }

  function handleSuccessfulDeleteHook() {
    vm.getHooks();
    vm.updateErrorHook = false;
    vm.updateErrorHookMessage = null;
    vm.updateStatusHook = true;
    vm.updateStatusHookMessage = 'Hook révoqué !';
  }

  function addHook() {
    $http({
      method: 'POST',
      url: '/api/admin/hooks',
      data: {
        name: vm.newHook,
        url: vm.newHookURL,
        groupID: vm.user.currentAssoc.group_id
      }
    })
    .then(handleSuccessfulAddHook)
    .catch(handleFailedAddHook);
  }

  function handleSuccessfulAddHook() {
    vm.getHooks();
    vm.newHook = null;
    vm.newHookURL = null;
    vm.updateErrorHook = false;
    vm.updateErrorHookMessage = null;
    vm.updateStatusHook = true;
    vm.updateStatusHookMessage = 'Hook ajouté !';
  }

  function handleFailedAddHook(response) {
    vm.newHook = null;
    vm.newHookURL = null;
    vm.updateErrorHook = true;
    vm.updateErrorHookMessage = 'Erreur';
    vm.updateStatusHook = false;
    vm.updateStatusHookMessage = null;
    if (response && response.data) {
      vm.updateErrorHookMessage += ': ' + response.data.message;
    }
  }

  function updateGroup() {
    authService.updateGroup(vm.user.currentAssoc.group);
    vm.user.currentAssoc.group.groupID = vm.user.currentAssoc.group.id;
    $http({
      method: 'POST',
      url: '/api/admin/group',
      data: JSON.stringify(vm.user.currentAssoc.group)
    })
    .then(handleSuccessfulAddGroup)
    .catch(handleFailedAddGroup);
  }

  function handleSuccessfulAddGroup() {
    vm.user = authService.updateLocalData();
    vm.updateErrorGroup = false;
    vm.updateErrorGroupMessage = null;
    vm.updateStatusGroup = true;
    vm.updateStatusGroupMessage = 'Modifications enregistrées !';
  }

  function handleFailedAddGroup(response) {
    vm.updateErrorGroup = true;
    vm.updateErrorGroupMessage = 'Erreur';
    vm.updateStatusGroup = false;
    vm.updateStatusGroupMessage = null;
    if (response && response.data) {
      vm.updateErrorGroupMessage += ': ' + response.data.message;
    }
  }
}
