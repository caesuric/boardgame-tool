import {commHandler} from 'network'
import './index.scss'
var template = require('./index.html')

function explorerController($scope, $element, $state) {
    var ctrl = this
    ctrl.$onInit = function() {
        ctrl.mode = 'picker'
        ctrl.message = 'Which game sounds most appealing right now?'
        ctrl.gamesSelected = []
        commHandler.context = ctrl
        commHandler.scope = $scope
        if (!commHandler.socket) commHandler.start()
        setTimeout(function() {
            $($element[0].firstChild).addClass('fadein')
        }, 10)
        setTimeout(function() {
            var message = {
                message: 'queryGameSample'
            }
            commHandler.sendMessage(message)
        }, 400)
    }
    ctrl.selectGame = function(game) {
        if (ctrl.mode!='picker') return
        ctrl.gamesSelected.push(game)
        if (ctrl.gamesSelected.length<5) {
            var message = {
                message: 'queryGameSample'
            }
            commHandler.sendMessage(message)
        }
        else {
            ctrl.mode = 'results'
            ctrl.message = 'Waiting on other players to finish...'
            var message = {
                message: 'sendInBestGames',
                games: ctrl.getGameIds(ctrl.gamesSelected)
            }
            commHandler.sendMessage(message)
        }
    }
    ctrl.getGameIds = function(games) {
        var result = []
        for (let game of games) result.push(game.id)
        return result
    }
}

angular.module('widgets').component('boardgameExplorer', {
    template: template,
    controller: explorerController,
    bindings: {
        model: '='
    }
})
