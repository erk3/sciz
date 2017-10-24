angular
  .module('app')
  .controller('EventsCtrl', ['$http', '$window', eventsCtrl]);

function eventsCtrl($http, $window) {
  var vm = this;
  vm.searchValue = '';
  vm.events = [];
  vm.cur = {};
  vm.offset = 0;
  vm.busy = false;
  vm.noMoreEvent = false;

  vm.switchTrigger = function (event) {
    vm.cur = event;
    if (event.cdm) {
      vm.switchCDM();
    } else {
      vm.switchBATTLE();
    }
    $window.scrollTo(0, 0);
  };

  vm.loadMoreEvents = function () {
    if (vm.busy || vm.noMoreEvent) {
      return;
    }
    vm.busy = true;
    $http({method: 'GET', url: '/api/events', params: {offset: vm.offset}})
      .then(function (response) {
        if (response && response.data) {
          var events = angular.fromJson(response.data);
          for (var i = 0, len = events.length; i < len; i++) {
            events[i].sub = (events[i].cdm) ? events[i].cdm : events[i].battle_event;
          }
          var oldLength = vm.events.length;
          vm.events = vm.events.concat(events);
          if (oldLength <= 0) {
            vm.switchTrigger(vm.events[0]);
          }
          if (vm.events.length > 0) {
            vm.offset += vm.events.length;
          }
          if (events.length <= 0) {
            vm.noMoreEvent = true;
          }
          vm.busy = false;
        }
      });
  };

  /*
   * BATTLE logic
   */
  vm.switchBATTLE = function () {
    vm.cur.isDead = (vm.cur.battle_event.type.indexOf('mortelle') !== -1);
    vm.cur.isTouched = (vm.cur.battle_event.att > vm.cur.battle_event.esq);
    vm.cur.isCrit = (vm.cur.battle_event.att >= vm.cur.battle_event.esq * 2);
    vm.cur.isFull = (vm.cur.battle_event.resi >= vm.cur.battle_event.sr);
  };

  /*
   * CDM logic
   */
  vm.switchCDM = function () {
    // Progress bar
    vm.cur.cdm.lifePercent = 100 - vm.cur.cdm.blessure;
    var rPvMin = (vm.cur.cdm.pv_min ? vm.cur.cdm.pv_min : vm.cur.cdm.pv_max);
    vm.cur.cdm.pvMinBlessure = Math.max(1, Math.floor(rPvMin * vm.cur.cdm.lifePercent / 100));
    var rPvMax = (vm.cur.cdm.pv_max ? vm.cur.cdm.pv_max : vm.cur.cdm.pv_mmin);
    if (vm.cur.cdm.pv_max) {
      vm.cur.cdm.pvMaxBlessure = Math.floor(rPvMax * vm.cur.cdm.lifePercent / 100);
    } else {
      vm.cur.cdm.pvMaxBlessure = Math.max(100, Math.floor(Math.floor(rPvMax * vm.cur.cdm.lifePercent / 100) * 1.2));
    }
    // Capa desc
    vm.cur.cdm.capa = '';
    vm.cur.cdm.capa += (vm.cur.cdm.capa_desc) ? vm.cur.cdm.capa_desc : '';
    vm.cur.cdm.capa += (vm.cur.cdm.capa_effet) ? ' - Affecte : ' + vm.cur.cdm.capa_effet : '';
    vm.cur.cdm.capa += (vm.cur.cdm.capa_tour) ? ' - ' + vm.cur.cdm.capa_tour + 'T' : '';
    vm.cur.cdm.capa += (vm.cur.cdm.portee_capa) ? ' (' + vm.cur.cdm.portee_capa + ')' : '';
    vm.cur.cdm.capa = vm.cur.cdm.capa.trim();
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

  vm.isRelatedToCur = function (event) {
    // Cur Event
    var curAttID = null;
    curAttID = (vm.cur.battle_event) ? ((vm.cur.battle_event.att_troll_id) ? vm.cur.battle_event.att_troll_id : vm.cur.battle_event.att_mob_id) : null;
    var curDefID = (vm.cur.cdm) ? (vm.cur.cdm.mob_id) : null;
    curDefID = (vm.cur.battle_event) ? ((vm.cur.battle_event.def_troll_id) ? vm.cur.battle_event.def_troll_id : vm.cur.battle_event.def_mob_id) : null;
    // Event
    var eAttID = (event.cdm) ? (event.cdm.troll_id) : null;
    eAttID = (event.battle_event) ? ((event.battle_event.att_troll_id) ? event.battle_event.att_troll_id : event.battle_event.att_mob_id) : null;
    var eDefID = (event.cdm) ? (event.cdm.mob_id) : null;
    eDefID = (event.battle_event) ? ((event.battle_event.def_troll_id) ? event.battle_event.def_troll_id : event.battle_event.def_mob_id) : null;
    if ((curAttID !== null) && (curDefID !== null)) {
      return ((curAttID === eAttID) && (curDefID === eDefID)) || ((curDefID === eAttID) && (curAttID === eDefID));
    } else if (curAttID !== null) {
      return (curAttID === eAttID) || (curAttID === eDefID);
    }
    return (curDefID === eAttID) || (curDefID === eDefID);
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
