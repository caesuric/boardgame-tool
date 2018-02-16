import {commHandler} from 'network'
import './index.scss'
var template = require('./index.html')

function explorerSetupController($scope, $element, $state) {
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
            message: 'createExplorerTable',
            name: ctrl.name,
            minutes: ctrl.minutes
        }
        commHandler.sendMessage(message)
    }
    ctrl.moveToTable = function(tableName) {
        $($element[0].firstChild).removeClass('fadein')
        $($element[0].firstChild).addClass('fadeout')
        setTimeout(function() {
            $state.go('explorerWaiting', {tableName: tableName})
        }, 500)
    }
}

angular.module('widgets').component('boardgameExplorerSetup', {
    template: template,
    controller: explorerSetupController,
    bindings: {
        model: '='
    }
})
