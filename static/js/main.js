var socket_name = 'http://' + document.domain + ':' + location.port;
console.log(socket_name);
var socket = null;
var gamemode = null,
    input_type = null;
var username = null

function main() {
    // create, initiate and append game canvas
    socket= io.connect(socket_name);
    username = window.prompt("Enter a username", "Username");
    init(); // initiate game objects
    //$(document).keydown(keyDown); //add keylisteners
    //$(document).keyup(keyUp);
    //draw();
}

function init() {
    socket.emit('add user', username);
    console.log('sent add user');
}
socket.on('initialize', function(data) {
    gamemode = data.mode ? 'chaos' : 'democracy';
    input_type = data.input_type;
    switch (input_type) {
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
    if (username != null) socket.emit("disconnect", username);
}
main();