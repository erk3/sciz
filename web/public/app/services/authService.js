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
        if (user.assocs !== null) {
          user.currentGroupID = user.assocs[0].group_id;
          user.currentGroupName = user.assocs[0].group.name;
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

  function changeGroup(index) {
    var user = authService.dataWrap.user;
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === index) {
        user.currentGroupID = index;
        user.currentGroupName = user.assocs[i].group.name;
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
        if ((user.assocs[i].group_id === user.currentGroupID) && (levelAccess & user.assocs[i].role)) {
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
