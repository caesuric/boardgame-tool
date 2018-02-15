import 'bootstrap/dist/css/bootstrap.css'
import angular from 'angular'
import ngAnimate from 'angular-animate'
import 'angular-ui-router'
import 'angular-ui-bootstrap'

import 'widgets'
import 'views'
import './index.scss'

var app = angular.module('boardgameTool', ['ngAnimate', 'ui.bootstrap', 'ui.router', 'widgets', 'views'])
app.config(function($stateProvider, $urlRouterProvider) {
    $stateProvider.state({
        name: 'picker',
        url: '/picker',
        template: '<boardgame-picker></boardgame-picker>'
    })
    $stateProvider.state({
        name: 'explorer',
        url: '/explorer/{tableName:string}',
        template: '<boardgame-explorer></boardgame-explorer>'
    })
    $stateProvider.state({
        name: 'explorerSetup',
        url: '/explorerSetup',
        template: '<boardgame-explorer-setup></boardgame-explorer-setup>'
    })
    $urlRouterProvider.otherwise('/picker')
})
.controller('mainCtrl', function($scope) {
    var ctrl=this
    ctrl.$onInit = function() {

    }
})
