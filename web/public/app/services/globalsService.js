angular
  .module('app')
  .factory('globalService', [
    globalService
  ]);

function globalService() {
  var globalService = {
    starded: false
  };

  return globalService;
}
