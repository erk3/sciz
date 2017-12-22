angular
  .module('app')
  .config(textAngularConfig);

/** @ngInject */
function textAngularConfig($provide) {
  $provide.decorator('taOptions', ['taRegisterTool', '$delegate',
    function (taRegisterTool, taOptions) { // $delegate is the taOptions we are decorating
      taOptions.toolbar = [
                            ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'quote'],
                            ['bold', 'italics', 'underline', 'strikeThrough', 'ul', 'ol', 'redo', 'undo'],
                            ['justifyLeft', 'justifyCenter', 'justifyRight'],
                            ['html', 'insertImage', 'insertLink']
      ];
      return taOptions;
    }]);
  $provide.decorator('taTools', ['$delegate', function (taTools) {
    taTools.h1.tooltiptext = 'Titre 1';
    taTools.h2.tooltiptext = 'Titre 2';
    taTools.h3.tooltiptext = 'Titre 3';
    taTools.h4.tooltiptext = 'Titre 4';
    taTools.h5.tooltiptext = 'Titre 5';
    taTools.h6.tooltiptext = 'Titre 6';
    taTools.p.tooltiptext = 'Paragraphe';
    taTools.pre.tooltiptext = 'Texte préformatté';
    taTools.quote.tooltiptext = 'Citation';
    taTools.bold.tooltiptext = 'Gras';
    taTools.italics.tooltiptext = 'Italique';
    taTools.underline.tooltiptext = 'Souligné';
    taTools.strikeThrough.tooltiptext = 'Barré';
    taTools.ul.tooltiptext = 'Liste non ordonnée';
    taTools.ol.tooltiptext = 'Liste ordonnée';
    taTools.redo.tooltiptext = 'Refaire';
    taTools.undo.tooltiptext = 'Défaire';
    taTools.justifyLeft.tooltiptext = 'Aligner à gauche';
    taTools.justifyCenter.tooltiptext = 'Centrer';
    taTools.justifyRight.tooltiptext = 'Aligner à droite';
    taTools.html.tooltiptext = 'HTML / Texte enrichi';
    taTools.insertImage.tooltiptext = 'Insérer une image';
    taTools.insertLink.tooltiptext = 'Insérer / éditer un lien';
    return taTools;
  }]);
}
