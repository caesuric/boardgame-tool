import './index.scss'
var template = require('./index.html')

function tileNonlinkController($scope, $element) {
    var ctrl = this
    ctrl.$onInit = function() {
        
    }
}

angular.module('widgets').component('boardgameTileNonlink', {
    template: template,
    controller: tileNonlinkController,
    bindings: {
        model: '='
    }
})
