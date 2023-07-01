window.addEventListener("load", (event) => {
    fetch("http://localhost:8000/relation/home", {
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
        console.log(response)
          if(response.result){
            if(response.data.length == 0){
               document.getElementById("requests-section").innerHTML = "<h2 style='text-align: center;'>Non ci sono richieste, al momento</h2>"
            }else{
               response.data.forEach(element => {
                  document.getElementById("requests-section").innerHTML += createRequestComponent(element)
               });
            }
            
          }else{
            alert("Errore nel caricamento dei dati")
          }
       });
 });

 const createRequestComponent = (request) => {
   if(request.profile_pic == null){
      request.profile_pic = "../assets/no_profile.png";
   }
    let s = `
    <div class="card bg-transparent" id="id_box_${request.id_follow}">
        <div class="card-body row">
        <div class="col-sm">
            <div>
                <img id="profilepic" src="${request.profile_pic}" >
            </div>
        </div>
        <div class="col-sm">
            <div id="data">
               <h4 id="idfullname">${request.fullname}</h4>
               <a href="/frontend/html/user.html?username=${request.username}"><div id="idusername">@${request.username}</div></a>
            </div>
        </div>
        <div class="col-sm">
            <button type="button" class="btn btn-success" onclick="requestAnswer(true,'${request.id_follow}')">Accetta</button>
            <button type="button" class="btn btn-danger" onclick="requestAnswer(false,'${request.id_follow}')">Rifiuta</button>
        </div>
        
        </div>
    </div>
    `
    return s
 }

 const requestAnswer = (answer, id_request) => {
    console.log("Ha risposto con " + answer + " alla richiesta " + id_request)
    fetch("http://localhost:8000/relation/answer", {
       method: "POST",
       headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("token"),
       },
       body: JSON.stringify({
          token: localStorage.getItem("token").split(' ')[1],
          answer: answer,
          id_follow: id_request
       }),
    })
       .then((response) => response.json())
       .then((response) => {
        console.log(response)
          if(response.result){
            console.log("Tutto a buon fine")
            document.getElementById(`id_box_${id_request}`).remove()
          }else{
            alert("Errore nella risposta alla richiesta")
          }

       });
 }