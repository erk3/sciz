angular
  .module('app')
  .controller('ProfileCtrl', ['$http', profileCtrl]);

function profileCtrl($http) {
  var vm = this;
  vm.updateProfile = updateProfile;
  vm.profile = {};

  vm.updateError = false;
  vm.updateErrorMessage = null;
  vm.updateStatus = false;
  vm.updateStatusMessage = null;

  $http({method: 'GET', url: '/api/profile'})
    .then(function (response) {
      if (response && response.data) {
        vm.profile = response.data;
      }
    });

  function updateProfile() {
    if (vm.old_pwd || vm.new_pwd || vm.pwd) {
      if (vm.pwd !== vm.new_pwd) {
        vm.updateError = true;
        vm.updateErrorMessage = 'Les mots de passent ne correspondent pas';
        return;
      } else if ((vm.pwd.length < 8) || (vm.new_pwd < 8)) {
        vm.updateError = true;
        vm.updateErrorMessage = 'Le mot de passe doit faire au moins 8 caractères';
        return;
      } else if (vm.old_pwd.length <= 0) {
        vm.updateError = true;
        vm.updateErrorMessage = 'L\'ancien mot de passe est obligatoire';
        return;
      }
      vm.profile.old_pwd = vm.old_pwd;
      vm.profile.new_pwd = vm.new_pwd;
      vm.profile.pwd = vm.pwd;
    }

    $http({
      method: 'POST',
      url: '/api/profile',
      data: JSON.stringify(vm.profile)
    })
    .then(handleSuccessfulUpdate)
    .catch(handleFailedUpdate);
  }

  function handleSuccessfulUpdate() {
    vm.old_pwd = null;
    vm.new_pwd = null;
    vm.pwd = null;
    vm.updateError = false;
    vm.updateErrorMessage = null;
    vm.updateStatus = true;
    vm.updateStatusMessage = 'Modifications enregistrées';
  }

  function handleFailedUpdate(response) {
    vm.old_pwd = null;
    vm.new_pwd = null;
    vm.pwd = null;
    vm.updateError = true;
    vm.updateErrorMessage = 'Erreur';
    vm.updateStatus = false;
    vm.updateStatusMessage = null;
    if (response && response.data) {
      vm.updateErrorMessage += ': ' + response.data.message;
    }
  }
}
