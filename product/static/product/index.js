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
const chatOpen = document.querySelector("#chat_open")
const chatName = document.querySelector("#chat_name")
const JoinChat = document.querySelector("#join_chat");
const msgCenterElement = document.querySelector("#msg_center");
const chatRoom = document.querySelector("#chat_room");


/**
 * Connection based elements
 */

let chatSocket = null
let chatRoomName = ''
let windowUlr = window.location.url
let chatRoomId = Math.random().toString(36).slice(2, 15)
/**
 * functions
 */

chatOpen.addEventListener('click', () => {
    chatOpen.style.display = 'None'
    msgCenterElement.style.display = "block";
})

JoinChat.addEventListener('click', () => {
    chatRoom.style.display = "block"
    msgCenterElement.style.display = "none";
})
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
