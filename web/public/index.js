var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'ngCookies', 'ngSanitize', 'infinite-scroll']);

app.run([
  '$rootScope',
  '$state',
  '$transitions',
  'authService',
  authRun
]);

function authRun($rootScope, $state, $transitions, authService) {
  $rootScope.authService = authService;
  $transitions.onStart({to: '*'}, function (trans) {
    var toState = trans.to();
    if (toState.name !== 'login') {
      if (authService && authService.isAuthenticated()) {
        var user = authService.getUserData();
        if (user && toState.data && toState.data.accessLevel) {
          if (toState.data.accessLevel & user.role) {
            return;
          }
        }
      }
      return trans.router.stateService.target('login');
    }
  });
}
