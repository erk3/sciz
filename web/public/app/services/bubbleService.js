angular
  .module('app')
  .factory('bubbleService', [
    '$window',
    '$document',
    bubbleService
  ]);

function bubbleService($window, $document) {
  var bubbleService = {
    checkOver: checkOver,
    closeBubbles: closeBubbles,
    getCurrentBubble: getCurrentBubble
  };

  /*
   * Credits for the following go to Canop
   * Adapted from : https://github.com/Canop/miaou/blob/master/src/main-js/miaou.fish.js
   */
  var current = null; // {targetRect, bubble} if a bubble is open

  function getCurrentBubble() {
    return current;
  }

  function overClientRect(e, rect) {
    return e.pageX >= rect.left && e.pageX <= rect.left + rect.width && e.pageY >= rect.top && e.pageY <= rect.top + rect.height;
  }

  function checkOver(e) {
    if (!current) {
      return bubbleService.closeBubbles();
    }
    if (overClientRect(e, current.targetRect)) {
      return;
    }
    if (overClientRect(e, current.bubble.getBoundingClientRect())) {
      return;
    }
    bubbleService.closeBubbles();
  }

  function closeBubbles() {
    if (!current) {
      return;
    }
    var hBubble = angular.element(document.querySelector('.bubble'));
    hBubble.remove();
    angular.element($window).off('mousemove', bubbleService.checkOver);
    current = null;
  }

  function visibleRect(element) {
    var rect = element.getBoundingClientRect();
    rect = {
      top: rect.top,
      right: rect.right,
      bottom: rect.bottom,
      left: rect.left
    };
    var container = element;
    for (;;) {
      container = container.parentElement;
      if (!container) {
        break;
      }
      if (container.scrollHeight > container.clientHeight) {
        var crect = container.getBoundingClientRect();
        if (crect.top > rect.top) {
          rect.top = crect.top;
        }
        if (crect.right < rect.right) {
          rect.right = crect.right;
        }
        if (crect.left > rect.left) {
          rect.left = crect.left;
        }
        if (crect.bottom < rect.bottom) {
          rect.bottom = crect.bottom;
        }
      }
      var position = $window.getComputedStyle(container).position;
      if (position === 'fixed' || position === 'absolute') {
        break;
      }
    }
    rect.width = rect.right - rect.left;
    rect.height = rect.bottom - rect.top;
    return rect;
  }

  function fixRect(r, ww, wh, margin) {
    if (r.width <= margin || r.height <= margin) {
      return r;
    }
    var fr = {
      left: Math.max(r.left, margin),
      top: Math.max(r.top, margin),
      right: Math.min(r.right, ww - margin),
      bottom: Math.min(r.bottom, wh - margin)
    };
    fr.width = fr.right - fr.left;
    fr.height = fr.bottom - fr.top;
    return fr;
  }

  angular.element.prototype.bubble = function (options) {
    bubbleService.closeBubbles();
    var side = null;
    var match = null;
    var css = null;
    var ww = $window.innerWidth;
    var wh = $window.innerHeight;
    var targetRect = fixRect(visibleRect(this[0]), ww, wh, 7);
    var hB = angular.element(angular.element($document[0].body).append('<div class="bubble">')[0].lastChild);
    var hC = angular.element(hB.append('<div class="bubble-content">')[0].lastChild);
    if (targetRect.width <= 1 || targetRect.height <= 1) {
      return;
    }
    if (options.classes) {
      hB.addClass(options.classes);
    }
    hB.append('<div class="bubble-arrow">');
    if (options.side) {
      if (/-/.test(options.side)) {
        side = options.side;
      } else if (options.side === 'horizontal') {
        side = (targetRect.left < ww / 2 ? 'right' : 'left') + '-' + (targetRect.top < wh / 2 ? 'bottom' : 'top');
      } else if (options.side === 'vertical') {
        side = (targetRect.top < wh / 2 ? 'bottom' : 'top') + '-' + (targetRect.left < ww / 2 ? 'right' : 'left');
      } else if ((match = options.side.match(/^(top|bottom)/))) {
        side = match[1] + '-' + (targetRect.left < ww / 2 ? 'right' : 'left');
      } else {
        side = ((options.side.match(/left|right/) || [])[0] || (targetRect.left < ww / 2 ? 'right' : 'left')) +
          '-' +
          ((options.side.match(/bottom|top/) || [])[0] || (targetRect.top < wh / 2 ? 'bottom' : 'top'));
      }
    } else {
      side = (targetRect.top < wh / 2 ? 'bottom' : 'top') +
        '-' +
        (targetRect.left < ww / 2 ? 'right' : 'left');
    }
    switch (side) {
      case 'bottom-left': // at the bottom right of the target, going towards left
        css = {
          right: (ww - targetRect.right + Math.min(targetRect.width - 25 | 0, 10)) + 'px',
          top: targetRect.bottom + 'px'
        };
        break;
      case 'bottom-right': // at the bottom left of the target, going towards right
        css = {
          left: (targetRect.left + Math.min(targetRect.width - 26 | 0, -2)) + 'px',
          top: targetRect.bottom + 'px'
        };
        break;
      case 'top-left': // at the bottom right, bubble extending towards left
        css = {
          right: (ww - targetRect.right + Math.min(targetRect.width - 25 | 0, 10)) + 'px',
          bottom: (wh - targetRect.top) + 'px'
        };
        break;
      case 'top-right': // at the bottom left, bubble extending towards right
        css = {
          left: (targetRect.left + Math.min(targetRect.width - 26 | 0, -2)) + 'px',
          bottom: (wh - targetRect.top) + 'px'
        };
        break;
      case 'left-bottom': // at the left of the target, going towards the bottom
        css = {
          right: (ww - targetRect.left) + 'px',
          top: (targetRect.top - 5) + 'px'
        };
        break;
      case 'left-top':
        css = {
          bottom: (wh - targetRect.bottom - 12) + 'px',
          right: (ww - targetRect.left) + 'px'
        };
        break;
      case 'right-bottom':
        css = {
          left: targetRect.right + 'px',
          top: (targetRect.top - 5) + 'px'
        };
        break;
      case 'right-top':
        css = {
          left: targetRect.right + 'px',
          bottom: (wh - targetRect.bottom - 12) + 'px'
        };
        break;
      default:
        break;
    }
    hB.css(css).addClass(side + '-bubble');
    if (options.text) {
      hC[0].innerText = options.text;
    } else if (options.html) {
      hC[0].innerHTML = options.html;
    }
    current = {
      targetRect: targetRect,
      bubble: hB[0],
      caller: this
    };
    if (options.blower) {
      var r = options.blower.call(this, hC, options);
      if (r === false) {
        hB.remove();
        return;
      }
    }
    angular.element($window).on('mousemove', bubbleService.checkOver);
    return this;
  };

  // registers options for bubbling:
  //   $(parentElement).bubbleOn("delegateSelector", options);
  //   $(bubblingElement).bubbleOn(options);
  // Options:
  //   side (optional): where the bubble should open
  //   blower: function called on the element with bubble content element as argument
  //    (may return false to prevent the bubble)
  angular.element.prototype.bubbleOn = function (selector, options) {
    if (!options) {
      options = selector;
      selector = null;
    }
    if (typeof options === 'string') {
      options = {text: options};
    } else if (typeof options === 'function') {
      options = {blower: options};
    }
    var args = [options, function () {
      angular.element(this).bubble(options);
    }];
    if (selector) {
      var items = document.querySelectorAll(selector);
      for (var i = 0; i < items.length; i++) {
        angular.element(items[i]).on('mouseenter', args[args.length - 1]);
      }
    } else {
      this.on('mouseenter', args[args.length - 1]);
    }
    return this;
  };

  return bubbleService;
}
