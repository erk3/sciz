angular
  .module('app')
  .controller('TrollsCtrl', ['$scope', '$http', 'authService', trollsCtrl]);

function trollsCtrl($scope, $http, authService) {
  var vm = this;

  vm.user = authService.refreshLocalData();
  vm.getTrolls = getTrolls;
  vm.troll = {};
  vm.resetAlerts = resetAlerts;

  function resetAlerts() {
    vm.updateStatus = false;
    vm.updateStatusMessage = null;
  }

  vm.getTrolls(null);

  function getTrolls(troll) {
    $http({
      method: 'GET',
      url: '/api/trolls',
      params: {groupID: vm.user.currentAssoc.group_id}
    })
      .then(function (response) {
        if (response && response.data) {
          vm.slides = response.data;
          for (var i = 0; i < vm.slides.length; i++) {
            if (troll === null || vm.slides[i].id === troll.id) {
              vm.troll = vm.slides[i];
              vm.troll.clicked = false;
              vm.troll.sinceLastMHsp4Call = Math.floor((vm.adjustDate(new Date(), 0, false, false) - vm.adjustDate(vm.troll.last_mhsp4_call, 0, false, true)) / 3600000);
              break;
            }
          }
          vm.slides = vm.slides.map(function (item) {
            // Set the callback function used by the carousel slider
            item.callback = function () {
              vm.troll = item;
              vm.troll.clicked = false;
              vm.troll.sinceLastMHsp4Call = Math.floor((vm.adjustDate(new Date(), 0, false, false) - vm.adjustDate(vm.troll.last_mhsp4_call, 0, false, true)) / 3600000);
            };
            // Comptute the string reprs of the troll
            item = vm.trollToStr(item);
            return item;
          });
        }
      });
  }

  vm.updateTroll = function (troll) {
    troll.clicked = true;
    $http({
      method: 'POST',
      url: '/api/trolls/update',
      data: {groupID: vm.user.currentAssoc.group_id, trollID: troll.id}
    })
      .then(function (response) {
        if (response && response.data) {
          vm.getTrolls(troll);
          vm.updateStatus = true;
          vm.updateStatusMessage = response.data.message;
        }
      });
  };

  vm.displayHours = function (minutes) {
    if (minutes === null || minutes === undefined) {
      return null;
    }
    var sign = '';
    if (minutes < 0) {
      minutes *= -1;
      sign = '-';
    }
    return sign + Math.trunc(minutes / 60) + ' h ' + (minutes % 60) + ' m ';
  };

  vm.adjustDate = function (date, minutesToAdd, reverted, adjustTimeZone) {
    var d = new Date();
    if (date !== null && date !== undefined) {
      d = new Date(date);
    }

    var t = 0;
    if (adjustTimeZone !== null && adjustTimeZone !== undefined && adjustTimeZone !== false) {
      t = new Date(date).getTimezoneOffset() * 60 * 1000;
    }

    var m = 0;
    if (minutesToAdd !== null && minutesToAdd !== undefined) {
      m = minutesToAdd * 60 * 1000;
    }

    var r = 1;
    if (reverted !== null && reverted !== undefined && reverted !== false) {
      r = -1;
    }

    d.setTime(d.getTime() + m + (t * r));

    return d;
  };

  vm.displayDate = function (date, minutesToAdd, reverted, adjustTimeZone) {
    var options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false};
    var dtf = new Intl.DateTimeFormat('fr-FR', options);
    var d = vm.adjustDate(date, minutesToAdd, reverted, adjustTimeZone);
    return dtf.format(d);
  };

  vm.trollToStr = function (troll) {
    var plus = function (n, positivePrefix, negativePrefix, nullValue, suffix) {
      if (Number.isInteger(n)) {
        return ((n === null || n === undefined) ? nullValue : ((n > 0 ? positivePrefix : negativePrefix) + n + suffix));
      }
      return ((n === null || n === undefined) ? nullValue : (positivePrefix + n + suffix));
    };

    troll.tPos = (troll.pos_x !== null) ? 'X = ' + troll.pos_x + ' | Y = ' + troll.pos_y + ' | N = ' + troll.pos_n : '?';
    troll.tConcentration = plus(troll.base_concentration, '', '', '?', ' %');
    troll.tVie = plus(troll.pv, '', '', '?', '');
    troll.tLifePercent = plus(troll.pv / troll.base_bonus_pv_max * 100, '', '', 0, '');
    troll.tFatigueStr = '?';
    if (troll.fatigue !== null) {
      troll.tFatigueStr = troll.fatigue >= 0 ? 'Parfaitement reposé (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 1 && troll.fatigue < 3 ? 'En pleine forme (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 3 && troll.fatigue < 5 ? 'Tonique (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 5 && troll.fatigue < 7 ? 'Juste Bien (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 7 && troll.fatigue < 11 ? 'Plus très frais (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 11 && troll.fatigue < 16 ? 'Mou du genou (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 16 && troll.fatigue < 21 ? 'Fatigué ' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 21 && troll.fatigue < 31 ? 'Crevé (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 31 && troll.fatigue < 41 ? 'Lessivé (' + troll.fatigue + ')' : troll.tFatigueStr;
      troll.tFatigueStr = troll.fatigue >= 41 && troll.fatigue < 128 ? 'Complètement épuisé (' + troll.fatigue + ')' : troll.tFatigueStr;
    }

    troll.tPA = plus(troll.pa, '', '', '?', ' PA / 6');
    troll.tDLA = plus(vm.displayDate(troll.dla, 0, false, true), '', '', '?', '');
    troll.tLastSP4Call = plus(vm.displayDate(troll.last_mhsp4_call, 0, false, true), '', '', '?', '');
    troll.bTour = plus(vm.displayHours(troll.base_tour), '', '', '?', '');
    var malusTourBlessure = Math.trunc((250 * (troll.base_bonus_pv_max - troll.pv)) / troll.base_bonus_pv_max);
    troll.tMalusTourBlessure = plus(vm.displayHours(malusTourBlessure), '', '', '?', '');
    var poidsTour = troll.base_poids + troll.malus_poids_phy + troll.malus_poids_mag;
    troll.tPoidsTour = plus(vm.displayHours(poidsTour), '', '', '?', '');
    var bmmTour = troll.bonus_tour_phy + troll.bonus_tour_mag;
    troll.tBMMTour = plus(vm.displayHours(bmmTour), '', '', '?', '');
    var nextTour = Math.max(troll.base_tour, troll.base_tour + malusTourBlessure + poidsTour + bmmTour);
    troll.bNextTour = plus(vm.displayHours(nextTour), '', '', '?', '');
    troll.tNextDLA = plus(vm.displayDate(troll.dla, nextTour, false, true), '', '', '?', '');

    troll.bAtt = plus(troll.base_att, '', '', '?', 'D6');
    troll.bAttPhy = plus(troll.bonus_att_phy, '+', '', '?', '');
    troll.bAttMag = plus(troll.bonus_att_mag, '+', '', '?', '');
    troll.bEsq = plus(troll.base_esq, '', '', '?', 'D6');
    troll.bEsqPhy = plus(troll.bonus_esq_phy, '+', '', '?', '');
    troll.bEsqMag = plus(troll.bonus_esq_mag, '+', '', '?', '');
    troll.bDeg = plus(troll.base_deg, '', '', '?', 'D3');
    troll.bDegPhy = plus(troll.bonus_deg_phy, '+', '', '?', '');
    troll.bDegMag = plus(troll.bonus_deg_mag, '+', '', '?', '');
    troll.bPVMax = plus(troll.base_pv_max, '', '', '?', '');
    troll.bPVMaxPhy = plus(troll.bonus_pv_max_phy, '+', '', '?', '');
    troll.bPVMaxMag = plus(troll.bonus_pv_max_mag, '+', '', '?', '');
    troll.bReg = plus(troll.base_reg, '', '', '?', 'D3');
    troll.bRegPhy = plus(troll.bonus_reg_phy, '+', '', '?', '');
    troll.bRegMag = plus(troll.bonus_reg_mag, '+', '', '?', '');
    troll.bArm = plus(troll.base_arm_phy, '', '', '?', 'D3');
    troll.bArmPhy = plus(troll.bonus_arm_phy, '+', '', '?', '');
    troll.bArmMag = plus(troll.bonus_arm_mag, '+', '', '?', '');
    troll.bVue = plus(troll.base_vue, '', '', '?', '');
    troll.bVuePhy = plus(troll.bonus_vue_phy, '+', '', '?', '');
    troll.bVueMag = plus(troll.bonus_vue_mag, '+', '', '?', '');
    troll.bMM = plus(troll.base_mm, '', '', '?', '');
    troll.bMMPhy = plus(troll.bonus_mm_phy, '+', '', '?', '');
    troll.bMMMag = plus(troll.bonus_mm_mag, '+', '', '?', '');
    troll.bRM = plus(troll.base_rm, '', '', '?', '');
    troll.bRMPhy = plus(troll.bonus_rm_phy, '+', '', '?', '');
    troll.bRMMag = plus(troll.bonus_rm_mag, '+', '', '?', '');

    troll.tPVMax = plus(troll.base_pv_max + troll.bonus_pv_max_phy + troll.bonus_pv_max_mag, '', '', '?', ' PV');
    troll.tVue = plus(troll.base_vue + troll.bonus_vue_phy + troll.bonus_vue_mag, '', '', '?', ' cases');
    troll.tMM = plus(troll.base_mm + troll.bonus_mm_phy + troll.bonus_mm_mag, '+', '', '?', ' points');
    troll.tRM = plus(troll.base_rm + troll.bonus_rm_phy + troll.bonus_rm_mag, '+', '', '?', ' points');

    troll.tCorp = plus(Math.floor(troll.base_pv_max / 10) + troll.bonus_arm_phy, '', '', '?', ' points');
    troll.tAgi = plus(troll.base_esq + troll.base_reg, '', '', '?', ' points');
    troll.tStab = plus(Math.floor((troll.base_esq + troll.base_reg) * 2 / 3), '', '', '?', 'D6');
    troll.tStab += ' ' + plus(troll.bonus_esq_phy, '+', '', '', '');

    return troll;
  };
}
