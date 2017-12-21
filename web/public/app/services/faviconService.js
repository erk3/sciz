angular
  .module('app')
  .factory('faviconService', [
    '$window',
    faviconService
  ]);

function faviconService($window) {
  var faviconService = {
    badge: badge,
    reset: reset,
    add: add
  };

  var gCount = 0;

  var favico = new Favico({
    position: 'down',
    animation: 'none'
    // ddbgColor: '#5CB85C',
    // textColor: '#ff0'
  });

  return faviconService;

  function add(count) {
    gCount += count;
    badge(gCount);
  }

  function badge(count) {
    if (count <= 0) {
      reset();
    } else {
      favico.badge(count);
      $window.document.title = count + ' - SCIZ';
    }
  }

  function reset() {
    gCount = 0;
    favico.reset();
    $window.document.title = 'SCIZ';
  }
}
