angular
    .module('app')
    .factory('requestInterceptor', [
      '$cookies',
      requestInterceptor
    ]);

function requestInterceptor($cookies) {
  return {
    request: function (config) {
      var user = $cookies.get('user');
      var token = null;

      if (user !== null && user !== undefined) {
        user = JSON.parse(user);
        token = user.token ? user.token : null;
      }

      if (token) {
        config.headers = config.headers || {};
        config.headers.Authorization = token;
      }
      return config;
    }
  };
}
