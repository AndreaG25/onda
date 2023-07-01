
window.addEventListener("load", (event) => {
   verifyToken(false)
   fetch("http://localhost:8000/user/myinfo", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(' ')[1],
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if(response.result){
            insertData(response.info)
            response.posts.forEach(element => {
               document.getElementById("posts").innerHTML += insertPosts(element)
            });
         }else{
            alert("Errore nel caricamento dei dati")
         }
         
      });
});

const updateDatas = () => {
   let fullname = document.getElementById("idfullname").value
   let born_date =  document.getElementById("idborndate").value
   let description = document.getElementById("iddescription").value
   let checkForm = validateUpdateData(born_date, fullname)
   if(checkForm[0]){
      fetch("http://localhost:8000/change/myinfo", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
         fullname: fullname,
         born_date: born_date,
         description: description,
         privacy_account:
            document.querySelector('input[name="accountprivacy"]:checked')
               .value == true,
      }),
   })
      .then((response) => response.json())
      .then((response) => {
        console.log(response)
         if (response) {
            alert("Profilo aggiornato correttamente");
            window.location.reload()
         }else{
            document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto nella modifica"
         }
      });
   }else {
      document.getElementById("error-msg").innerHTML = checkForm[1][0];
   }
};

const changePic = (url) => {
    let msg = "Sei sicuro di voler cambiare l'immagine?"
    if(url == ''){
        msg = "Sei sicuro di voler rimuovere l'immagine?"
    }
   if (confirm(msg) == true) {
      fetch("http://localhost:8000/change/pic", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: localStorage.getItem("token").split(" ")[1],
            url: url,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            if (response) {
                if(url == ''){
                    alert("Foto profilo rimossa con successo");
                }else{
                    alert("Foto profilo aggiornata con successo");
                }
                window.location.reload()
            }else{
                document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto nel cambio dell'immagine"
            }
         });
   }
};

const showEditImage = () => {
   if (document.getElementById("editImageBox").style.display == "none") {
      document.getElementById("editImageBox").style.display = "block";
   } else {
      document.getElementById("editImageBox").style.display = "none";
   }
};

const insertPosts = (post) => {
   let wordShow = "Rendi pubblico"
   let iconShow = "../assets/eye-show-black.png"
   let boolShow = true
   if(post.public_flag){
      iconShow = "../assets/eye-hide-black.png"
      wordShow = "Nascondi"
      boolShow = false
   }
   let s = `
    
          <div class="card bg-transparent">
            <div class="card-header">${formatDateTime(post.creation_date)}</div>
            <div class="card-body">
            <a href="/frontend/html/post.html?id_post=${(post.id_post).split('_')[1]}">
              <h5 class="card-title">${post.title}</h5>
              <p class="card-text">${post.content}</p>
            </a>
              <div class="second-body row">
                
                  <div class="col-sm option" style="cursor:pointer" onclick="deletePost('${post.id_post}')">
                     <img src="../assets/trash-black.png" alt="" height="25px" />
                     <div class="number">Elimina</div>
                  </div>
                  <div class="col-sm option" style="cursor:pointer" onclick="edit_public_flag('${post.id_post}',${boolShow})">
                     <img src="${iconShow}" alt="" height="25px" />
                     <div class="number">${wordShow}</div>
                  </div>
                  
                  <div class="col-sm option" style="cursor:pointer" onclick="window.location.href = './editpost.html?id_post=${(post.id_post).split('_')[1]}'">
                     <img src="../assets/newpost.png" alt="" height="25px" />
                     <div class="number">Modifica</div>
                  </div>
                  
              </div>
            </div>
          </div>
    `;
   return s;
};

const switchSection = (which) => {
    if (which) {
      document.getElementById("datasButton").classList.add("active");
      document.getElementById("data").style.display = "block";
  
      document.getElementById("postsButton").classList.remove("active");
      document.getElementById("posts").style.display = "none";
    } else {
      document.getElementById("datasButton").classList.remove("active");
      document.getElementById("data").style.display = "none";
  
      document.getElementById("postsButton").classList.add("active");
      document.getElementById("posts").style.display = "block";
    }
};

const insertData = (data) => {
    document.getElementById("idfullname").value = data.fullname;
    document.getElementById("idborndate").value = data.born_date;
    document.getElementById("iddescription").innerHTML = data.description;
    if (data.privacy_account) {
       document.getElementById("idprivacy1").checked = true;
    } else {
       document.getElementById("idprivacy0").checked = true;
    }
    if (data.profile_pic != null) {
       document.getElementById("imgpic").src = data.profile_pic;
       document.getElementById("urlPic").value = data.profile_pic;
    }
};
 
const edit_public_flag = (id_post, action) => {
   let s = "Sei sicuro di rendere privato il post?"
   if(action){
      s = "Sei sicuro di rendere pubblico il post?"
   }
   res = window.confirm(s)
   if(res){
      fetch("http://localhost:8000/post/change_public_flag", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: localStorage.getItem("token").split(" ")[1],
            id_post: id_post,
            action: action
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            console.log(response)
            if (response.result) {
               window.location.reload()
            }else{
               document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto"
            }
         });
   }
}

const deletePost = (id_post) => {
   res = window.confirm("Sei sicuro di voler rimuovere in modo definito il post?")
   if(res){
      fetch("http://localhost:8000/post/delete", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: localStorage.getItem("token").split(" ")[1],
            id_post: id_post,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            console.log(response)
            if (response.result) {
               window.location.reload()
            }else{
               document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto"
            }
         });
   }
}