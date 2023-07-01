const createPost = (post) => {
   if (post.profile_pic == null) {
      post.profile_pic =
         "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png";
   }

   let iconlike = `<img id="comment_like_${post.id_post}" src="../assets/like-black.png" alt="" onclick="likeAction(true,'${post.id_post}',this.id)" height="35px">`;
   if (post.is_there_like) {
      iconlike = `<img id="comment_like_${post.id_post}" src="../assets/likered.png" alt="" onclick="likeAction(false,'${post.id_post}',this.id)" height="35px">`;
   }
   let commentStyle = 'style="opacity: 0.5;"';
   let commentFunction = "";
   if (post.comment_flag) {
      commentStyle = "";
      commentFunction = 'onclick="showCommentForm()"';
   }
   let s = `<div class="post" id="post">
    <div class="card bg-transparent">
      <h5 class="card-header ">${formatDateTime(post.creation_date)}</h5>
      <div class="card-body">
        <div class="first-body d-flex flex-row">
          <div class="d-flex justify-content-start">
            <img id="imgpic" src="${post.profile_pic}" alt="">
          </div>
          <div id="profileinfo">
            <h5 class="card-title" id="name">${post.fullname}</h5>
            <h6 class="card-title" id="username"><a href="/frontend/html/user.html?username=${
               post.username
            }">@${post.username}</a></h6>
          </div>
        </div>
        
        <h3 class="title">${post.title}</h3>
        <p class="card-text">${post.content}</p>
        <div class="second-body row">
          <div class="col-sm option">
            <img src="../assets/comment-black.png" ${commentStyle} ${commentFunction} alt="" height="35px">
            <div class="number">${post.comments.length}</div>
          </div>
          <div class="col-sm option">
             ${iconlike}
            <div class="number" id="post_number_of_like_${post.id_post}">${
      post.number_of_like
   }</div>
          </div>
          <div class="col-sm option" onclick="options('${post.id_post}')" data-toggle="modal" data-target="#exampleModal">
            <img src="../assets/dots-black.png" alt="" height="35px">
          </div>
        </div>
        </div>
      </div>
    </div>
  </div>
    `;
   return s;
};

const createComment = (element) => {
   if (element.profile_pic == null || element.profile_pic == "") {
      element.profile_pic =
         "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png";
   }

   let like = "";
   if (element.is_there_like) {
      like = `<img class="likeemoji" id="comment_like_${element.id_comment}" src="../assets/likered.png" onclick="likeAction(false,'${element.id_comment}',this.id)" alt="" style="height: 30px;">`;
   } else {
      like = `<img class="likeemoji" id="comment_like_${element.id_comment}" src="../assets/like-black.png" alt="" onclick="likeAction(true,'${element.id_comment}',this.id)" style="height: 30px;">`;
   }

   let showCommentOfCommentButton = "";
   let showCommentOfCommentID = "";
   if (element.children && element.children.length > 0) {
      showCommentOfCommentButton = `
      <div class="col align-self-end">
            <div class="answerComment" id="show-${element.id_comment}" onclick="showCommentOfCommentBox('${element.id_comment}', '${element.username}')">Mostra risposte</div>
         </div>
         `;
      showCommentOfCommentID = `
      <div id="showcomment-${element.id_comment}" style="display:none">
         <div class="form-group" id="commentOfComments-${element.id_comment}">
               
         </div>
      </div>
      `;
   }

   let s = `
    <div class="card bg-transparent">
        <div class="card-body d-flex justify-content-between">
            <div>
                <img class="commentpic" src="${element.profile_pic}" alt="">
            </div>
            <div class="comment-content">
                <a href="/frontend/html/user.html?username=${element.username}"><h4>@${element.username}</h4></a>
                <h5 class="comment-content">${element.content}</h5>
            </div>
            <div>
                ${like}
                <span  id="comment_number_of_like_${element.id_comment}" style="margin-left: 7px">${element.number_of_like}</span>
            </div>
        </div>
        <div class="row">
         <div class="col align-self-start">
            <div class="answerComment" id="resp-${element.id_comment}" onclick="showCommentOfComment('${element.id_comment}', '${element.username}')">Rispondi</div>
         </div>
         ${showCommentOfCommentButton}
      </div>
         <div id="addcomment-${element.id_comment}" style="width: 90%;margin-left: 20px;display:none">
            <div class="form-group" id="commentForm-${element.id_comment}">
               <textarea class="form-control bg-transparent" id="idanswer-${element.id_comment}" rows="3" style="resize: none;" placeholder="Scrivi il tuo commento"></textarea>
               <button type="submit" class="btn btn-primary" style="margin-top: 15px;" onclick="answerComment('${element.id_comment}')">Commenta</button>
            </div>
         </div>
         ${showCommentOfCommentID}
   </div>
    `;
   return s;
};

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const id_post = "post_" + urlParams.get("id_post");

fetch("http://localhost:8000/post/get/" + id_post, {
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
      console.log(response);
      if (response.result) {
         if(response.data == null){
            document.getElementById("error-msg").innerHTML = "Il post è stato nascosto dall'autore"
         }else{
            document.getElementById("father").innerHTML = createPost(
               response.data
            );
            let comments = response.data.comments;
         comments = filter(comments);

         comments = comments.sort(
            (a, b) => b.number_of_like - a.number_of_like
         );

         console.log(comments);

         comments.forEach((element) => {
            document.getElementById("comments-section").innerHTML +=
               createComment(element);
            console.log(element.children);
            if (element.children.length > 0) {
               element.children.forEach((son) => {
                  document.getElementById(
                     "commentOfComments-" + element.id_comment
                  ).innerHTML += createComment(son);
               });
            }
         });
         }
         

         
      } else {
         document.getElementById("error-msg").innerHTML = "<h1>" + response.error + "</h1>";
      }
   });

