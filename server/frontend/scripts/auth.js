const tryLogin = () => {
   let username = document.getElementById("idusername").value;
   let password = document.getElementById("idpw").value;
   if (genericText(username) && genericText(password)) {
      fetch("http://localhost:8000/auth/login", {
         method: "POST",
         headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            username: username,
            password: password,
         }),
      })
         .then((response) => response.json())
         .then((response) => {
            if (response.result) {
               localStorage.setItem("token", "Bearer " + response.access_token);
               location.reload();
            } else {
               document.getElementById("error-msg").innerHTML = response.error;
            }
         });
   } else {
      document.getElementById("error-msg").innerHTML =
         "Errore nella compilazione dell'input";
   }
};

const trySignup = () => {
   let email = document.getElementById("idmail").value;
   let fullname = document.getElementById("idfullname").value;
   let username = document.getElementById("idusername").value;
   let born_date = document.getElementById("idborndate").value;
   let password = document.getElementById("idpw").value;
   let privacy_account =
      document.querySelector('input[name="accountprivacy"]:checked').value ==
      true;

   document.getElementById("error-msg").innerHTML = "";
   document.getElementById("success-msg").innerHTML = "";
   if (
      document.getElementById("idpw").value !=
      document.getElementById("idpw1").value
   ) {
      document.getElementById("error-msg").innerHTML =
         "Le password non coincidono";
      document.getElementById("idpw").value = "";
      document.getElementById("idpw1").value = "";
   } else {
      let checkForm = validateRegistration(
         email,
         password,
         username,
         born_date,
         fullname
      );
      if (checkForm[0]) {
         fetch("http://localhost:8000/auth/signup", {
            method: "POST",
            headers: {
               Accept: "application/json",
               "Content-Type": "application/json",
            },
            body: JSON.stringify({
               email:email,
               fullname: fullname,
               username: username,
               born_date: born_date,
               password: password,
               privacy_account: privacy_account,
            }),
         })
            .then((response) => response.json())
            .then((response) => {
               console.log(response);
               document.getElementById("success-msg").innerHTML = ''
               document.getElementById("error-msg").innerHTML = ''
               if (response.result) {
                  document.getElementById("success-msg").innerHTML =
                     response.msg;
                  document.getElementById("submitbtn").classList.add("disabled")
               } else {
                  document.getElementById("error-msg").innerHTML =
                     response.error;
               }
            });
      } else {
         document.getElementById("error-msg").innerHTML = checkForm[1][0];
      }
   }
};
