var socket_name = 'http://' + document.domain + ':' + location.port;
var socket = io.connect(socket_name);
var gamemode = null,
    input_type = null;
var username = null;

function main() {
    // create, initiate and append game canvas
    username = window.prompt("Enter a username", "Username");
    init(); // initiate game objects
    $("#container").hide();
    //$(document).keydown(keyDown); //add keylisteners
    //$(document).keyup(keyUp);
    //draw();
}

function init() {
    socket.emit('add user', username);
}

function fillNES() {
    var a_button = $('<img id="A_button" class="A" src="/static/images/A_button.png"/>');
    var b_button = $('<img id="B_button" class = "B" src="/static/images/B_button.png"/>');
    var d_pad = $('<img id="D_pad" class = "DPad" src="/static/images/D_pad.png"/>');
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
        var forceX = ((width/2)-relativeX);
        var forceY = ((height/2)-relativeY);
        var command = "";
        if (forceX>0 && Math.abs(forceX)>Math.abs(forceY)) {
            command = "left";
        }
        if (forceX<0 && (Math.abs(forceX))>Math.abs(forceY)) {
            command = "right";
        }
        if(forceY<0 && (Math.abs(forceY))>Math.abs(forceX)){
            command = "down";
        }
        if(forceY>0 && Math.abs(forceY)>Math.abs(forceX)){
            command="up";
        }
        socket.emit("sendInput", {
            user_input: command
        });
    });
}

function fillSNES() {
    fillNES();
    var x_button = $('<img id="X_button" class="X"  src="/static/images/X_button.png"/>');
    var y_button = $('<img id="Y_button" class="Y" src="/static/images/Y_button.png"/>');
    $("#XY_layout").append(x_button);
    $("#XY_layout").append(y_button);
    $("#X_button").click(function() {
        socket.emit("sendInput", {
            user_input: "X"
        });
    });
    $("#Y_button").click(function() {
        socket.emit("sendInput", {
            user_input: "Y  "
        });
    });
}
function fillKeyboard(){
    $("#container").removeClass('hidden');
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
                fillKeyboard();
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