import {commHandler} from 'network'
import './index.scss'
var template = require('./index.html')

function pickerController($scope, $element, $state, $stateParams) {
    var ctrl = this
    ctrl.$onInit = function() {
        commHandler.context = ctrl
        commHandler.scope = $scope
        if (!commHandler.socket) commHandler.start()
        setTimeout(function() {
            $($element[0].firstChild).addClass('fadein')
        }, 10)
    }
    ctrl.submit = function() {
        var message = {
            message: 'queryGames',
            players: ctrl.numberOfPlayers,
            minutes: ctrl.minutesAvailable
        }
        commHandler.sendMessage(message)
    }
}

angular.module('widgets').component('boardgamePicker', {
    template: template,
    controller: pickerController,
    bindings: {
        model: '='
    }
})
