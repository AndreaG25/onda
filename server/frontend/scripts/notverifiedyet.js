const sendNewEmail = () => {
    fetch("http://localhost:8000/auth/newemail", {
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
         if (response.result) {
            document.getElementById("result").innerHTML = response.msg;
         }
      });
}