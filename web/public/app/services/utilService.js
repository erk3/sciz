angular
  .module('app')
  .factory('utilService', [
    utilService
  ]);

function utilService() {
  var utilService = {
    adjustDate: adjustDate,
    displayDate: displayDate,
    dateDiffInDays: dateDiffInDays
  };

  function adjustDate(date, minutesToAdd, reverted, adjustTimeZone) {
    var d = new Date();
    if (date !== null && date !== undefined) {
      d = new Date(date);
    } else {
      return null;
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
  }

  function displayDate(date, minutesToAdd, reverted, adjustTimeZone) {
    var options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false};
    var dtf = new Intl.DateTimeFormat('fr-FR', options);
    var d = adjustDate(date, minutesToAdd, reverted, adjustTimeZone);
    if (d === null) {
      return null;
    }
    return dtf.format(d);
  }

  function dateDiffInDays(a, b) {
    const _MS_PER_DAY = 1000 * 60 * 60 * 24;
    const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());
    return Math.floor((utc2 - utc1) / _MS_PER_DAY);
  }

  return utilService;
}
