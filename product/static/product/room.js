/**
 * Room element
 */
const chatRoomUuid = document.querySelector("#chat_uuid")
const chatName = document.querySelector("#chat_name")
const agentId = document.querySelector("#agent_id");
const chatElement = document.querySelector("#chat");
const JoinChatElement = document.querySelector("#join_chat");
const msgCenterElement = document.querySelector("#msg_center");
const chatRoom = document.querySelector("#chat_room");
const sendMessageElement = document.querySelector("#send_message");
const actualMessage = document.querySelector("#chat_msg");
let chatLogsElement = document.querySelector("#chat_logs");

console.log(chatRoomUuid);
console.log("object");
/**
 * Websocket elements
 */

let chatSocket = new WebSocket(
  `ws://${window.location.host}/ws/chat/${chatName.innerHTML}`
);
console.log(chatSocket);
chatSocket.onmessage = function (e) {
  console.log("On message")
}

chatSocket.onopen = function (e) {
  console.log("On open");
}

chatSocket.onclose = function (e) {
  console.log("On close")
}
/**
 * Functions
 */


/**
 * Event listeners
 */
sendMessageElement.addEventListener("click", (e) => {
    e.preventDefault();
    sendMessage();
});


const sendMessage = () => {
  chatSocket.send(
    JSON.stringify({
      "type": "message",
      "message": actualMessage.value,
      "name": chatName.innerHTML,
    })
  );

  actualMessage.value = "";
};