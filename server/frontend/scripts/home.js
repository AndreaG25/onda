const openSection = (evt, value) => {
    let i, x, tablinks;
    x = document.getElementsByClassName("sections");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-border-indigo", "");
    }
    document.getElementById(value).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-border-indigo";
}

const createHomePost = (post) => {
  console.log(post)
  if (post.profile_pic == null || post.profile_pic == "") {
    post.profile_pic = "../assets/no_profile.png";
  }
  if(post.content.length > 300){
    post.content = post.content.slice(0, 300) + ` <a class="bg_blue_href" href='./post.html?id_post=${(post.id_post).split('_')[1]}'> Leggi tutto</a>`;
  }
  let s = `
  <div class="post" id="post">
    <div class="card bg-transparent">
      <h5 class="card-header">${formatDateTime(post.creation_date)}</h5>
      <div class="card-body">
        <div class="first-body d-flex flex-row">
          <div class="d-flex justify-content-start">
            <img id="imgpic" src="${post.profile_pic}" alt="">
          </div>
          <div id="profileinfo">
            <h5 class="card-title" id="name">${post.fullname}</h5>
            <h6 class="bg_blue_href" id="username"><a href="/frontend/html/user.html?username=${post.username}">@${post.username}</a></h6>
          </div>
        </div>
        <a href='./post.html?id_post=${(post.id_post).split('_')[1]}'><div id="content-box">
          <h3 class="title">${post.title}</h3>
          <p class="card-text">${post.content}</p>
        </div></a>
        </div>
      </div>
    </div>
  </div>
    `;
   return s;
};

let testComment = 
{
  "result": true,
  "data": {
      "id_post": "post_hwfczibxlajmuixeofghereuvqogbl4jyxyy",
      "fullname": "Andrea Gritti",
      "username": "andrea",
      "profile_pic": null,
      "title": "test",
      "content": `What is Lorem Ipsum?
      Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
      
      Why do we use it?
      It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).`,
      "creation_date": "2023-05-18 17:16:53.503790",
      "comment_flag": true,
      "number_of_like": 0,
      "is_there_like": false,
      "comments": []
  }
}
/*
const formatDateTime = (dateTimeStr) => {
  const dateTime = new Date(dateTimeStr);
  const year = dateTime.getFullYear();
  const month = ("0" + (dateTime.getMonth() + 1)).slice(-2);
  const day = ("0" + dateTime.getDate()).slice(-2);
  const hours = ("0" + dateTime.getHours()).slice(-2);
  const minutes = ("0" + dateTime.getMinutes()).slice(-2);
  return `${day}/${month}/${year} ${hours}:${minutes}`;
};



document.getElementById("followPostList").innerHTML = createHomePost(testComment.data)
document.getElementById("followPostList").innerHTML += createHomePost(testComment.data)
document.getElementById("followPostList").innerHTML += createHomePost(testComment.data)
document.getElementById("followPostList").innerHTML += createHomePost(testComment.data)
*/

const getHome = () => {
  document.getElementById("sb-username").innerHTML = "@" + getUsernameFromToken(localStorage.getItem("token").split(' ')[1])
  fetch("http://localhost:8000/home/", {
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
        if(response.profile_pic){
          document.getElementById("profilePic").src = response.profile_pic
        }
        if(response.post_by_follower.length <= 0){
          document.getElementById("followPostList").innerHTML = "<h1>Non ci sono post al momento</h1>"
        }else{
          response.post_by_follower.forEach(element => {
            document.getElementById("followPostList").innerHTML += createHomePost(element)
          });
        }
        if(response.recent_post.length <= 0){
          document.getElementById("recentPostList").innerHTML = "<h1>Non ci sono post al momento</h1>"
        }else{
          response.recent_post.forEach(element => {
            document.getElementById("recentPostList").innerHTML += createHomePost(element)
          });
        }
      });
}

getHome()