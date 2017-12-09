angular
  .module('app')
  .controller('AdminCtrl', ['$http', '$window', 'authService', adminCtrl]);

function adminCtrl($http, $window, authService) {
  var vm = this;

  /*
   * Init
   */
  vm.newHook = null;
  vm.newHookURL = null;
  vm.hooks = [];
  vm.confs = {};

  vm.hostname = $window.location.protocol + '//' + $window.location.hostname + '/api/bot/hooks';

  vm.addHook = addHook;
  vm.getHooks = getHooks;
  vm.revokeHook = revokeHook;
  vm.getConfs = getConfs;
  vm.updateConfs = updateConfs;
  vm.updateGroup = updateGroup;
  vm.switchView = switchView;
  vm.isUnboxConfValueValid = isUnboxConfValueValid;

  vm.updateErrorConf = false;
  vm.updateErrorConfConfMessage = null;
  vm.updateStatusConf = false;
  vm.updateStatusConfMessage = null;
  vm.updateErrorHook = false;
  vm.updateErrorHookMessage = null;
  vm.updateStatusHook = false;
  vm.updateStatusHookMessage = null;
  vm.updateErrorGroup = false;
  vm.updateErrorGroupMessage = null;
  vm.updateStatusGroup = false;
  vm.updateStatusGroupMessage = null;

  vm.user = authService.refreshLocalData();
  vm.switchView('group');
  vm.confSection = 'battle_format';

  /*
   * View Switcher
   */
  function switchView(view) {
    if (view === 'hooks') {
      vm.getHooks();
    } else if (view === 'confs') {
      vm.getConfs();
    }
    vm.view = view;
  }

  /*
   * Confs
   */
  function isUnboxConfValueValid(conf) {
    if (conf.key.startsWith('s_')) {
      return !(conf.value === '' || conf.value === undefined || conf.value === null) &&
        !conf.value.match(/{[^}]*({|$)/ig) &&
        !conf.value.match(/((^)|})[^{]*}/ig) &&
        !conf.value.match(/{[^{}]*\W[^{}]*}/ig);
    }
    return !(conf.value === '' || conf.value === undefined || conf.value === null) &&
      !conf.value.match(/{[^}]*({|$)/ig) &&
      !conf.value.match(/((^)|})[^{]*}/ig);
  }

  function unboxConf(conf) {
    var newVal = conf.value.replace(/{o\.s_([^}]+)}/g, function (str, group) {
      return '{' + group + '}';
    });
    if (newVal === conf.value) {
      newVal = conf.value.replace(/{o\.([^}]+)}/g, function (str, group) {
        return '{' + group + '}';
      });
      if (newVal === conf.value) {
        conf.prefix = '';
      } else {
        conf.prefix = 'o.';
      }
    } else {
      conf.prefix = 'o.s_';
    }
    conf.value = newVal;
    return conf;
  }

  function boxConfValue(conf) {
    var res = conf.value;
    if (conf.key.startsWith('s_')) {
      res = conf.value.replace(/{([^}]+)}/g, function (str, group) {
        return '{' + conf.prefix + group + '}';
      });
    }
    return res;
  }

  function getConfs() {
    $http({
      method: 'GET',
      url: '/api/admin/confs',
      params: {
        groupID: vm.user.currentAssoc.group_id
      }
    })
    .then(handleSuccessfulGetConfs);
  }

  function handleSuccessfulGetConfs(response) {
    if (response && response.data) {
      vm.origConfs = angular.fromJson(response.data);
      vm.confs = JSON.parse(JSON.stringify(vm.origConfs)).map(unboxConf);
    }
  }

  function updateConfs() {
    // Build modified conf
    var modifiedConfs = [];
    for (var i = 0; i < vm.confs.length; i++) {
      var val = boxConfValue(vm.confs[i]);
      if (val !== vm.origConfs[i].value) {
        vm.origConfs[i].value = val;
        modifiedConfs.push(vm.origConfs[i]);
      }
    }
    $http({
      method: 'POST',
      url: '/api/admin/confs',
      data: {
        confs: JSON.stringify(modifiedConfs),
        groupID: vm.user.currentAssoc.group_id
      }
    })
    .then(handleSuccessfulUpdateConfs)
    .catch(handleFailedUpdateConfs);
  }

  function handleSuccessfulUpdateConfs() {
    vm.updateErrorConf = false;
    vm.updateErrorConfMessage = null;
    vm.updateStatusConf = true;
    vm.updateStatusConfMessage = 'Modifications enregistrées !';
  }

  function handleFailedUpdateConfs(response) {
    vm.updateErrorConf = true;
    vm.updateErrorConfMessage = 'Erreur';
    vm.updateStatusConf = false;
    vm.updateStatusConfMessage = null;
    if (response && response.data) {
      vm.updateErrorConfMessage += ': ' + response.data.message;
    }
  }

  /*
   * Hooks
   */
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

  /*
   * Group
   */
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
