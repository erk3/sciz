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
  vm.firstLoad = true;
  vm.assocs = [];
  vm.hooks = [];
  vm.confs = {};
  vm.usersList = [];

  vm.hostname = $window.location.protocol + '//' + $window.location.hostname + '/api/bot/hooks';

  vm.addHook = addHook;
  vm.getAssocs = getAssocs;
  vm.exclude = exclude;
  vm.roleUpdate = roleUpdate;
  vm.getHooks = getHooks;
  vm.revokeHook = revokeHook;
  vm.getConfs = getConfs;
  vm.updateConfs = updateConfs;
  vm.updateGroup = updateGroup;
  vm.deleteGroup = deleteGroup;
  vm.switchView = switchView;
  vm.isUnboxConfValueValid = isUnboxConfValueValid;
  vm.templateConf = templateConf;
  vm.queryUserSearch = queryUserSearch;
  vm.inviteUser = inviteUser;

  vm.resetAlerts = function () {
    vm.inviteError = false;
    vm.inviteErrorMessage = null;
    vm.inviteStatus = false;
    vm.inviteStatusMessage = null;
    vm.assocsError = false;
    vm.assocsErrorMessage = null;
    vm.assocsStatus = false;
    vm.assocsStatusMessage = null;
    vm.updateErrorConf = false;
    vm.updateErrorConfMessage = null;
    vm.updateStatusConf = false;
    vm.updateStatusConfMessage = null;
    vm.updateErrorHook = false;
    vm.updateErrorHookMessage = null;
    vm.updateStatusHook = false;
    vm.updateStatusHookMessage = null;
    vm.updateErrorGroup = false;
    vm.updateErrorGroupMessage = null;
    vm.deleteErrorGroup = false;
    vm.deleteErrorGroupMessage = null;
    vm.updateStatusGroup = false;
    vm.updateStatusGroupMessage = null;
  };

  vm.deleteConfirmation = false;

  vm.resetAlerts();
  getUsersList();

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
    } else if (view === 'assocs') {
      vm.getAssocs();
    }
    vm.view = view;
  }

  /*
   * Confs
   */
  function templateConf(template) {
    if (template === null || template === undefined) {
      return;
    }
    $http({
      method: 'GET',
      url: '/api/templates',
      params: {
        templateName: template
      },
      dataType: 'json',
      contentType: 'application/json'
    })
      .then(handleSuccessfulGetConfs);
  }

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
      var confs = angular.fromJson(response.data);
      var updateConfs = [];
      if (vm.firstLoad) {
        vm.origConfs = confs;
        vm.firstLoad = false;
        updateConfs = confs;
      } else {
        // FIXME : awful perfs...
        for (var j = 0; j < vm.origConfs.length; j++) {
          var conf = {
            section: vm.origConfs[j].section,
            key: vm.origConfs[j].key,
            value: vm.origConfs[j].value
          };
          updateConfs.push(conf);
          for (var i = 0; i < confs.length; i++) {
            if (confs[i].section === vm.origConfs[j].section && confs[i].key === vm.origConfs[j].key) {
              updateConfs[j].value = confs[i].value;
            }
          }
        }
      }
      vm.confs = JSON.parse(JSON.stringify(updateConfs)).map(unboxConf);
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
    vm.resetAlerts();
    vm.updateStatusConf = true;
    vm.updateStatusConfMessage = 'Modifications enregistrées !';
  }

  function handleFailedUpdateConfs(response) {
    vm.resetAlerts();
    vm.updateErrorConf = true;
    vm.updateErrorConfMessage = 'Erreur';
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
    vm.resetAlerts();
    vm.updateErrorHook = true;
    vm.updateErrorHookMessage = 'Erreur';
    if (response && response.data) {
      vm.updateErrorHookMessage += ': ' + response.data.message;
    }
  }

  function handleSuccessfulDeleteHook() {
    vm.getHooks();
    vm.resetAlerts();
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
    vm.resetAlerts();
    vm.updateStatusHook = true;
    vm.updateStatusHookMessage = 'Hook ajouté !';
  }

  function handleFailedAddHook(response) {
    vm.newHook = null;
    vm.newHookURL = null;
    vm.resetAlerts();
    vm.updateErrorHook = true;
    vm.updateErrorHookMessage = 'Erreur';
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
    vm.resetAlerts();
    vm.updateStatusGroup = true;
    vm.updateStatusGroupMessage = 'Modifications enregistrées !';
  }

  function handleFailedAddGroup(response) {
    vm.resetAlerts();
    vm.updateErrorGroup = true;
    vm.updateErrorGroupMessage = 'Erreur';
    if (response && response.data) {
      vm.updateErrorGroupMessage += ': ' + response.data.message;
    }
  }

  function deleteGroup() {
    $http({
      method: 'DELETE',
      url: '/api/admin/group',
      params: {groupID: vm.user.currentAssoc.group_id}
    })
    .then(handleSuccessfulDeleteGroup)
    .catch(handleFailedDeleteGroup);
  }

  function handleSuccessfulDeleteGroup() {
    authService.logout();
  }

  function handleFailedDeleteGroup(response) {
    vm.resetAlerts();
    vm.deleteErrorGroup = true;
    vm.deleteErrorGroupMessage = 'Erreur';
    if (response && response.data) {
      vm.deleteErrorGroupMessage += ': ' + response.data.message;
    }
  }

  /*
   * Users
   */
  function getAssocs() {
    $http({
      method: 'GET',
      url: '/api/admin/assocs',
      params: {groupID: vm.user.currentAssoc.group_id}
    })
    .then(handleSuccessfulGetAssocs);
  }

  function handleSuccessfulGetAssocs(response) {
    if (response && response.data) {
      var assocs = angular.fromJson(response.data);
      vm.assocs = assocs;
      vm.nbAssocActive = vm.assocs.filter(function (x) { return !x.pending; }).length;
      vm.nbAssocPending = vm.assocs.filter(function (x) { return x.pending; }).length;
    }
  }

  function exclude(userID) {
    $http({
      method: 'DELETE',
      url: '/api/admin/assoc',
      params: {groupID: vm.user.currentAssoc.group_id, userID: userID}
    })
    .then(handleSuccessfulExclude)
    .catch(handleFailedExclude);
  }

  function handleSuccessfulExclude() {
    vm.getAssocs();
    vm.resetAlerts();
    vm.assocsStatus = true;
    vm.assocsStatusMessage = 'Utilisateur exclu du groupe !';
  }

  function handleFailedExclude(response) {
    vm.resetAlerts();
    vm.assocsError = true;
    vm.assocsErrorMessage = 'Erreur';
    if (response && response.data) {
      vm.assocErrorMessage += ': ' + response.data.message;
    }
  }

  function roleUpdate(userID, role) {
    $http({
      method: 'POST',
      url: '/api/admin/assoc',
      data: {groupID: vm.user.currentAssoc.group_id, userID: userID, role: role}
    })
    .then(handleSuccessfulRoleUpdate)
    .catch(handleFailedRoleUpdate);
  }

  function handleSuccessfulRoleUpdate() {
    vm.getAssocs();
    vm.resetAlerts();
    vm.assocsStatus = true;
    vm.assocsStatusMessage = 'Rôle de l\'utilisateur modifié !';
  }

  function handleFailedRoleUpdate(response) {
    vm.resetAlerts();
    vm.assocsError = true;
    vm.assocsErrorMessage = 'Erreur';
    if (response && response.data) {
      vm.assocErrorMessage += ': ' + response.data.message;
    }
  }

  /*
   * Users invite
   */
  function createFilterFor(query) {
    var lowercaseQuery = angular.lowercase(query);
    return function (user) {
      return (user.id.toString().indexOf(lowercaseQuery) === 0 || angular.lowercase(user.pseudo).indexOf(lowercaseQuery) === 0);
    };
  }

  function queryUserSearch(query) {
    var results = query ? vm.usersList.filter(createFilterFor(query)) : vm.usersList;
    return results;
  }

  function getUsersList() {
    $http({
      method: 'GET',
      url: '/api/usersList'
    })
    .then(handleSuccessfulGetUsersList);
  }

  function handleSuccessfulGetUsersList(response) {
    if (response && response.data) {
      vm.usersList = angular.fromJson(response.data);
    }
  }

  function inviteUser(user) {
    $http({
      method: 'POST',
      url: '/api/admin/invite',
      data: {groupID: vm.user.currentAssoc.group_id, userID: user.id}
    })
    .then(handleSuccessfulInviteUser)
    .catch(handleFailedInviteUser);
  }

  function handleSuccessfulInviteUser() {
    vm.getAssocs();
    vm.resetAlerts();
    vm.inviteStatus = true;
    vm.inviteStatusMessage = 'Utilisateur invité !';
  }

  function handleFailedInviteUser(response) {
    vm.resetAlerts();
    vm.inviteError = true;
    vm.inviteErrorMessage = 'Erreur';
    if (response && response.data) {
      vm.inviteErrorMessage += ': ' + response.data.message;
    }
  }
}
