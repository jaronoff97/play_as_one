var socket_name = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(socket_name);
var gamemode = null,
    input_type = null;
var username = null

function main() {
    // create, initiate and append game canvas
    username = window.prompt("Enter a username", "Username");
    init(); // initiate game objects
    //$(document).keydown(keyDown); //add keylisteners
    //$(document).keyup(keyUp);
    //draw();
}

function init() {
    socket.emit('add user', username);
}
socket.on('initialize', function(data) {
    console.log(data);
    gamemode = data.mode ? 'chaos' : 'democracy';
    input_type = data.input_type;
    switch (input_type) {
        case ('NES'):
            {
                break;
            }
        case ('wasd'):
            {
                break;
            }
            default: {
                break;
            }
    }
});
window.beforeunload = function() {
    if (username != null) socket.emit("disconnect", username);
}
main();