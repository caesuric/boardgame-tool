import './index.scss'
var template = require('./index.html')

function tileController($scope, $element) {
    var ctrl = this
    ctrl.$onInit = function() {
        
    }
}

angular.module('widgets').component('boardgameTile', {
    template: template,
    controller: tileController,
    bindings: {
        model: '='
    }
})
