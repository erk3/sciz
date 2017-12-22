angular
  .module('app')
  .controller('PadCtrl', ['$scope', '$http', 'authService', padCtrl]);

function padCtrl($scope, $http, authService) {
  var vm = this;

  vm.firstLoad = true;
  vm.htmlPAD = '';
  vm.user = authService.refreshLocalData();

  $http({
    method: 'GET',
    url: '/api/pad',
    params: {groupID: vm.user.currentAssoc.group_id}
  })
    .then(successCallBack, errorCallBack);

  vm.updatePAD = function () {
    if (!vm.firstLoad) {
      $http({
        method: 'POST',
        url: '/api/pad',
        data: '{"pad" : ' + JSON.stringify(vm.htmlPAD) + ', "groupID" : ' + vm.user.currentAssoc.group_id + '}'
      })
        .then(successCallBack, errorCallBack);
    }
  };

  function successCallBack(response) {
    if (response.data) {
      var res = angular.fromJson(response.data).value;
      vm.htmlPAD = (res && (res !== '')) ? res : vm.htmlPAD;
      vm.firstLoad = false;
    }
  }

  function errorCallBack() {}

  $scope.$watch('pc.htmlPAD', vm.updatePAD);
}
