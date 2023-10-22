document.addEventListener("DOMContentLoaded", () => {


    const socket = io();
    function appendMessage(message, sender) {
        const chatMessages = document.querySelector(".chat-messages");
        const messageElement = document.createElement("li");
        messageElement.innerText = `${sender}: ${message}`;
        chatMessages.appendChild(messageElement);
    }
    socket.on("chat message", (data) => {
        appendMessage(data.message, data.sender);
    });
});
