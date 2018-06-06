angular
  .module('app')
  .controller('EventsCtrl', ['$http', '$window', 'authService', 'faviconService', 'globalService', eventsCtrl]);

function eventsCtrl($http, $window, authService, faviconService, globalService) {
  var vm = this;
  vm.searchValue = '';
  vm.events = [];
  vm.cur = {};
  vm.offset = 0;
  vm.lastID = 0;
  vm.busy = false;
  vm.noMoreEvent = false;
  vm.blasonError = 'images/MyNameIsNobody.gif';

  vm.user = authService.refreshLocalData();

  $window.onfocus = function () {
    faviconService.reset();
  };

  $window.onblur = function () {
    faviconService.reset();
  };

  // Refresh the events every minute
  if (!globalService.started) {
    globalService.started = true;
    $window.setInterval(function () {
      vm.loadMoreEvents(false);
    }, 30000);
  }

  vm.switchTrigger = function (event) {
    vm.cur = event;
    if (event.cdm_id !== null) {
      vm.switchCDM();
    } else if (event.battle_id !== null) {
      vm.switchBATTLE();
    } else if (event.piege_id !== null) {
      vm.switchPIEGE();
    } else if (event.portal_id !== null) {
      vm.switchPORTAL();
    } else if (event.idc_id !== null) {
      vm.switchIDC();
    } else if (event.aa_id !== null) {
      vm.switchAA();
    }
    $window.scrollTo(0, 0);
  };

  /*
   * Event displayer
   */

  vm.displayShortEvent = function (e, decorator) {
    var time = vm.displayDate(e.sub.time);
    var s = '';
    var att_decorator_f = (decorator) ? '<span style="color: #856404"><b>' : '';
    var def_decorator_f = (decorator) ? '<span style="color: #0C5460"><b>' : '';
    var decorator_b = (decorator) ? '</b></span>' : '';
    if (e.battle_id) {
      var att = (e.sub.att_troll_id) ? e.sub.att_troll.nom + ' (' + e.sub.att_troll.id + ')' : '';
      att = (e.sub.att_mob_id) ? e.sub.att_mob.nom + ' [' + e.sub.att_mob.age + '] (' + e.sub.att_mob.id + ')' : att;
      var def = (e.sub.def_troll_id) ? e.sub.def_troll.nom + ' (' + e.sub.def_troll.id + ')' : '';
      def = (e.sub.def_mob_id) ? e.sub.def_mob.nom + ' [' + e.sub.def_mob.age + '] (' + e.sub.def_mob.id + ')' : def;
      var action = (e.sub.type) ? e.sub.type : '';
      action += (e.sub.subtype) ? (action ? ' (' + e.sub.subtype + ')' : e.sub.subtype) : '';
      s = time + ' ' + action;
      s += (att) ? ' de ' + att_decorator_f + att + decorator_b : '';
      s += (def) ? ' sur ' + def_decorator_f + def + decorator_b : '';
    } else if (e.cdm_id) {
      s = time + ' Connaissance des Monstres (' + e.sub.comp_niv + ') de ' + att_decorator_f + e.sub.troll.nom + ' (' + e.sub.troll.id + ')' + decorator_b + ' sur ' + def_decorator_f + e.sub.mob.nom + ' [' + e.sub.mob.age + '] (' + e.sub.mob.id + ')' + decorator_b;
    } else if (e.aa_id) {
      s = time + ' Analyse Anatomique de ' + att_decorator_f + e.sub.troll.nom + ' (' + e.sub.troll.id + ')' + decorator_b + ' sur ' + def_decorator_f + e.sub.troll_cible.nom + ' (' + e.sub.troll_cible.id + ')' + decorator_b;
    } else if (e.piege_id) {
      s = time + ' Pose d\'un piège à ' + e.sub.type + ' en X = ' + e.sub.posx + ' Y = ' + e.sub.posy + ' N = ' + e.sub.posn;
    } else if (e.portal_id) {
      s = time + ' Portail de ' + e.sub.troll.nom + ' (' + e.sub.troll.id + ') en X = ' + e.sub.posx + ' Y = ' + e.sub.posy + ' N = ' + e.sub.posn + ' vers X = ' + e.sub.dst_posx + ' Y = ' + e.sub.dst_posy + ' N = ' + e.sub.dst_posn;
    } else if (e.idc_id) {
      s = time + ' Identification de ' + e.sub.troll.nom + ' (' + e.sub.troll.id + ') d\'un ' + e.sub.type + ' ' + e.sub.qualite;
    }
    return s;
  };

  /*
   * Event loader
   */
  vm.loadMoreEvents = function (old) {
    var cOffset = (old) ? vm.offset : 0;
    var cLastID = (old) ? 0 : Math.max.apply(Math, vm.events.map(function (e) {
      return e.id;
    }));
    cLastID = (cLastID < 0) ? 0 : cLastID;
    if (vm.busy || (vm.noMoreEvent && old)) {
      return;
    }
    vm.busy = true;
    $http({method: 'GET', url: '/api/events', params: {offset: cOffset, lastID: cLastID, groupID: vm.user.currentAssoc.group_id}})
      .then(function (response) {
        if (response && response.data) {
          var events = angular.fromJson(response.data);
          for (var i = 0, len = events.length; i < len; i++) {
            events[i].sub = (events[i].cdm_id === null) ? events[i].sub : events[i].cdm;
            events[i].sub = (events[i].battle_id === null) ? events[i].sub : events[i].battle;
            events[i].sub = (events[i].piege_id === null) ? events[i].sub : events[i].piege;
            events[i].sub = (events[i].portal_id === null) ? events[i].sub : events[i].portal;
            events[i].sub = (events[i].idc_id === null) ? events[i].sub : events[i].idc;
            events[i].sub = (events[i].aa_id === null) ? events[i].sub : events[i].aa;
          }
          var oldLength = vm.events.length;
          vm.events = (old) ? vm.events.concat(events) : events.concat(vm.events);
          if (oldLength <= 0) {
            if (vm.events.length > 0) {
              vm.switchTrigger(vm.events[0]);
            }
            if (events.length <= 0) {
              vm.cur = null;
            }
          }
          if (vm.events.length > 0) {
            vm.offset = vm.events.length;
            if (!old) {
              faviconService.add(vm.events.length - oldLength);
            }
          }
          if (old && events.length <= 0) {
            vm.noMoreEvent = true;
          }
          vm.busy = false;
        }
      });
  };

  /*
   * AA logic
   */

  vm.switchAA = function () {
    // Progress bar
    vm.cur.aa.lifePercent = 100 - vm.cur.aa.blessure;
    var rPvMin = (vm.cur.aa.pv_min ? vm.cur.aa.pv_min : vm.cur.aa.pv_max);
    vm.cur.aa.pvMinBlessure = Math.max(1, Math.floor(rPvMin * vm.cur.aa.lifePercent / 100));
    var rPvMax = (vm.cur.aa.pv_max ? vm.cur.aa.pv_max : vm.cur.aa.pv_mmin);
    if (vm.cur.aa.pv_max) {
      vm.cur.aa.pvMaxBlessure = Math.floor(rPvMax * vm.cur.aa.lifePercent / 100);
    } else {
      vm.cur.aa.pvMaxBlessure = Math.max(100, Math.floor(Math.floor(rPvMax * vm.cur.aa.lifePercent / 100) * 1.2));
    }
  };

  /*
   * IDC logic
   */

  vm.switchIDC = function () {};

  /*
   * PORTAL logic
   */

  vm.switchPORTAL = function () {};

  /*
   * PIEGE logic
   */

  vm.switchPIEGE = function () {};

  /*
   * BATTLE logic
   */
  vm.switchBATTLE = function () {
    vm.cur.attBlason = (vm.cur.sub.att_troll_id) ? vm.cur.sub.att_troll.blason_url : ((vm.cur.sub.att_mob_id) ? vm.cur.sub.att_mob.metamob.blason_url : vm.blasonError);
    vm.cur.defBlason = (vm.cur.sub.def_troll_id) ? vm.cur.sub.def_troll.blason_url : ((vm.cur.sub.def_mob_id) ? vm.cur.sub.def_mob.metamob.blason_url : vm.blasonError);
    vm.cur.isTouched = (vm.cur.battle.att > vm.cur.battle.esq);
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
    // VLC & ATT DIST
    if (vm.cur.cdm.vlc !== null) {
      vm.cur.cdm.vlc = vm.boolean2French(vm.cur.cdm.vlc);
    }
    if (vm.cur.cdm.att_dist !== null) {
      vm.cur.cdm.att_dist = vm.boolean2French(vm.cur.cdm.att_dist);
    }
    if (vm.cur.cdm.voleur !== null) {
      vm.cur.cdm.voleur = vm.boolean2French(vm.cur.cdm.voleur);
    }
    if (vm.cur.cdm.att_mag !== null) {
      vm.cur.cdm.att_mag = vm.boolean2French(vm.cur.cdm.att_mag);
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

  vm.isRelatedToCurDef = function (e) {
    // Cur Event
    var curDefID = (vm.cur.cdm.id) ? (vm.cur.cdm.mob_id) : null;
    curDefID = (vm.cur.aa.id) ? (vm.cur.aa.troll_cible_id) : curDefID;
    curDefID = (vm.cur.battle.id) ? ((vm.cur.battle.def_troll_id) ? vm.cur.battle.def_troll_id : vm.cur.battle.def_mob_id) : curDefID;
    // Event
    var eAttID = (e.cdm.id) ? (e.cdm.troll_id) : null;
    eAttID = (e.aa.id) ? (e.aa.troll_id) : eAttID;
    eAttID = (e.battle.id) ? ((e.battle.att_troll_id) ? e.battle.att_troll_id : e.battle.att_mob_id) : eAttID;
    var eDefID = (e.cdm.id) ? (e.cdm.mob_id) : null;
    eDefID = (e.aa.id) ? (e.aa.troll_cible_id) : eDefID;
    eDefID = (e.battle.id) ? ((e.battle.def_troll_id) ? e.battle.def_troll_id : e.battle.def_mob_id) : eDefID;
    // Is the current event target related to the event target tested ?
    return ((curDefID !== null) && ((curDefID === eDefID) || (curDefID === eAttID)));
  };

  vm.isRelatedToCurAtt = function (e) {
    // Cur Event
    var curAttID = (vm.cur.cdm.id) ? (vm.cur.cdm.troll_id) : null;
    curAttID = (vm.cur.aa.id) ? (vm.cur.aa.troll_id) : curAttID;
    curAttID = (vm.cur.battle.id) ? ((vm.cur.battle.att_troll_id) ? vm.cur.battle.att_troll_id : vm.cur.battle.att_mob_id) : curAttID;
    // Event
    var eAttID = (e.cdm.id) ? (e.cdm.troll_id) : null;
    eAttID = (e.aa.id) ? (e.aa.troll_id) : eAttID;
    eAttID = (e.battle.id) ? ((e.battle.att_troll_id) ? e.battle.att_troll_id : e.battle.att_mob_id) : eAttID;
    var eDefID = (e.cdm.id) ? (e.cdm.mob_id) : null;
    eDefID = (e.aa.id) ? (e.aa.troll_cible_id) : eDefID;
    eDefID = (e.battle.id) ? ((e.battle.def_troll_id) ? e.battle.def_troll_id : e.battle.def_mob_id) : eDefID;
    // Is the current event sender related to the event sender tested ?
    return ((curAttID !== null) && ((curAttID === eDefID) || (curAttID === eAttID)));
  };

  /*
   * Utils
   */

  vm.boolean2French = function (bool) {
    return (bool) ? 'Oui' : 'Non';
  };

  vm.displayDate = function (date) {
    var options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false};
    var dtf = new Intl.DateTimeFormat('fr-FR', options);
    var d = new Date(date);
    d.setTime(d.getTime() + (new Date(date).getTimezoneOffset() * 60 * 1000));
    return dtf.format(d);
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
