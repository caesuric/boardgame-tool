import './index.scss'
var template = require('./index.html')

function navbarController($scope, $element, $state) {
    var ctrl = this
    ctrl.$onInit = function() {

    }
    ctrl.isSelected = function(text) {
        return ($state.$current.name==text)
    }
}

angular.module('widgets').component('navbar', {
    template: template,
    controller: navbarController,
    bindings: {
        model: '='
    }
})
