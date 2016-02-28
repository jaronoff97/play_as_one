var socket = io();
var gamemode = null,
    input_type = null;

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
    gamemode = data.mode ? 'chaos' : 'democracy';
    input_type = data.input_type;
    switch (input_type): {
        case ('gameboy'):
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
    socket.emit("disconnect", username);
}
main();