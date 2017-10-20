angular
  .module('app')
  .controller('EventsCtrl', ['$http', eventsCtrl]);

function eventsCtrl($http) {
  var vm = this;
  vm.searchValue = '';
  vm.events = [];
  vm.cur = {};

  $http({method: 'GET', url: '/api/events'})
    .then(function (response) {
      if (response && response.data) {
        vm.events = angular.fromJson(response.data);
        for (var i = 0, len = vm.events.length; i < len; i++) {
          vm.events[i].sub = (vm.events[i].cdm) ? vm.events[i].cdm : vm.events[i].battle_event;
        }
        vm.switchTrigger(vm.events[0]);
      }
    });

  vm.switchTrigger = function (event) {
    vm.cur = event;
    if (event.cdm) {
      // Progress bar
      vm.cur.cdm.life_percent = 100 - vm.cur.cdm.blessure;
      var rPvMin = (vm.cur.cdm.pv_min ? vm.cur.cdm.pv_min : vm.cur.cdm.pv_max);
      vm.cur.cdm.pv_min_blessure = Math.max(1, Math.floor(rPvMin * vm.cur.cdm.life_percent / 100));
      var rPvMax = (vm.cur.cdm.pv_max ? vm.cur.cdm.pv_max : vm.cur.cdm.pv_mmin);
      if (vm.cur.cdm.pv_max) {
        vm.cur.cdm.pv_max_blessure = Math.floor(rPvMax * vm.cur.cdm.life_percent / 100);
      } else {
        vm.cur.cdm.pv_max_blessure = Math.max(100, Math.floor(Math.floor(rPvMax * vm.cur.cdm.life_percent / 100) * 1.2));
      }
      // Capa desc
      vm.cur.cdm.capa = '';
      vm.cur.cdm.capa += (vm.cur.cdm.capa_desc) ? vm.cur.cdm.capa_desc : '';
      vm.cur.cdm.capa += (vm.cur.cdm.capa_effet) ? ' - Affecte : ' + vm.cur.cdm.capa_effet : '';
      vm.cur.cdm.capa += (vm.cur.cdm.capa_tour) ? ' - ' + vm.cur.cdm.capa_tour + 'T' : '';
      vm.cur.cdm.capa += (vm.cur.cdm.portee_capa) ? ' (' + vm.cur.cdm.portee_capa + ')' : '';
      vm.cur.cdm.capa = vm.cur.cdm.capa.trim();
    }
  };

  /*
   * Search logic
   */
  vm.search = function () {
    return function (event) {
      if (!vm.searchValue || vm.searchValue.length === 0) {
        return true;
      }
      var w = vm.searchValue.split(' ');
      var index = 0;
      var len = 0;
      var key = null;
      for (index = 0, len = w.length; index < len; ++index) {
        var foundWord = false;
        for (key in event) {
          if (event[key] && event[key].toString().toLowerCase().indexOf(w[index].toLowerCase()) >= 0) {
            foundWord = true;
            break;
          }
        }
        if (!foundWord) {
          for (key in event.sub) {
            if (event.sub[key] && event.sub[key].toString().toLowerCase().indexOf(w[index].toLowerCase()) >= 0) {
              foundWord = true;
              break;
            }
          }
        }
        if (!foundWord) {
          return false;
        }
      }
      return true;
    };
  };

  /*
   * Utils
   */
  vm.displayDate = function (date) {
    var d = new Date(date);
    var day = ('0' + d.getDate()).slice(-2);
    var mon = ('0' + (d.getMonth() + 1)).slice(-2);
    var hou = ('0' + d.getHours()).slice(-2);
    var min = ('0' + d.getMinutes()).slice(-2);
    var sec = ('0' + d.getSeconds()).slice(-2);
    return day + '/' + mon + ' ' + hou + ':' + min + ':' + sec;
  };

  vm.displayMinMax = function (min, max, short) {
    if (min && max) {
      if (min === max) {
        if (short) {
          return max;
        }
        return 'égal à ' + max;
      }
      if (short) {
        return min + ' - ' + max;
      }
      return 'entre ' + min + ' et ' + max;
    } else if (max) {
      if (short) {
        return '< ' + max;
      }
      return 'inférieur à' + max;
    } else if (min) {
      if (short) {
        return '> ' + min;
      }
      return 'supérieur à' + min;
    }
    return '-';
  };

  vm.displayAverage = function (min, max, mul) {
    mul = (mul) ? mul : 1;
    if (min && max) {
      return Math.floor(((parseInt(min, 10) + parseInt(max, 10)) / 2) * mul);
    }
    return '-';
  };
}
