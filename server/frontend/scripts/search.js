const search = () => {
   let s = document.getElementById("idsearch").value;
   if (s != '') {
    document.getElementById("items").innerHTML = ''
      fetch("http://localhost:8000/search/" + s, {
         method: "GET",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
      })
         .then((response) => response.json())
         .then((response) => {
            if(response.result){
                response.data.forEach(element => {
                    document.getElementById("items").innerHTML += createItem(element)
                });
            }
         });
   }else{
      document.getElementById("items").innerHTML = ''
   }
};

const createItem = (el) => {
   if(el.profile_pic == null){
      el.profile_pic = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png";

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
/*
<li class="list-group-item bg-transparent" style="border: 1px solid white">
         
         <div class="row">
            <div class="col align-self-start">
               <img
                  src = "${el.profile_pic}"
                  style="border-radius: 50%"
                  height="40px"
               >
            </div>
            <div class="col" style="margin-left: 0px">
               ${el.fullname}
            </div>
         </div>
      </li>*/