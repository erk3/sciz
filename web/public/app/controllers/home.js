angular
  .module('app')
  .controller('HomeCtrl', ['$state', '$http', 'authService', homeCtrl]);

function homeCtrl($state, $http, authService) {
  var vm = this;

  vm.loginError = false;
  vm.loginErrorMessage = null;

  vm.login = login;
  vm.testLogin = testLogin;
  vm.signup = signup;

  vm.view = 'login'; // can also be 'signup'

  vm.user = authService.refreshLocalData();

  function testLogin() {
    vm.id = '0';
    vm.pwd = 'test';
    vm.login();
  }

  function login() {
    vm.loginError = false;
    vm.loginErrorMessage = null;

    if (!vm.id || !vm.pwd) {
      vm.loginError = true;
      vm.loginErrorMessage = 'Identifiant et mot de passe requis !';
      return;
    }

    authService.login(vm.id, vm.pwd)
      .then(handleSuccessfulLogin)
      .catch(handleFailedLogin);
  }

  function handleSuccessfulLogin() {
    $state.go('events');
  }

  function handleFailedLogin(response) {
    if (response && response.data) {
      vm.loginError = true;
      vm.loginErrorMessage = response.data.message;
    }
  }

  function signup() {
    vm.signupError = false;
    vm.signupErrorMessage = null;

    if (!vm.id || !vm.pwd || !vm.pwd2 || !vm.mh_apikey || vm.pwd.length < 8 || vm.pwd !== vm.pwd2) {
      vm.signupError = true;
      vm.signupErrorMessage = 'Erreur dans le formulaire !';
      return;
    }

    $http({
      method: 'POST',
      url: '/api/signup',
      data: {
        id: vm.id,
        pwd: vm.pwd,
        mh_apikey: vm.mh_apikey
      }
    })
      .then(handleSuccessfulSignup)
      .catch(handleFailedSignup);
  }

  function handleSuccessfulSignup() {
    authService.login(vm.id, vm.pwd)
      .then(handleSuccessfulLogin)
      .catch(handleFailedSignup);
  }

  function handleFailedSignup(response) {
    if (response && response.data) {
      vm.signupError = true;
      vm.signupErrorMessage = 'Erreur : ' + response.data.message;
    }
  }
}
