const chatRoom = document.querySelector("#chat_room");
const sendMessageElement = document.querySelector("#send_message");
const actualMessage = document.querySelector("#chat_msg");
let chatLogsElement = document.querySelector("#chat_logs");


function sendMessage() {
  console.log(chatRoomName);
  chatSocket.send(
    JSON.stringify({
      type: "message",
      message: actualMessage.value,
      name: chatRoomName,
    })
  );
  actualMessage.value = "";
}



function receiveMessage(data) {
  console.log("Now prinint gmessages", data);
  if (data.type == "chat_message") {
    if (data.agent) {
      chatLogsElement.innerHTML += `
        <div class="agent">
          <div class="initials">${data.initials}</div>
          <div class="chat-message">${data.message}</div>
        <div/>
      `;
    } else {
      chatLogsElement.innerHTML += `
        <div class="client">
          <div class="initials">${data.initials}</div>
          <div class="chat-message">${data.message}</div>
        <div/>
      `;
    }
  }
}



sendMessageElement.addEventListener("click", (e) => {
  e.preventDefault();

  sendMessage();
});