export var commHandler = {
    socket: null,
    start: function() {
        commHandler.openSocket()
    },
    openSocket: function() {
        commHandler.socket = new WebSocket('ws://' + location.host + '/datasocket')
        commHandler.socket.onmessage = function(event) {
            try {
                commHandler.processMessage(JSON.parse(event.data))
            }
            catch (error) {
                console.log(error)
            }
        }
        commHandler.socket.onopen = commHandler.initialize
        commHandler.socket.onclose = commHandler.close
    },
    close: function() {
        console.log('CONNECTION CLOSED')
        return setTimeout(function() {
            commHandler.openSocket()
        }, 500)
    },
    sendMessage: function(message) {
        commHandler.socket.send(JSON.stringify(message))
    },
    initialize: function() {
        //blank for now
    },
    processMessage: function(message) {
        if (message.message=='gameList') {
            commHandler.context.games = message.games
            if (message.why) {
                commHandler.context.why = message.why
                commHandler.context.message = 'Here are your table\'s recommendations:'
            }
            commHandler.scope.$apply()
        }
        else if (message.message=='newTable') commHandler.context.moveToTable(message.tableName)
        else if (message.message=='tableInfo') {
            commHandler.context.players = message.players
            commHandler.context.you = message.you
            commHandler.scope.$apply()
        }
        else if (message.message=='tableReady') commHandler.context.tableReady()
    }
}
