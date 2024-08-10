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

function joinChatRoom() {
  chatRoomName = chatNameElement.value;
  console.log("Room uuid", chatRoomUuid);

  fetch(`/create-room/${chatRoomUuid}/`, {
    method: "POST",
    body: new URLSearchParams({
      name: chatRoomName,
      url: windowURL,
    }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.text()) // Read response as text
    .then((data) => console.log(data)); // Alert the response

  chatSocket = new WebSocket(`ws://${windowURL}/ws/chat/${chatRoomName}`)

  chatSocket.onmessage = (e) => {
    console.log(JSON.parse(e.data)["type"]);
    receiveMessages(JSON.parse(e.data));
    console.log("On message")
  }

  chatSocket.onclose = (e) => {
    console.log("CLosed unexpectedly");
  }

  chatSocket.onopen = (e) => {
    console.log("Chat created/opened");
  }
}

function receiveMessages(data) {
  console.log(data)
  chatLogsElement.innerHTML += `
    <div class="msg_back">
      <p>Received new message</p>
    </div>
  `;
}

const sendMessage = () => {
  chatSocket.send(
    JSON.stringify({
      "type": "message",
      "message":actualMessage.value,
      "name": chatRoomName
    })
  )

  actualMessage.value = ''
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
