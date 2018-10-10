angular
  .module('app')
  .factory('notificationService', [
    'webNotification',
    notificationService
  ]);

function notificationService(webNotification) {
  var notificationService = {
    show: show
  };

  return notificationService;

  function show(g, e) {
    webNotification.showNotification('SCIZ - ' + g, {body: e, icon: 'images/favicon-64.png', onClick: function () {}, autoClose: 30000}, function () {});
  }
}
