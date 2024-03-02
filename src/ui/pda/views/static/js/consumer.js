window.addEventListener("DOMContentLoaded", () => {
  const messages = document.getElementById("messages");
  const websocket = new WebSocket("ws://localhost:5678/");
  
  websocket.onmessage = ({ data }) => {
    const message = document.createElement("li");
    const content = document.createTextNode(data);
    message.appendChild(content);
    messages.appendChild(message);
  };
});
