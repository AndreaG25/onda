let chatInfo = [];
let openedChat = ''
let id_userOpened = ''
const getChats = () => {
   fetch("http://localhost:8000/chat/direct", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if (response.result) {
            chatInfo = response.chats;
            if(response.chats.length == 0){
               document.getElementById("chat-list-ul").innerHTML = "<h4 style='margin-top: 20px'>Nessuna chat al momento</h4>"
            }else{
               response.chats.forEach((element) => {
                  document.getElementById("chat-list-ul").innerHTML +=
                     createChatItem(element);
               });
            }
         }
         console.log(response);
      });
};

getChats();



const createChatItem = (chat) => {
   let s = `
    <li data-chatid="${chat.id_chat}" onclick="openChat('${chat.id_chat}')">${chat.username}</li>
    `;
   return s;
};

const createChatMessage = (message) => {
   let who = "other";
   if (
      message.id_user == getIDUserFromToken(localStorage.getItem("token").split(" ")[1]) ||
      message.id_user_sender == getIDUserFromToken(localStorage.getItem("token").split(" ")[1])
      
   ) {
      who = "mine";
   }
   let s = `
    <div class="message ${who}">
        <p>${message.content}</p>
    </div>
    `;
   return s;
};



const openChat = (id_chat) => {
   document.getElementById("message-body").innerHTML = "";
   document.getElementById("profile-pic-chat").src = getProfilePic(id_chat);
   document.getElementById("username-chat").innerHTML = getProfileUsername(id_chat);
    openedChat = id_chat
    id_userOpened = getIdUser(id_chat)
   document.getElementById("form-footer").style.display = "block";
   fetch("http://localhost:8000/chat/get/" + id_chat, {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if (response.result) {
            let messages = sortByCreationDate(response.data);
            messages.forEach((element) => {
               document.getElementById("message-body").innerHTML +=
                  createChatMessage(element);
            });
            document.getElementById("message-body").scrollTop =
               document.getElementById("message-body").scrollHeight;
         }else{
            console.log(response)
         }
      });
};

const getProfilePic = (id_chat) => {
   const chat = chatInfo.find((chat) => chat.id_chat == id_chat);
   if (chat) {
      if (chat.profile_pic == null) {
         return "../assets/no_profile.png";
      }
      return chat.profile_pic;
   } else {
      return null;
   }
};

const getProfileUsername = (id_chat) => {
   const chat = chatInfo.find((chat) => chat.id_chat == id_chat);
   if (chat) {
      return chat.username;
   } else {
      return null;
   }
};

const getIdUser = (id_chat) => {
    const chat = chatInfo.find((chat) => chat.id_chat == id_chat);
   if (chat) {
      return chat.id_user;
   } else {
      return null;
   }
}

const sortByCreationDate = (arr) => {
   arr.sort(function (a, b) {
      var dateA = new Date(a.creation_date.replace(" ", "T"));
      var dateB = new Date(b.creation_date.replace(" ", "T"));
      return dateA - dateB;
   });
   return arr;
};

const websocket = new WebSocket("ws://localhost:8765/");

websocket.onopen = function (event) {
    const token = localStorage.token.split(' ')[1];
    websocket.send(token);
};

websocket.onmessage = function (event) {
   console.log(event.data)
    const notification = JSON.parse(event.data);
    if(notification.id_chat == openedChat){
        document.getElementById("message-body").innerHTML += createChatMessage(notification)
    }
    document.getElementById("message-body").scrollTop = document.getElementById("message-body").scrollHeight;
};

const sendMessage = () => {
    if (websocket.readyState === WebSocket.OPEN) {
        if(document.getElementById("message-input").value != ''){
            websocket.send(JSON.stringify(createMessage()));
            document.getElementById("message-input").value = ''
        }   
    } else {
        console.log("La connessione non è ancora stata stabilita.");
    }
};
const createMessage = () => {
    const message = {
    id_user_sender: getIDUserFromToken(localStorage.token.split(' ')[1]),
    id_user_recipient: id_userOpened,
    content: document.getElementById("message-input").value,
    creation_date: getCurrentTime(),
    id_chat: openedChat
    };
    return message
}

const params = new URLSearchParams(window.location.search);
const chatParam = params.get('chat');
if(chatParam){
   params.delete('chat');
   const newUrl = `${window.location.pathname}?${params.toString()}`;
   window.history.replaceState({}, '', newUrl);
}


setTimeout(function() {
   let img = document.getElementById("profile-pic-chat");
   img.src = "../assets/comment-black.png";
   if(chatParam){
      openChat(chatParam);
   }
}, 500);
