/**
 * ShoppingElements
 */
const addToCart = document.querySelectorAll("#addToCart");
const checkout = document.querySelector("#checkout");
const products = document.querySelectorAll(".cart product");

/**
 * Chat Elemets
 */

const chatElement = document.querySelector("#chat")
const chatOpenElement = document.querySelector("#chat_open")
const chatNameElement = document.querySelector("#chat_name")
const JoinChatElement = document.querySelector("#join_chat");
const msgCenterElement = document.querySelector("#msg_center");
const chatRoom = document.querySelector("#chat_room");
const sendMessageElement = document.querySelector("#send_message");
const actualMessage = document.querySelector("#chat_msg");
let chatLogsElement = document.querySelector("#chat_logs");


/**
 * Connection based elements
 */

let chatSocket = null
let chatRoomName = ''
let windowURL = window.location.host
let chatRoomUuid = Math.random().toString(36).slice(2, 15)

/**
 * Functions
 */

function getCookie(cookiename) {
  let cookieValue = null

  if (document.cookie && document.cookie != '') {
    let cookies = document.cookie.split(';')

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim()
      if (cookie.substring(0, cookiename.length + 1) == (cookiename + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(cookiename.length + 1, cookie.length + 1))
        break;
      }
    }
  }
  console.log(cookieValue);
  return cookieValue
}

async function joinChatRoom() {
  chatRoomName = chatNameElement.value;
  console.log("Room uuid", chatRoomUuid);

  console.log("Joined as:", chatRoomUuid);
  console.log("Cookie: ", getCookie('csrftoken'))
  const res = await fetch(`/create-room/${chatRoomUuid}`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/x-www-form-url-encoded; charset=UTF-8'
    },
    body: new URLSearchParams({
      'name': chatRoomName,
      'url': windowURL
    })
  })
  const data = await res.json()
  console.log(data)
  chatSocket = new WebSocket(`ws://${windowURL}/ws/chat/${chatRoomName}`)

  chatSocket.onmessage = function (e) {
    console.log("On message");

    receiveMessage(JSON.parse(e.data));
  }

  chatSocket.onopen = function (e) {
    console.log("On open");
  }

  chatSocket.onclose = function (e) {
    console.log("On close");
  }
}


function sendMessage() {
  console.log(chatRoomName);
  chatSocket.send(
    JSON.stringify({
      "type": "message",
      "message": actualMessage.value,
      "name": chatRoomName
    })
  );
  actualMessage.value = ''
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
/**
 * Event listners
 */

chatOpenElement.addEventListener("click", () => {
  chatOpenElement.style.display = "None";
  msgCenterElement.classList.remove('d-none')
  msgCenterElement.classList.add('d-block')

});

JoinChatElement.addEventListener('click', () => {
  joinChatRoom()
  chatRoom.classList.remove("d-none")
  chatRoom.classList.add("d-block")
  msgCenterElement.classList.add("d-none");
})

sendMessageElement.addEventListener('click', (e) => {
  e.preventDefault()

  sendMessage();
})

// Add items in cart
addToCart.forEach((element) => {
  element.addEventListener("click", async (e) => {
    productId = e.target.getAttribute("data-id");
    try {
      const data = await fetch("{% url 'product:add_to_cart' %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": "{{ csrf_token }}",
        },
        body: new URLSearchParams({
          product_id: productId,
        }),
      });
      //cart = await data.json()
      console.log(await data.json());
    } catch (error) {
      console.log(error);
    }
  });
});
