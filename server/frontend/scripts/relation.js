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

const getRelations = () => {
    fetch("http://localhost:8000/relation/getrelations", {
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
        
        if(response.followers.length <= 0){
          document.getElementById("followerList").innerHTML = "<h1>Non ci sono followers al momento</h1>"
        }else{
          response.followers.forEach(element => {
            document.getElementById("followerList").innerHTML += createItem(element)
          });
        }

        
        if(response.followed.length <= 0){
            document.getElementById("followList").innerHTML = "<h1>Non segui ancora nessuno</h1>"
          }else{
            response.followed.forEach(element => {
              document.getElementById("followList").innerHTML += createItem(element)
            });
        }


        if(response.requests.length <= 0){
            document.getElementById("requestsList").innerHTML = "<h1>Nessuna richiesta</h1>"
        }else{
            response.requests.forEach(element => {
                document.getElementById("requestsList").innerHTML += createItem(element)
            });
        }
      });
}
getRelations()


const createItem = (el) => {
  if(!(el.profile_pic)){
    el.profile_pic = "../assets/no_profile.png"
  }
  let s = `
  <a href="/frontend/html/user.html?username=${el.username}">
      <li class="list-group-item bg-transparent" style="border: 1px solid white">
      <div class="d-flex align-items-center">
         <div class="align-self-start">
            <img src="${el.profile_pic}" style="border-radius: 50%" height="40px" width="40px">
         </div>
         <div class="ml-3">
            ${el.fullname}
         </div>
      </div>
      </li>

      </a>
  `
  return s
}