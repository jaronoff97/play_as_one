var socket_name = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(socket_name);
var gamemode = null,
    input_type = null;
var username = null;
$(document).ready(function() {
    $("#X_button").click(function() {
        socket.emit("sendInput", { user_input: "X" });
    });
});

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

function fillNES() {
    var a_button = $('<div class="A_button"><input type="button" value=""/></div>');
    var b_button = $('<div class="B_button"><input type="button" value=""/></div>');
    var d_pad = $('<div class="D_pad"><input type="button" value=""/></div>');
    $("#button_layout").append(a_button);
    $("#button_layout").append(b_button);
    $("#button_layout").append(d_pad);
}

function fillSNES() {
    fillNES();
    var x_button = $('<div class="X_button"><input type="button" value=""/></div>');
    var y_button = $('<div class="Y_button"><input type="button" value=""/></div>');
    $("#button_layout").append(x_button);
    $("#button_layout").append(y_button);

}
socket.on('initialize', function(data) {
    console.log(data);
    gamemode = data.mode ? 'chaos' : 'democracy';
    input_type = data.input_type;
    console.log(input_type);
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
                fillSNES();
                break;
            }
        default:
            {
                break;
            }
    }
});
window.beforeunload = function() {
    if (username != null) socket.emit("disconnect", username);
}
main();