const showCommentForm = () => {
   if (document.getElementById("commentForm").style.display == "none") {
      document.getElementById("commentForm").style.display = "block";
   } else {
      document.getElementById("commentForm").style.display = "none";
   }
};

const newComment = () => {
   let msg = document.getElementById("idcomment").value;
   if (msg) {
      fetch("http://localhost:8000/comments/new", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: localStorage.getItem("token").split(" ")[1],
            id_post: id_post,
            content: msg,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            console.log(response);
            if (response.result) {
               location.reload()
            } else {
               document.getElementById("error-msg").innerHTML = "<h1>" + response.error + "</h1>";
            }
         });
   }
};

const showCommentOfComment = (id_comment, username) => {
   console.log(id_comment)
   if (
      document.getElementById(`addcomment-${id_comment}`).style.display ==
      "none"
   ) {
      document.getElementById(`addcomment-${id_comment}`).style.display =
         "block";
      document.getElementById(`showcomment-${id_comment}`).style.display =
         "none";
      document.getElementById(`resp-${id_comment}`).innerHTML =
         "Rispondi a @" + username;
   } else {
      document.getElementById(`addcomment-${id_comment}`).style.display =
         "none";
      document.getElementById(`resp-${id_comment}`).innerHTML = "Rispondi";
   }
};

const showCommentOfCommentBox = (id_comment) => {
   if (
      document.getElementById(`showcomment-${id_comment}`).style.display ==
      "none"
   ) {
      document.getElementById(`showcomment-${id_comment}`).style.display =
         "block";
      document.getElementById(`show-${id_comment}`).innerHTML =
         "Nascondi risposte";
      document.getElementById(`addcomment-${id_comment}`).style.display =
         "none";
   } else {
      document.getElementById(`showcomment-${id_comment}`).style.display =
         "none";
      document.getElementById(`show-${id_comment}`).innerHTML =
         "Mostra risposte";
   }
};

const answerComment = (id) => {
   let msg = document.getElementById("idanswer-" + id).value;
   if (msg) {
      fetch("http://localhost:8000/comments/new", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: localStorage.getItem("token").split(" ")[1],
            id_post: id_post,
            content: msg,
            reference_comment: id,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            console.log(response);
            if (response.result) {
               window.location.reload()
            } else {
               document.getElementById("error-msg").innerHTML = "<h1>" + response.error + "</h1>";
            }
         });
   }
};
const filter = (comments) => {
   let fatherComments = getFathers(comments);
   fatherComments.forEach((element) => {
      element.children = [];
   });
   let sonComments = getNotFathers(comments);
   let c = 1;
   sonComments.forEach((son) => {
      let fatherID = getLastComment(son, comments);
      let fatherOBJ = fatherComments.filter((obj) => {
         return obj.id_comment == fatherID;
      });
      fatherOBJ[0].children.push(son);
   });
   return fatherComments;
};

const getFathers = (list) => {
   const filteredList = list.filter((obj) => obj.reference_comment == null);
   return filteredList;
};

const getNotFathers = (list) => {
   const filteredList = list.filter((obj) => obj.reference_comment != null);
   return filteredList;
};
const getLastComment = (obj, comments_list) => {
   if (obj.reference_comment == null) {
      return obj.id_comment;
   } else {
      let result = riscontro(comments_list, obj);
      return getLastComment(result, comments_list);
   }
};
const riscontro = (comments_list, obj) => {
   let s = "error";
   comments_list.forEach((el) => {
      if (el.id_comment == obj.reference_comment) {
         s = el;
      }
   });
   return s;
};

const likeAction = (like, id, id_element) => {
   fetch("http://localhost:8000/like/new", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
         token: localStorage.getItem("token").split(" ")[1],
         like: like,
         id_element: id,
      }),
   })
      .then((response) => response.json())
      .then((response) => {
         if (response.result) {
            let value = parseInt(
               document.getElementById(
                  `${id.split("_")[0]}_number_of_like_${id}`
               ).innerText
            );
            if (like) {
               document.getElementById(id_element).src =
                  "../assets/likered.png";
               document.getElementById(id_element).onclick = function () {
                  likeAction(false, id, id_element);
               };
               value = value + 1;
            } else {
               document.getElementById(id_element).src =
                  "../assets/like-black.png";
               document.getElementById(id_element).onclick = function () {
                  likeAction(true, id, id_element);
               };
               value = value - 1;
            }
            document.getElementById(
               `${id.split("_")[0]}_number_of_like_${id}`
            ).innerText = value.toString();
         } else {
            console.log(response.error);
            document.getElementById("error-msg").innerHTML = "<h1>" + response.error + "</h1>";
         }
      });
};

const options = (id_post) => {
   /*
   document.getElementById("modal-body").innerHTML = `
   <li style="width: 100%;"><div style="text-align: center;cursor: pointer;" onclick="share('${id_post}')">Condividi</div></li>
   <li style="width: 100%;"><div style="text-align: center;cursor: pointer;" onclick="report('${id_post}')">Segnala</div></li>
   `*/
   document.getElementById("modal-body").innerHTML = "Al momento non ci sono opzioni disponibili<br><img class='d-flex justify-content-center' src='../assets/process.png' height='50px' />"

};
