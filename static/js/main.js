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
    console.log("here");
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
        var width = $(this).width();
        var height = $(this).height();
        var relativeX = (e.pageX - offset.left);
        var relativeY = (e.pageY - offset.top);
        var forceX = relativeX < width / 2 ? ((width/2)-relativeX) : ((width/2)+relativeX);
        var forceY = relativeY < height / 2 ? ((height/2)-relativeY) : ((height/2)+relativeY);
        var command = "";
        if (relativeX < width / 2) {
            command = "A";
        } else {
            command = "D";
        }
        if (relativeY < height / 2) {
            command = "S";
        } else {
            command = "W";
        }
        console.log([offset,
            {"width":width},
            {"height":height},
            {"relativeX":relativeX},
            {"relativeY":relativeY},
            {"forceX":forceX},
            {"forceY":forceY}
        ]);
        console.log(command);
        socket.emit("sendInput", {
            user_input: command
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