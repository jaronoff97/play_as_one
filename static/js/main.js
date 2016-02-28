var socket_name = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(socket_name);
var gamemode = null,
    input_type = null;
var username = null;

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
    var a_button = $('<img id="A_button" src="/static/images/A_button.png"/>');
    var b_button = $('<img id="B_button" src="/static/images/B_button.png"/>');
    var d_pad = $('<img id="D_pad" src="/static/images/D_pad.png"/>');
    $("#button_layout").append(a_button);
    $("#button_layout").append(b_button);
    $("#button_layout").append(d_pad);
    $("#A_button").click(function() {
        socket.emit("sendInput", {
            user_input: "A"
        });
    });
    $("#B_button").click(function() {
        socket.emit("sendInput", {
            user_input: "B"
        });
    });
    $("#D_pad").click(function(e) {
        var offset = $(this).offset();
        var dx = (e.pageX - offset.left);
        var dy = (e.pageY - offset.top);
        socket.emit("sendInput", {
            user_input: "X"
        });
    });
}

function fillSNES() {
    fillNES();
    var x_button = $('<img id="X_button" src="/static/images/X_button.png"/>');
    var y_button = $('<img id="Y_button" src="/static/images/Y_button.png"/>');
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