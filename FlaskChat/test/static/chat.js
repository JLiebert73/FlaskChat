document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    function sendMessage() {
        const messageInput = document.getElementById("message-input");
        const message = messageInput.value;
        socket.emit("chat message", message);
        messageInput.value = "";
    }
    document.getElementById("send-button").addEventListener("click", sendMessage);

    socket.on("chat message", (data) => {
        const chatMessages = document.querySelector(".chat-messages");
        const messageElement = document.createElement("li");
        messageElement.innerText = `${data.sender}: ${data.message}`;
        chatMessages.appendChild(messageElement);
    });
});
