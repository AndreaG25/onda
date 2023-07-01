const formatDateTime = (dateTimeStr) => {
   const dateTime = new Date(dateTimeStr);
   const year = dateTime.getFullYear();
   const month = ("0" + (dateTime.getMonth() + 1)).slice(-2);
   const day = ("0" + dateTime.getDate()).slice(-2);
   const hours = ("0" + dateTime.getHours()).slice(-2);
   const minutes = ("0" + dateTime.getMinutes()).slice(-2);
   return `${day}/${month}/${year} ${hours}:${minutes}`;
};

const verifyToken = (redirectOnValidToken, redirectUrl) => {
   const token = localStorage.getItem("token");
   if (checkTokenRegex(token)) {
      let token2send = token.split(" ")[1];
      fetch("http://localhost:8000/auth/validateToken", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            token: token2send,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            if (response.result && redirectOnValidToken) {
               //Il token è valido e devi reinderizzarmi (/login - /signup rimandano alla home)
               window.location.href = redirectUrl;
            } else if (
               !response.result &&
               window.location.pathname != "/frontend/html/signin.html" &&
               window.location.pathname != "/frontend/html/signup.html" &&
               window.location.pathname != "/frontend/html/change_pw_page.html"
            ) {

               //test--------------------------test
               localStorage.removeItem("token")
               //test--------------------------test
               
               //Il token non è valido e allo stesso tempo non sono nelle schermate di login
               window.location.href = "/frontend/html/signin.html";
            } else if (response.result && !redirectOnValidToken) {
               //il token è valido pero devi stare fermo
               console.log("you logged");
               console.log("Stato dell'utente: " + response.userState)
               manageState(response.userState)

            } else {
               //il token è valido pero devi stare fermo
               console.log("Il token non è valido e siamo in signup/signin");
            }
         });
   } else {
      if (
         window.location.pathname != "/frontend/html/signin.html" &&
         window.location.pathname != "/frontend/html/signup.html" && 
         window.location.pathname != "/frontend/html/changepwrequest.html" &&
         window.location.pathname != "/frontend/html/change_pw_page.html"
      )
         window.location.href = "/frontend/html/signin.html";
   }
};

const checkTokenRegex = (token) => {
   const regex = /^Bearer\s[a-zA-Z0-9._-]+$/i;
   if (token && regex.test(token)) {
      return true;
   } else {
      //localStorage.removeItem('token');
      return false;
   }
};

const getUsernameFromToken = (token) => {
   const tokenParts = token.split(".");
   const encodedPayload = tokenParts[1];
   const decodedPayload = atob(encodedPayload);
   const payloadObj = JSON.parse(decodedPayload);
   return payloadObj.username;
};

const getIDUserFromToken = (token) => {
   const tokenParts = token.split(".");
   const encodedPayload = tokenParts[1];
   const decodedPayload = atob(encodedPayload);
   const payloadObj = JSON.parse(decodedPayload);
   return payloadObj.id_user;
}

const getCurrentTime = () => {
   const date = new Date();

   const year = date.getFullYear().toString().padStart(4, '0');
   const month = (date.getMonth() + 1).toString().padStart(2, '0');
   const day = date.getDate().toString().padStart(2, '0');

   const hours = date.getHours().toString().padStart(2, '0');
   const minutes = date.getMinutes().toString().padStart(2, '0');
   const seconds = date.getSeconds().toString().padStart(2, '0');
   const milliseconds = date.getMilliseconds().toString().padStart(6, '0');

   const dateString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
   return dateString

}
/*
addEventListener("popstate", (event) => {
   console.log("è tornato indietro")
});

onpopstate = (event) => {
   console.log("è tornato indietro")
};*/


 


/*
const getUserState = () => {
   const token = localStorage.getItem("token");
   if (checkTokenRegex(token)) {
      let token2send = token.split(" ")[1];
      fetch("http://localhost:8000/auth/getstate", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("token"),
         },
         body: JSON.stringify({
            token: token2send,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            console.log(response)
            if (response.result) {
               return response.state;
            } else {
               console.log("error nella verifica dello state");
               return 0
            }
         });
   }
};*/

const manageState = (state) => {
   console.log("Stato da gestire: " + state);
   switch (state) {
      case -1:
         localStorage.removeItem("token")
         window.location.href = "/frontend/html/signin.html"
         break;
      case 1:
         if(window.location.pathname != "/frontend/html/notverifiedyet.html"){
            window.location.href = "/frontend/html/notverifiedyet.html";
         }
         break;
      case 2:
         if(window.location.pathname != "/frontend/html/blocked.html" && window.location.pathname != "/frontend/html/notverifiedyet.html"){
            console.log("stato regolare");
         }else{
            window.location.href = "/frontend/html/home.html";
         }
         break;
      case 3:
         if(window.location.pathname != "/frontend/html/blocked.html"){
            window.location.href = "/frontend/html/blocked.html";
         }
         break;
      default:
         console.log("Errore nella gestione dello stato")
   }
};

console.log(Math.floor(Math.random() * 90))