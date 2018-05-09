angular
  .module('app')
  .factory('authService', [
    '$http',
    '$cookies',
    '$state',
    '$window',
    '$localStorage',
    authService
  ]);

function authService($http, $cookies, $state, $window, $localStorage) {
  var authService = {
    login: login,
    logout: logout,
    isAuthenticated: isAuthenticated,
    isAuthorized: isAuthorized,
    refreshLocalData: refreshLocalData,
    updateLocalData: updateLocalData,
    refreshGroups: refreshGroups,
    updateGroup: updateGroup,
    changeGroup: changeGroup,
    getGroup: getGroup,
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
        user.token = response.token;
        var expires = new Date();
        var time = response.session_duration;
        time = (time) ? time : 30;
        expires.setTime(expires.getTime() + (time * 60 * 1000));
        $cookies.putObject(
          'user',
          user,
          {expires: expires}
        );

        // Local Storage
        user.pseudo = response.pseudo;
        user.session_duration = response.session_duration;
        user.default_group_id = response.default_group_id;
        user.assocs = response.assocs;
        user.blasonURL = response.blasonURL;

        authService.dataWrap.user = user;
        authService.updateLocalData();

        if (user.assocs !== null && user.assocs.length > 0) {
          var index = (user.default_group_id) ? user.default_group_id : user.assocs[0].group_id;
          authService.changeGroup(index, false);
        }
      }
    });
  }

  function logout() {
    $cookies.remove('user');
    $state.go('home');
  }

  function isAuthenticated() {
    var scizCookie = $cookies.getObject('user');
    return scizCookie && scizCookie !== null && scizCookie !== 'undefined';
  }

  function refreshGroups() {
    var reqObj = {
      method: 'GET',
      url: '/api/assocs'
    };

    $http(reqObj).then(function (response) {
      if (response && response.data) {
        authService.dataWrap.user.assocs = response.data;
        authService.updateLocalData();
      }
    });
  }

  function updateGroup(group) {
    var user = refreshLocalData();
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === group.id) {
        user.assocs[i].group.name = group.name;
        user.assocs[i].group.blason_url = group.blason_url;
        user.assocs[i].group.desc = group.desc;
        user.currentAssoc = user.assocs[i];
        if (user.currentAssoc.group.blason_url === null) {
          user.currentAssoc.group.blason_url = 'images/MyNameIsNobody.gif';
        }
      }
    }
    authService.dataWrap.user = user;
    return authService.updateLocalData();
  }

  function getGroup(index) {
    var user = refreshLocalData();
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === index) {
        return user.assocs[i].group;
      }
    }
    return {};
  }

  function changeGroup(index, reload) {
    var user = refreshLocalData();
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id === index) {
        user.currentAssoc = user.assocs[i];
        if (user.currentAssoc.group.blason_url === null) {
          user.currentAssoc.group.blason_url = 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
        }
      }
    }
    authService.dataWrap.user = user;
    authService.updateLocalData();
    if (reload) {
      $window.location.reload();
    }
  }

  function refreshLocalData() {
    authService.dataWrap.user = $localStorage.user;
    return authService.dataWrap.user;
  }

  function updateLocalData() {
    $localStorage.user = authService.dataWrap.user;
  }

  function isAuthorized(levelAccess) {
    if (!isAuthenticated()) {
      return false;
    }
    var user = refreshLocalData();
    if (user && user.assocs !== null) {
      for (var i = 0; i < user.assocs.length; i++) {
        if ((user.assocs[i].group_id === user.currentAssoc.group_id) && (levelAccess & user.assocs[i].role)) {
          return true;
        }
      }
    }
    return false;
  }
}
