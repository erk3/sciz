angular
  .module('app')
  .config(routesConfig);

var staticData = {};

staticData.userRoles = {
  guest: 1,
  user: 2,
  admin: 4
};

staticData.accessLevels = {
  guest: staticData.userRoles.guest | staticData.userRoles.user | staticData.userRoles.admin,
  user: staticData.userRoles.user | staticData.userRoles.admin,
  admin: staticData.userRoles.admin
};

/** @ngInject */
function routesConfig($stateProvider, $urlRouterProvider, $httpProvider, $locationProvider) {
  $locationProvider.html5Mode(true).hashPrefix('!');
  $urlRouterProvider.otherwise('/');

  $stateProvider
    .state('home', {
      url: '/',
      templateUrl: 'app/views/home.html',
      controller: 'HomeCtrl as hc'
    });

  $stateProvider
    .state('events', {
      url: '/events',
      templateUrl: 'app/views/events.html',
      controller: 'EventsCtrl as ec',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $stateProvider
    .state('profile', {
      url: '/settings',
      templateUrl: 'app/views/settings.html',
      controller: 'ProfileCtrl as pc',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $stateProvider
    .state('admin', {
      url: '/admin',
      templateUrl: 'app/views/admin.html',
      controller: 'AdminCtrl as ac',
      data: {
        accessLevel: staticData.accessLevels.admin
      }
    });

  $stateProvider
    .state('help', {
      url: '/help',
      templateUrl: 'app/views/help.html',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $stateProvider
    .state('trolls', {
      url: '/trolls',
      templateUrl: 'app/views/trolls.html',
      controller: 'TrollsCtrl as tc',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $stateProvider
    .state('pad', {
      url: '/pad',
      templateUrl: 'app/views/pad.html',
      controller: 'PadCtrl as pc',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $stateProvider
    .state('view', {
      url: '/view',
      templateUrl: 'app/views/view.html',
      controller: 'ViewCtrl as vc',
      data: {
        accessLevel: staticData.accessLevels.user
      }
    });

  $httpProvider.interceptors.push('requestInterceptor');
}
