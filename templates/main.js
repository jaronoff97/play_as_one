var socket = io();
var gamemode = null,
    layout = null;

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
socket.on('initialize', function(data){

});
window.beforeunload = function(){
    socket.emit("disconnect", {});
}
main();