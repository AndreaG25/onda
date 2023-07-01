const createTicket = async () => {
   let token = localStorage.getItem("token")
   if(!(token)){
      alert("Devi essere loggato per mandare richieste")
   }
    let object = document.getElementById("idobject").value
    let category = document.getElementById("idcategory").value
    let content = document.getElementById("idcontent").value
    if(object != '' && content != ''){
       try {
        //capire quale route dare a questa funzione
          const response = await fetch("http://localhost:8000/support/createticket", {
             method: "POST",
             headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: localStorage.getItem("token"),
             },
             body: JSON.stringify({
                token: localStorage.getItem("token").split(" ")[1],
                subject: object,
                content: content,
                category: category
             }),
          });
          if (!response.ok) {
             throw new Error(response.status);
          }
          const data = await response.json();
          if (data.result) {
               alert("Ticket aggiunto correttamente");
             window.location.href = "/frontend/html/home.html";
          } else {
             document.getElementById("error-msg").innerHTML = data.error;
          }
       } catch (error) {
          document.getElementById("error-msg").innerHTML = 
             "Qualcosa è andato storto durante l'aggiunta del ticket";
       }
    }
    else{
       document.getElementById("error-msg").innerHTML = "I campi non possono essere lasciati vuoti"
    }
 };
 