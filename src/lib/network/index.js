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
            commHandler.scope.$apply()
        }
    }
}
