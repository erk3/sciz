angular
  .module('app')
  .controller('ProfileCtrl', ['$http', '$window', '$document', 'authService', profileCtrl]);

function profileCtrl($http, $window, $document, authService) {
  var vm = this;
  const stepDynSpRefresh = 2;
  const stepStaticSpRefresh = 0;

  vm.updateProfile = updateProfile;
  vm.deleteAccount = deleteAccount;
  vm.resetAlerts = resetAlerts;
  vm.profile = {};
  vm.view = 'profile';

  vm.user = authService.refreshLocalData();

  vm.updateError = false;
  vm.updateErrorMessage = null;
  vm.updateStatus = false;
  vm.updateStatusMessage = null;
  vm.deleteError = false;
  vm.deleteErrorMessage = null;

  vm.deleteConfirmation = false;

  $http({method: 'GET', url: '/api/profile'})
    .then(function (response) {
      if (response && response.data) {
        vm.profile = response.data;
        vm.dynSpRefresh = (vm.profile.dyn_sp_refresh === 0) ? 0 : 24 * 60 * stepDynSpRefresh / vm.profile.dyn_sp_refresh;
        vm.staticSpRefresh = (vm.profile.static_sp_refresh === 0) ? 0 : 24 * 60 * stepStaticSpRefresh / vm.profile.static_sp_refresh;
        if (vm.profile.trolls && vm.profile.trolls[0]) {
          vm.profile.blasonUrl = vm.profile.trolls[0].blason_url;
          vm.profile.nom = vm.profile.trolls[0].nom;
        } else {
          vm.profile.blasonURL = 'images/MyNameIsNobody.gif';
        }
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

    vm.profile.dyn_sp_refresh = (vm.dynSpRefresh === 0) ? 0 : 24 * 60 * stepDynSpRefresh / vm.dynSpRefresh;
    vm.profile.static_sp_refresh = (vm.staticSpRefresh === 0) ? 0 : 24 * 60 * stepStaticSpRefresh / vm.staticSpRefresh;

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
    resetAlerts();
    vm.updateStatus = true;
    vm.updateStatusMessage = 'Modifications enregistrées';
  }

  function handleFailedUpdate(response) {
    vm.oldPwd = null;
    vm.newPwd = null;
    vm.pwd = null;
    resetAlerts();
    vm.updateError = true;
    vm.updateErrorMessage = 'Erreur';
    if (response && response.data) {
      vm.updateErrorMessage += ': ' + response.data.message;
    }
  }

  function resetAlerts() {
    vm.updateError = false;
    vm.updateErrorMessage = null;
    vm.updateStatus = false;
    vm.updateStatusMessage = null;
    vm.deleteError = false;
    vm.deleteErrorMessage = null;
  }
  
  function deleteAccount() {
    $http({
      method: 'DELETE',
      url: '/api/profile'
    })
    .then(handleSuccessfulDelete)
    .catch(handleFailedDelete);
  }

  function handleSuccessfulDelete() {
    authService.logout();
  }

  function handleFailedDelete(response) {
    resetAlerts();
    vm.deleteError = true;
    vm.deleteErrorMessage = 'Erreur';
    if (response && response.data) {
      vm.deleteErrorMessage += ': ' + response.data.message;
    }
  }}
