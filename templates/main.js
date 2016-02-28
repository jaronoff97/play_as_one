var socket = io();

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

setInterval(function(){
        socket.emit('key_state', {
            keystate: keystate,
        });
}, 10)
socket.on('move user', function(data) {
    var indexOfUser = findIndexOfUser(data.id);
    if (indexOfUser != -1) {
        players[indexOfUser].updatePos(data);
    }
    draw();
});
socket.on('move ball', function(data) {
    ball.updatePos(data);
    draw();
});
socket.on('login', function(data) {
    $("#amount_of_users").empty();
    $("#amount_of_users").append("<h2> There are " + data.numUsers + " users connected</h2>");
});
socket.on('user joined', function(data) {
    $("#amount_of_users").empty();
    $("#amount_of_users").append("<h2> There are " + data.numUsers + " users connected</h2>");
    var tempPlayer = Player({
        xpos: data.user["xpos"],
        ypos: data.user["ypos"],
        radius: 25,
        charge: data.user["charge"],
        id: data.user["id"],
        name: data.user["name"]
    });
    players.push(tempPlayer);
    draw();
});
socket.on('user left', function(data){
    players.splice(findIndexOfUser(data.id), 1);
    $("#amount_of_users").empty();
    $("#amount_of_users").append("<h2> There are " + data.numUsers + " users connected</h2>");
});
window.beforeunload = function(){
    socket.emit("disconnect", {});
}
main();