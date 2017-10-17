angular
  .module('app')
  .controller('LoginCtrl', ['$state', 'authService', loginCtrl]);

function loginCtrl($state, authService) {
  var vm = this;

  vm.loginError = false;
  vm.loginErrorMessage = null;

  vm.login = login;

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

    $state.go('events');
  }

  function handleSuccessfulLogin() {
    $state.go('index');
  }

  function handleFailedLogin(response) {
    if (response && response.data) {
      vm.loginErrorMessage = response.data.message;
      vm.loginError = true;
    }
  }
}
