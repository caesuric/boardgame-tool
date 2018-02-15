import {commHandler} from 'network'
import './index.scss'
var template = require('./index.html')

function explorerWaitingController($scope, $element, $state, $stateParams) {
    var ctrl = this
    ctrl.$onInit = function() {
        ctrl.url = window.location.href
        commHandler.context = ctrl
        commHandler.scope = $scope
        if (!commHandler.socket) commHandler.start()
        setTimeout(function() {
            $($element[0].firstChild).addClass('fadein')
        }, 10)
        setTimeout(function() {
            var message = {
                message: 'getTableInfo',
                table: $stateParams.tableName
            }
            commHandler.sendMessage(message)
        }, 500)
    }
    ctrl.keepUrlCorrect = function() {
        ctrl.url = window.location.href
    }
    ctrl.joinTable = function(name) {
        var message = {
            message: 'joinTable',
            table: $stateParams.tableName,
            name: name
        }
        commHandler.sendMessage(message)
    }
    ctrl.changedReadyState = function(readyState) {
        var message = {
            message: 'readyState',
            readyState: readyState
        }
        commHandler.sendMessage(message)
    }
    ctrl.tableReady = function() {
        $($element[0].firstChild).removeClass('fadein')
        $($element[0].firstChild).addClass('fadeout')
        setTimeout(function() {
            $state.go('explorer', {tableName: $stateParams.tableName})
        }, 500)
    }
}

angular.module('widgets').component('boardgameExplorerWaiting', {
    template: template,
    controller: explorerWaitingController,
    bindings: {
        model: '='
    }
})
