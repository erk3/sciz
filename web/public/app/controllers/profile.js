angular
  .module('app')
  .controller('ProfileCtrl', ['$http', 'authService', profileCtrl]);

function profileCtrl($http, authService) {
  var vm = this;
  vm.updateProfile = updateProfile;
  vm.profile = {};

  vm.user = authService.refreshLocalData();

  vm.updateError = false;
  vm.updateErrorMessage = null;
  vm.updateStatus = false;
  vm.updateStatusMessage = null;

  $http({method: 'GET', url: '/api/profile'})
    .then(function (response) {
      if (response && response.data) {
        vm.profile = response.data;
        vm.profile.blasonUrl = vm.profile.trolls.find(function (troll) {
          return troll.blason_url !== null;
        });
        vm.profile.blasonUrl = (vm.profile.blasonUrl) ? vm.profile.blasonUrl : 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
      }
    });

  function updateProfile() {
    if (vm.oldPwd || vm.newPwd || vm.pwd) {
      if (vm.pwd !== vm.newPwd) {
        vm.updateError = true;
        vm.updateErrorMessage = 'Les mots de passent ne correspondent pas';
        return;
      } else if ((vm.pwd.length < 8) || (vm.newPwd < 8)) {
        vm.updateError = true;
        vm.updateErrorMessage = 'Le mot de passe doit faire au moins 8 caractères';
        return;
      } else if (vm.oldPwd.length <= 0) {
        vm.updateError = true;
        vm.updateErrorMessage = 'L\'ancien mot de passe est obligatoire';
        return;
      }
      vm.profile.oldPwd = vm.oldPwd;
      vm.profile.newPwd = vm.newPwd;
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
    vm.oldPwd = null;
    vm.newPwd = null;
    vm.pwd = null;
    vm.updateError = false;
    vm.updateErrorMessage = null;
    vm.updateStatus = true;
    vm.updateStatusMessage = 'Modifications enregistrées';
  }

  function handleFailedUpdate(response) {
    vm.oldPwd = null;
    vm.newPwd = null;
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
