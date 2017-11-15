angular
  .module('app')
  .factory('authService', [
    '$http',
    '$cookies',
    '$state',
    '$window',
    authService
  ]);

function authService($http, $cookies, $state, $window) {
  var authService = {
    login: login,
    logout: logout,
    // signup: signup,
    isAuthenticated: isAuthenticated,
    isAuthorized: isAuthorized,
    refreshLocalData: refreshLocalData,
    updateLocalData: updateLocalData,
    updateGroup: updateGroup,
    changeGroup: changeGroup,
    dataWrap: {}
  };

  return authService;

  function login(id, pwd) {
    var reqObj = {
      method: 'POST',
      url: '/api/authenticate',
      data: {
        id: id,
        pwd: pwd
      }
    };

    return $http(reqObj).then(function (response) {
      if (response && response.data) {
        response = response.data;

        var user = {};
        user.id = response.id;
        user.pseudo = response.pseudo;
        user.assocs = response.assocs;
        user.token = response.token;
        authService.dataWrap.user = user;
        if (user.assocs !== null) {
          authService.changeGroup(user.assocs[0].group_id);
        }
        authService.dataWrap.user = user;

        authService.updateLocalData();
      }
    });
  }

  function logout() {
    $cookies.remove('user');
    $state.go('login');
  }

  function isAuthenticated() {
    authService.refreshLocalData();
    return authService.dataWrap.user && authService.dataWrap.user !== 'undefined';
  }

  function updateGroup(group) {
    var user = authService.dataWrap.user;
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === group.id) {
        user.assocs[i].group.name = group.name;
        user.assocs[i].group.blason_url = group.blason_url;
        user.assocs[i].group.desc = group.desc;
        user.currentAssoc = user.assocs[i];
        if (user.currentAssoc.group.blason_url === null) {
          user.currentAssoc.group.blason_url = 'http://blason.mountyhall.com/Blason_PJ_MyNameIsNobody.gif';
        }
      }
    }
    authService.dataWrap.user = user;
    return authService.updateLocalData();
  }

  function changeGroup(index) {
    var user = authService.dataWrap.user;
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === index) {
        user.currentAssoc = user.assocs[i];
        if (user.currentAssoc.group.blason_url === null) {
          user.currentAssoc.group.blason_url = 'http://blason.mountyhall.com/Blason_PJ_MyNameIsNobody.gif';
        }
      }
    }
    authService.dataWrap.user = user;
    authService.updateLocalData();
    $window.location.reload();
  }

  function refreshLocalData() {
    authService.dataWrap.user = $cookies.getObject('user');
    return authService.dataWrap.user;
  }

  function updateLocalData() {
    var expires = new Date();
    expires.setTime(expires.getTime() + (30 * 60 * 1000));
    $cookies.putObject(
      'user',
      authService.dataWrap.user,
      {expires: expires}
    );
    return authService.refreshLocalData();
  }

  function isAuthorized(levelAccess) {
    if (!isAuthenticated()) {
      return false;
    }
    var user = authService.dataWrap.user;
    if (user.assocs !== null) {
      for (var i = 0; i < user.assocs.length; i++) {
        if ((user.assocs[i].group_id === user.currentAssoc.group_id) && (levelAccess & user.assocs[i].role)) {
          return true;
        }
      }
    }
    return false;
  }

  /*
  function signup(id, pwd) {
    var reqObj = {
      method: 'POST',
      url: '/api/signup',
      data: {
        id: id,
        pwd: pwd
      }
    };
    return $http(reqObj);
  }
  */
}
