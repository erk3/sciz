var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'ngCookies', 'ngSanitize', 'infinite-scroll', 'ngclipboard', 'ngAria', '720kb.tooltips']);

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
    if (toState && toState.name !== 'login' && toState.data && toState.data.accesLevel) {
      if (authService.isAuthorized(toState.data.accessLevel)) {
        return;
      }
      return trans.router.stateService.target('login');
    }
  });
}
