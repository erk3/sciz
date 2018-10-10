var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'ngCookies', /* 'ngSanitize', */ 'infinite-scroll', 'ngclipboard', 'ngAria', '720kb.tooltips', 'textAngular', 'ui.carousel', 'ngMaterial', 'ngStorage', 'angular-web-notification']);

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
    if (toState !== null && toState.name !== 'home' && toState.data !== null && toState.data.accesLevel !== null) {
      if (authService.isAuthorized(toState.data.accessLevel)) {
        return;
      }
      return trans.router.stateService.target('home');
    }
  });
}
