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
function fillNES(){
    var a_button= $('<input class="A_button" type="button" value="new button"/>');
    var b_button= $('<input class="B_button" type="button" value="new button"/>');
    var d_pad= $('<input class="D_pad" type="button" value="new button"/>');
    $("#button_layout").append(a_button);
    $("#button_layout").append(b_button);
    $("#button_layout").append(d_pad);
}
function fillSNES(){
    fillNES();
    var x_button= $('<input class="X_button" type="button" value="new button"/>');
    var y_button= $('<input class="Y_button" type="button" value="new button"/>');
    $("#button_layout").append(x_button);
    $("#button_layout").append(y_button);

}
socket.on('initialize', function(data) {
    console.log(data);
    gamemode = data.mode ? 'chaos' : 'democracy';
    input_type = data.input_type;
    switch (input_type) {
        case ('NES'):
            {
                fillNES();
                break;
            }
        case ('SNES'):
            {
                fillSNES();
                break;
            }
        case ('Full Keyboard'):
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