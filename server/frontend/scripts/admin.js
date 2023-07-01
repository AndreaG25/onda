let tickets = []
const tryAdminLogin = () => {
   let username = document.getElementById("idusername").value;
   let password = document.getElementById("idpw").value;
   if (username && password) {
      fetch("http://localhost:7000/login", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
         },
         body: JSON.stringify({ username: username, password: password }),
      })
         .then((response) => response.json())
         .then((response) => {
            if (response.result === true) {
               localStorage.setItem("admin_token", "Bearer " + response.access_token);
               window.location.reload();
            } else {
               document.getElementById("error-msg").innerHTML = response.result;
            }
         });
   }
};

const checkToken = () => {
   let token = localStorage.admin_token;
   if (token) {
      token = token.split(" ")[1];
      //localhost/admin/login
      fetch("http://localhost:7000/validateadmintoken", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
         },
         body: JSON.stringify({ token: token }),
      })
         .then((response) => response.json())
         .then((response) => {
            if (response.result) {
               if (window.location.pathname != "/frontend/html/admin/adminpanel.html" && window.location.pathname == "/frontend/html/admin/signinadmin.html") {
                  window.location.href = "./adminpanel.html";
               }
            } else {
               if (
                  window.location.pathname != "/frontend/html/admin/signinadmin.html"
               ) {
                  window.location.href = "./signinadmin.html";
               }
            }
         });
   }else{
      if (
         window.location.pathname != "/frontend/html/admin/signinadmin.html"
      ) {
         window.location.href = "./signinadmin.html";
      }
   }
};

const getAllUsers = () => {
   fetch("http://localhost:7000/users", {
      method: "GET",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("admin_token"),
      },
   })
      .then((response) => response.json())
      .then((response) => {
         response.result.forEach(element => {
            document.getElementById("table-body").innerHTML += generateUserTableRow(element)
         });
      });
};

const generateUserTableRow = (user) => {
   let row = '<tr>' +
       '<td>' + user.id_user + '</td>' +
       '<td>' + user.username + '</a></td>' +
       '<td>' + user.email + '</td>' +
       '<td>' + user.num_posts + '</td>' +
       '<td>' + user.num_comments + '</td>' +
       '<td>' + user.state + '</td>' +
       '<td>' + formatDate(user.registration_date) + '</td>' +
       '<td>' + generaAzione(user.state, user.id_user) + '</td>' +
       '</tr>';
   return row;
}

const formatDate = (dateString) => {
   let date = new Date(dateString);
   
   let month = date.getMonth() + 1;
   let day = date.getDate();
   let year = date.getFullYear();
   
   return month + '-' + day + '-' + year;
}

const generaAzione = (state, id_user) => {
   let stateMsg = ""
   if(state == 1){
      stateMsg = "Abilita l'utente"
   }else if(state == 2){
      stateMsg = "Blocca utente"
   }else if(state == 3){
      stateMsg = "Sblocca utente"
   }
   let button = `<button type="button" class="btn btn-primary" onclick="editUser(${state}, '${id_user}')">${stateMsg}</button>`
   return button
}

const editUser = (state, id_user) => {
   fetch("http://localhost:7000/edituser", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("admin_token"),
      },
      body: JSON.stringify({
         state: state,
         id_user: id_user
      })
   })
      .then((response) => response.json())
      .then((response) => {
         if(response.result){
            window.location.reload()
         }else{
            alert("Errore nel cambio dello stato")
            window.location.reload()
         }
      });
}

const getAllTickets = () => {
   fetch("http://localhost:7000/tickets", {
      method: "GET",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("admin_token"),
      },
   })
      .then((response) => response.json())
      .then((response) => {
         tickets = response.result
         showTickets(0)
      });
}

const generateTicketTableRow = (message) => {
   let categoryWord = ''
   switch(message.category){
      case 1:
         categoryWord = "Assistenza clienti"
         break
      case 2:
         categoryWord = "Problemi tecnici"
         break
      case 3:
         categoryWord = "Richiesta di informazioni"
         break
      case 4:
         categoryWord = "Reclami"
         break
      case 5:
         categoryWord = "Feedback"
         break
      default:
         categoryWord = "Errore nella categoria"
   }

   let button = `<button class="btn btn-primary" onclick="createAnswerForm('${message.id_ticket}')">Rispondi</button>`
   if(message.answer == 1){
      button = `<button class="btn btn-primary disabled">Rispondi</button>`
   }
   let row = 
   '<tr>' +
       '<td>@' + message.username + '</a></td>' +
       `<td>${categoryWord}</td>` +
       '<td>' + message.subject + '</td>' +
       '<td>' + message.content + '</td>' +
       `<td>${button}</td>` +
       '</tr>';
   return row;
}

const showTickets = (action) => {
   document.getElementById("table-body").innerHTML = ''
   let tickets_copy = tickets
   if(action == 1){
      tickets_copy = filterByAnswer(tickets_copy, 0)
   }else if(action == 2){
      tickets_copy = filterByAnswer(tickets_copy, 1)
   }
   tickets_copy = sortByDate(tickets_copy)
   tickets_copy.forEach(element => {
      document.getElementById("table-body").innerHTML += generateTicketTableRow(element)
   });
}

const sortByDate = (array) => {
   array.sort(function(a, b) {
     const dateA = new Date(a.creation_date);
     const dateB = new Date(b.creation_date);
     return dateB - dateA;
   });
   return array;
}
 
const filterByAnswer = (array, valore) => {
   return array.filter(function(item) {
     return item.answer == valore;
   });
}

const filterByCategory = (array, category) => {
   return array.filter(function(item) {
     return item.category == category;
   });
}
 
const createAnswerForm = (id_ticket) => {
   document.getElementById("idanswerform").innerHTML = ''
   document.getElementById("idanswerform").innerHTML = `
   <div class="form-group">
      <label for="id_textarea_${id_ticket}">Risposta:</label>
      <textarea class="form-control bg-transparent" id="id_textarea_${id_ticket}" rows="3"></textarea>
      <button type="submit" class="btn btn-primary" style="margin-top: 15px;" onclick="answerTicket('${id_ticket}')">Rispondi</button>
   </div>
   `
}

const answerTicket = (id_ticket) => {
   let response = document.getElementById(`id_textarea_${id_ticket}`).value 
   if(response){
      fetch("http://localhost:7000/answerTicket", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("admin_token"),
      },
      body: JSON.stringify({
         id_ticket: id_ticket,
         res: response
      })
      })
      .then((response) => response.json())
      .then((response) => {
         if(response.result){
            alert("Risposta inviata con successo")
         }else{
            alert("Errore nell'invio della risposta")
         }
         window.location.reload()
      });
   }
}


const show4category = (category) => {
   document.getElementById("table-body").innerHTML = ''
   let tickets_copy = tickets
   tickets_copy = filterByCategory(tickets_copy, category)
   tickets_copy.forEach(element => {
      document.getElementById("table-body").innerHTML += generateTicketTableRow(element)
   });
}