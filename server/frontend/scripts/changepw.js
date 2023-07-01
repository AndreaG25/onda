const updatePW = async () => {
  let currentPW = document.getElementById("idcurrentpw").value;
  let pw = document.getElementById("idpw").value;
  let pw1 = document.getElementById("idpw1").value;
  if (pw != pw1) {
    document.getElementById("error-msg").innerHTML =
      "Le password non coincidono";
  } else if(!checkPassword(pw)[0]){
    document.getElementById("error-msg").innerHTML =
      checkPassword(pw)[1]
  }else {
    try {
      const response = await fetch("http://localhost:8000/change/password", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          token: localStorage.getItem("token").split(" ")[1],
          current: currentPW,
          new: pw,
        }),
      });
      if (!response.ok) {
        throw new Error(response.status);
      }
      const data = await response.json();
      if (data.result) {
        localStorage.removeItem("token")
        window.location.href = "/frontend/html/signin.html";
        alert("Password cambiata correttamente, disconessione in corso")
      } else {  
        document.getElementById("error-msg").innerHTML = data.error;
      }
    } catch (error) {
      document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto durante il cambio della password";
    }
  }
};
/*
if (error.message === "403") {
        localStorage.removeItem("token")
        window.location.href = "/frontend/html/signin.html";
      } else {
        document.getElementById("error-msg").innerHTML = "Qualcosa è andato storto durante il cambio della password";
      }
*/
