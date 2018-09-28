angular
  .module('app')
  .controller('ViewCtrl', ['$window', '$document', '$scope', '$http', 'authService', 'bubbleService', 'utilService', viewCtrl]);

function viewCtrl($window, $document, $scope, $http, authService, bubbleService, utilService) {
  /*
   * CSS Getter
   */
  // Inside closure so that the inner functions don't need regeneration on every call.
  const getCssClasses = (function () {
    function normalize(str) {
      if (!str) {
        return '';
      }
      str = String(str).replace(/\s*([>~+])\s*/g, ' $1 '); // Normalize symbol spacing
      return str.replace(/(\s+)/g, ' ').trim(); // Normalize whitespace
    }
    function split(str, on) { // Split, Trim, and remove empty elements
      return str.split(on).map(function (x) { return x.trim(); }).filter(function (x) { return x; });
    }
    function containsAny(selText, ors) {
      return selText ? ors.some(function (x) { return selText.indexOf(x) >= 0; }) : false;
    }
    return function (selector) {
      const logicalORs = split(normalize(selector), ',');
      const sheets = Array.from(window.document.styleSheets);
      const ruleArrays = sheets.map(function (x) { return Array.from(x.rules || x.cssRules || []); });
      const allRules = ruleArrays.reduce(function (all, x) { return all.concat(x); }, []);
      return allRules.filter(function (x) { return containsAny(normalize(x.selectorText), logicalORs); });
    };
  })();

  /*
   * Alternative do angular.element.data
   */
  (function () {
    var datCache = new WeakMap();
    angular.element.prototype.dat = function (key, val) {
      if (this.length === 0) {
        return arguments.length === 1 ? undefined : this;
      }
      if (this.length > 1) {
        // console.log('Warning: angular.element.prototype.dat called on a collection with several elements', this);
      }
      var oc = datCache.get(this[0]);
      if (!oc) {
        oc = new Map();
        datCache.set(this[0], oc);
      }
      if (arguments.length === 1) {
        return oc.get(key);
      }
      oc.set(key, val);
      return this;
    };
  })();

  /*
   * Actual controller
   */
  var vm = this;

  vm.user = authService.refreshLocalData();
  vm.loadView = loadView;
  vm.makeCells = makeCells;
  vm.displayView = displayView;
  vm.makeGridDraggable = makeGridDraggable;
  vm.applyZoom = applyZoom;
  vm.centerView = centerView;
  vm.applyFilters = applyFilters;

  vm.minProf = -100;
  vm.maxProf = 0;
  vm.date = 2;
  vm.filter = "";
  vm.origX = null;
  vm.origY = null;
  vm.origN = null;
  vm.portee = null;
  vm.trolls = [];

  vm.cellWidth = 0;
  vm.zoom = 5;
  vm.currentView = null;
  vm.hoverGrid = false;
  vm.debouncing = false;

  const MH_BASE = 'https://games.mountyhall.com/mountyhall/View/';
  const cellSizes = getCssClasses('#mountyhall-view-grid.zoom1 .line, #mountyhall-view-grid.zoom2 .line, #mountyhall-view-grid.zoom3 .line, #mountyhall-view-grid.zoom4 .line, #mountyhall-view-grid.zoom5 .line, #mountyhall-view-grid.zoom6 .line')
    .map(function (v) {
      return parseInt(v.style.height, 10);
    });

  vm.loadView();

  /*
   * View loader
   */
  function loadView() {
    $http({
      method: 'GET',
      url: '/api/view',
      params: {
        groupID: vm.user.currentAssoc.group_id,
        origX: vm.origX,
        origY: vm.origY,
        origN: vm.origN,
        portee: vm.portee
      }
    })
    .then(function (response) {
      if (response && response.data) {
        vm.currentView = angular.fromJson(response.data);
        vm.origX = vm.currentView.origine.x;
        vm.origY = vm.currentView.origine.y;
        vm.origN = vm.currentView.origine.n;
        vm.portee = vm.currentView.origine.portee;
        vm.trolls = vm.currentView.gTrolls;
        vm.makeCells(vm.currentView);
        vm.displayView(vm.currentView);
        vm.makeGridDraggable();
        vm.applyFilters();
        setTimeout(vm.centerView, 1);
      }
    });
  }

  /*
   * Credits for the following go to Canop
   * Adapted from : https://github.com/Canop/miaou.mountyhall/blob/master/plugin/client-scripts/partage-vue.js
   */
  window.addEventListener('wheel', function (e) {
    if (!vm.hoverGrid) {
      return;
    }
    e.preventDefault();
    if (vm.debouncing) {
      return;
    }
    vm.debouncing = true;
    setTimeout(function () {
      vm.debouncing = false;
    }, 200);
    var oldZoom = vm.zoom;
    if (e.deltaY > 0) {
      vm.zoom--;
    } else if (e.deltaY < 0) {
      vm.zoom++;
    } else {
      return;
    }
    vm.zoom = Math.max(0, Math.min(cellSizes.length - 1, vm.zoom));
    if (vm.zoom !== oldZoom) {
      vm.applyZoom(e);
    }
    return false;
  });

  function makeCells(trollView) {
    var origine = trollView.origine;
    var portee = Math.max(origine.portee, 0);
    var xmin = origine.x - portee;
    var ymin = origine.y - portee;
    var size = trollView.size = (2 * portee) + 1;
    var cells = trollView.cells = [];

    for (var i = 0; i < size; i++) {
      var x = xmin + i;
      cells[i] = [];
      for (var j = 0; j < size; j++) {
        var y = ymin + j;
        cells[i][j] = {
          x: x,
          y: y
        };
      }
    }

    cells[origine.x - xmin][origine.y - ymin].origine = true;

    ['mobs', 'trolls', 'lieux'].forEach(function (key) {
      if (!trollView[key]) {
        return;
      }
      trollView[key].forEach(function (obj) {
        if (!obj.nom) {
          // console.log(key, 'sans nom :', obj);
          // return;
        }
        var col = cells[obj.pos_x - xmin];
        if (!col) {
          // console.log('hors grille :', key, obj);
          return;
        }
        var cell = col[obj.pos_y - ymin];
        if (!cell) {
          // console.log('hors grille :', key, obj);
          return;
        }
        if (!cell[key]) {
          cell[key] = [];
        }
        cell[key].push(obj);
      });
    });
  }

  function displayView(trollView) {
    var cells = trollView.cells;
    var size = trollView.size;
    var hView = angular.element(document.querySelector('#mountyhall-view'));
    var hGrid = angular.element(document.querySelector('#mountyhall-view-grid'));

    hGrid.empty();
    vm.applyZoom();

    for (var j = size - 1; j >= 0; j--) {
      var hLine = angular.element(hGrid.append('<div class="line">')[0].lastChild);
      for (var i = 0; i < size; i++) {
        var cell = cells[i][j];
        var k = 0;
        var obj = null;
        var hObj = null;
        var hCell = angular.element(hLine.append('<div class="mh-cell">')[0].lastChild);
        hCell.dat('cell', cell);
        if (cell.origine) {
          hCell.addClass('origine');
        }
        angular.element(hCell.append('<div class="position">')[0].lastChild).text(cell.x + ' ' + cell.y);
        if (cell.lieux) {
          hCell.append('<div class="nb-lieux">');
          cell.lieux.sort(function (a, b) { return b.pos_n - a.pos_n; });
          var bTrou = false;
          for (k = 0; k < cell.lieux.length; k++) {
            obj = cell.lieux[k];
            if (obj.nom === 'Trou de Météorite') {
              if (!bTrou) {
                hObj = angular.element(hCell.append('<div class="lieu">')[0].lastChild);
                hObj.text('Trou').addClass('trou');
                bTrou = true;
              }
            } else {
              hObj = angular.element(hCell.append('<div class="lieu">')[0].lastChild);
              hObj.text(obj.pos_n + ': ' + obj.nom);
            }
            hObj.dat('lieu', obj);
          }
        }
        if (cell.trolls) {
          angular.element(hCell.append('<div class=nb-trolls></div>')[0].lastChild).text(cell.trolls.length);
          cell.trolls.sort(function (a, b) { return b.pos_n - a.pos_n; });
          for (k = 0; k < cell.trolls.length; k++) {
            obj = cell.trolls[k];
            hObj = angular.element(hCell.append('<a class="troll"></a>')[0].lastChild)
              .attr('target', '_blank')
              .attr('href', MH_BASE + '/PJView.php?ai_IDPJ=' + obj.id)
              .text(obj.pos_n + ': ' + (obj.nom || obj.id));
            hObj.dat('troll', obj);
          }
        }
        if (cell.mobs) {
          cell.mobs.sort(function (a, b) { return b.pos_n - a.pos_n; });
          var n = 0;
          var hn = angular.element(hCell.append('<div class="nb-mobs"></div>')[0].lastChild);
          for (k = 0; k < cell.mobs.length; k++) {
            obj = cell.mobs[k];
            hObj = angular.element(hCell.append('<a class="mob"></a>')[0].lastChild)
              .attr('target', '_blank')
              .attr('href', MH_BASE + '/MonsterView.php?ai_IDPJ=' + obj.id);
            hObj.text(obj.pos_n + ': ' + obj.nom + ' [' + obj.age + ']');
            if (/^Gowap Appr/.test(obj.nom)) {
              hObj.addClass('gowap');
            } else {
              n++;
            }
            hObj.dat('mob', obj);
          }
          if (n) {
            hn.text(n);
          } else {
            hn.remove();
          }
        }
      }
    }

    hGrid.bind('mouseenter', function () {
      vm.hoverGrid = true;
    });
    hGrid.bind('mouseleave', function () {
      vm.hoverGrid = false;
    });

    hGrid.bubbleOn('.mh-cell', {
      side: 'horizontal',
      blower: cellBlower
    });

    hGrid.bubbleOn('.mob', {
      side: 'horizontal',
      classes: 'mob',
      blower: gonfleurMob
    });

    hGrid.bubbleOn('.troll', {
      side: 'horizontal',
      classes: 'troll',
      blower: gonfleurTroll
    });
  }

  function applyZoom(e) {
    var hView = angular.element(document.querySelector('#mountyhall-view'));
    var hGrid = angular.element(document.querySelector('#mountyhall-view-grid'));
    var oldCellWidth = vm.cellWidth;
    var size = vm.currentView.size;
    var adjustScroll = e && oldCellWidth;
    var lines = null;
    var heights1 = null;
    var marg = null;
    var VG1x = null;
    var VG1y = null;
    if (adjustScroll) {
      // on va avoir besoin des hauteurs de lignes avant application du style
      lines = hGrid[0].querySelectorAll('.line');
      heights1 = [].map.call(lines, function (line) {
        return line.offsetHeight;
      });
      marg = parseInt(getCssClasses('#mountyhall-view-grid')[0].style.marginLeft, 10);
      // on doit récupérer le scroll avant ajustement parce qu'il est parfois
      //  modifié par le changement de style
      VG1x = marg - hView[0].scrollLeft;
      VG1y = marg - hView[0].scrollTop;
    }

    // application du style
    hGrid[0].className = 'zoom' + vm.zoom;
    vm.cellWidth = cellSizes[vm.zoom];
    hGrid.css('width', (vm.cellWidth * size) + 'px');

    if (!adjustScroll) {
      return;
    }

    // l'objectif des opérations qui suivent est d'assurer que la même cellule
    // soit sous la souris avant et après zoom
    // Glossaire:
    //  S : coin haut gauche de la fenêtre
    //  V : coin haut gauche de la view (scrollable, contenant la grille)
    //  G : coin haut gauche de la grille
    //  G1: G avant zoom
    //  G2: G après zoom
    //  M : position de la souris
    //  (x,y) : position de la souris dans le référentiel MH avec l'origine le coin
    //          gauche de la grille
    //  marg : marge autour de la grille
    var SVleft = hView[0].offsetLeft;
    var SVtop = hView[0].offsetTop;

    // En x c'est relativement simple car les cellules ont toutes la même largeur
    var r = vm.cellWidth / oldCellWidth;
    var SMx = e.clientX;
    var VG2x = SMx - SVleft - (r * (SMx - SVleft - VG1x));

    // En y il faut composer avec des cellules qui ont des hauteurs variables
    //  => G1M connu (G1M=SM-VG1-SV)
    var SMy = e.clientY;
    var G1My = SMy - VG1y - SVtop;
    // BUG : au dézoom le G1My est parfois faux

    // => on en déduit y par accumulation des hauteurs de cellules jusqu'à atteindre G1My
    //    (on peut estimer un float en prenant le reste et en divisant par la hauteur de la
    //    cellule suivante)
    var y = 0;
    for (var gm = 0; gm !== null; gm += heights1[y++]) {
      if (y >= heights1.length || gm >= G1My) {
        break;
      }
      if (gm + heights1[y] > G1My) {
        y += (G1My - gm) / heights1[y];
        break;
      }
    }

    // => on fait la démarche inverse pour partir de y et arriver à G2M (somme des
    //    y premières hauteurs de ligne)
    var G2My = 0;
    var ry = Math.floor(y);
    for (var iy = 0; iy < ry; iy++) {
      G2My += lines[iy].offsetHeight;
    }
    if (ry < lines.length - 1) {
      G2My += (y - ry) * lines[ry + 1].offsetHeight;
    }

    // => G2M nous donne VG2 via VG2=-G2M+SM-SV)
    var VG2y = SMy - SVtop - G2My;

    // => et il ne reste plus qu'à tenir compte de la marge
    hView[0].scrollLeft = marg - VG2x;
    hView[0].scrollTop = marg - VG2y;
  }

  function makeGridDraggable() {
    var hView = angular.element(document.querySelector('#mountyhall-view'));
    var hGrid = angular.element(document.querySelector('#mountyhall-view-grid'));
    var lastLeft = 0;
    var lastTop = 0;

    function onDrag(e) {
      hView[0].scrollLeft = hView[0].scrollLeft - e.clientX + lastLeft;
      hView[0].scrollTop = hView[0].scrollTop - e.clientY + lastTop;
      lastLeft = e.clientX;
      lastTop = e.clientY;
    }

    hGrid.bind('mousedown', function (e) {
      lastLeft = e.clientX;
      lastTop = e.clientY;
      hView.on('mousemove', onDrag);
    });

    $document.on('mouseup wheel', function () {
      hView.off('mousemove', onDrag);
    });
  }

  function centerView() {
    var hView = angular.element(document.querySelector('#mountyhall-view'));
    var hOrigin = angular.element(document.querySelector('.origine'));
    var originOffsetLeft = hOrigin[0].offsetLeft;
    var originOffsetTop = hOrigin[0].offsetTop;
    hView[0].scrollLeft = originOffsetLeft + ((hOrigin[0].clientWidth - window.innerWidth) / 2);
    hView[0].scrollTop = originOffsetTop + ((hOrigin[0].clientHeight - window.innerHeight) / 2);
  }

  function cellBlower(c) {
    if (vm.zoom > 3) {
      return false;
    }
    c.append(angular.element(this).clone());
  }

  function gonfleurMob(c) {
    if (vm.zoom < 3) {
      return false;
    }
    var cCaller = bubbleService.getCurrentBubble().caller;
    var mob = cCaller.dat('mob');
    c.html('<p>Identifiant : ' + mob.id + '<br>Vu la dernière fois : ' + utilService.displayDate(mob.last_seen, 0, false, true) + '</p>');
  }

  function gonfleurTroll(c) {
    if (vm.zoom < 3) {
      return false;
    }
    var cCaller = bubbleService.getCurrentBubble().caller;
    var troll = cCaller.dat('troll');
    c.html('<p>Identifiant : ' + troll.id + '<br>Vu la dernière fois : ' + utilService.displayDate(troll.last_seen, 0, false, true) + '</p>');
  }

  function applyFilters() {
    var min = vm.minProf;
    var max = vm.maxProf;
    var date = vm.date;
    var name = vm.filter;
    var rname = (name === '' || name === undefined || name === null) ? null : new RegExp(name.trim(), 'i');
    if (min > 0) {
      min *= -1;
    }
    if (max > 0) {
      max *= -1;
    }
    if (min > max) {
      var temp = max;
      max = min;
      min = temp;
    }
    document.querySelectorAll('#mountyhall-view-grid .mh-cell').forEach(function (e) {
      var cell = angular.element(e).dat('cell');
      ['lieux', 'mobs', 'trolls'].forEach(function (key) {
        var arr = cell[key];
        if (arr) {
          var elems = e.querySelectorAll('.' + key.slice(0, -1));
          var n = 0;
          var changed = false;
          for (var i = 0; i < arr.length; i++) {
            var o = arr[i];
            var wasFiltered = (i < elems.length) && elems[i].classList.contains('filtered');
            var filtered = (min && o.pos_n < min) ||
              (date && utilService.dateDiffInDays(new Date(o.last_seen), new Date()) > date) ||
              (max && o.pos_n > max) ||
              (rname !== null && (!rname.test(o.nom + ' ' + o.id)));
            if ((i < elems.length) && (filtered !== wasFiltered)) {
              changed = true;
              elems[i].classList.toggle('filtered', filtered);
            }
            if (!filtered) {
              n++;
            }
          }
          if (changed) {
            var nbElem = angular.element(e.querySelector('.nb-' + key));
            if (nbElem && nbElem.length > 0) {
              nbElem.text(n);
              if ((n === 0 && !nbElem[0].classList.contains('filtered')) || (n !== 0 && nbElem[0].classList.contains('filtered'))) {
                nbElem[0].classList.toggle('filtered');
              }
            }
          }
        }
      });
    });
  }
}
