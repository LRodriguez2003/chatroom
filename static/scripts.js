var socket = io();

socket.on("message", function(msg) {
    let chat = document.getElementById("chat");
    let messageElement = document.createElement("p");
    messageElement.innerText = msg;
    chat.appendChild(messageElement);
});

function sendMessage() {
    let msg = document.getElementById("message").value;
    socket.send(msg);
    document.getElementById("message").value = "";
}