angular
  .module('app')
  .controller('LoginCtrl', ['$state', 'authService', loginCtrl]);

function loginCtrl($state, authService) {
  var vm = this;

  vm.loginError = false;
  vm.loginErrorMessage = null;

  vm.login = login;
  vm.testLogin = testLogin;

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
      vm.loginErrorMessage = response.data.message;
      vm.loginError = true;
    }
  }
}
