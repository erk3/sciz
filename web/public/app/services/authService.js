angular
  .module('app')
  .factory('authService', [
    '$http',
    '$cookies',
    '$state',
    authService
  ]);

function authService($http, $cookies, $state) {
  var authService = {
    login: login,
    logout: logout,
    // signup: signup,
    getUserData: getUserData,
    isAuthenticated: isAuthenticated
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

        var expires = new Date();
        var user = {};

        user.id = response.id;
        user.pseudo = response.pseudo;
        user.role = response.role;
        user.token = response.token;

        expires.setTime(expires.getTime() + (30 * 60 * 1000));

        $cookies.put(
          'user',
          JSON.stringify(user),
          {expires: expires}
        );
      }
    });
  }

  function logout() {
    $cookies.remove('user');
    $state.go('login');
  }

  function isAuthenticated() {
    var user = $cookies.get('user');
    return user && user !== 'undefined';
  }

  function getUserData() {
    if (isAuthenticated()) {
      return JSON.parse($cookies.get('user'));
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
