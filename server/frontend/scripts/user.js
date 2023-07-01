const createPost = (post) => {
   let iconlike = "../assets/iconlike.png";
   if (post.is_there_like) {
      iconlike = "../assets/likered.png";
   }
   let id_post = post.id_post.split('_')[1]
   let s = `
  <a href="/frontend/html/post.html?id_post=${id_post}">
        <div class="card bg-transparent">
          <div class="card-header">${formatDateTime(post.creation_date)}</div>
          <div class="card-body">
            <h5 class="card-title">${post.title}</h5>
            <p class="card-text">${post.content}</p>
          </div>
        </div>
      </a>
  `;
   return s;
};

/*
closeprofile
pendentrequest
allright
*/
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username = urlParams.get('username')
if(username == getUsernameFromToken(localStorage.getItem("token").split(" ")[1])){
   window.location.href = "/frontend/html/profile.html"
}else{
   fetch("http://localhost:8000/user/get/" + username, {
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
      console.log(response)
      if (response.result) {
         insertSimpleInformations(response.info);
         insertButtons(response.relation);
         if (response.relation == 2 || response.relation == 3) {
            response.posts.forEach((element) => {
               document.getElementById("posts").innerHTML +=
                  createPost(element);
            });
         }
      } else {
         if (response.code == 404) {
            document.getElementById("error-msg").innerHTML = response.error;
         }
      }
   });
}



const insertSimpleInformations = (response) => {
   document.getElementById("idfullname").innerHTML = response.fullname;
   document.getElementById("iddescription").innerHTML = response.description;
   document.getElementById("idusername").innerHTML =
      '<a href="/frontend/html/user.html?username=' +
      response.username +
      '">@' +
      response.username +
      "</a>";
   document.getElementById("numberofpost").innerHTML = response.number_of_posts;
   document.getElementById("numberoffollowers").innerHTML =
      response.number_of_followers;
   document.getElementById("numberoflike").innerHTML = response.number_of_like;
   if (response.profile_pic != null) {
      document.getElementById("imgpic").src = response.profile_pic;
   }
};

const insertButtons = (relation) => {
   let s = "";
   if (relation == 0) {
      s = `
    <button id="followbtn" class="btn btn-primary" onclick="updateFollow(1, ${relation})">Segui</button>
    <button id="followbtn" class="btn btn-primary disabled">
      Invia messaggio
    </button>
    <button id="followbtn" class="btn btn-primary">Blocca</button>
    `;
      privateAccount(false);
   } else if (relation == 1) {
      s = `
    <button id="followbtn" class="btn btn-light" onclick="updateFollow(0, ${relation})">Richiesta inviata</button>
    <button id="followbtn" class="btn btn-primary disabled">
      Invia messaggio
    </button>
    <button id="followbtn" class="btn btn-primary">Blocca</button>
    `;
      privateAccount(true);
   } else if (relation == 2) {
      s = `
    <button id="followbtn" class="btn btn-light" onclick="updateFollow(0, ${relation})">Segui già</button>
    <button id="followbtn" class="btn btn-primary" onclick="createChat('${username}')">
      Invia messaggio
    </button>
    <button id="followbtn" class="btn btn-primary">Blocca</button>
    `;
   }else if(relation == 3){
      s = `
    <button id="followbtn" class="btn btn-primary" onclick="updateFollow(2, ${relation})">Segui</button>
    <button id="followbtn" class="btn btn-primary disabled">
      Invia messaggio
    </button>
    <button id="followbtn" class="btn btn-primary">Blocca</button>
    `;
   }
   document.getElementById("btn-actions").innerHTML = s;
};

const privateAccount = (request) => {
   let msg =
      "L'account è privato devi effetturare la richiesta per vedere i post";
   if (request) {
      msg = "Vedrai i messaggi quando la richiesta verrà accettata";
   }
   document.getElementById("posts").innerHTML = `
  <div id="private-account" style="text-align: center;">
      <div class="d-flex justify-content-center">
      <img
          id="lock"
          src="../assets/lock_close_black.png"
          alt=""
          style="height: 80px;"
        />
      </div>
        <h1>Profilo privato</h1>
        <h3>${msg}</h3>
    </div>
  `;
};

const updateFollow = (new_state, relation) => {
   let res = false
   if(new_state == 0 && relation == 2){
      res = window.confirm("Sei sicuro di voler smettere di seguire questo profilo?")
   }else if(new_state == 0 && relation == 1){
      res = window.confirm("Sei sicuro di voler cancellare la richiesta?")
   }else if(new_state == 1 && relation == 0){
      res = true
   }else if(new_state == 2 && relation == 3){
      res = true
   }

   if(res){
      fetch("http://localhost:8000/relation/update", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
         new_state: new_state,
         username_recipient: username,
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if (response.result) {
            window.location.reload()
         } else {
            document.getElementById("error-msg").innerHTML = response.error;
         }
      });
   }
}

const createChat = (username) => {
   fetch("http://localhost:8000/chat/new", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
         username: username
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if(response.result){
            window.location.href = "./chat.html?chat=" + response.chat
         }else{
            document.getElementById("error-msg").innerHTML = response.error
         }
      });
}