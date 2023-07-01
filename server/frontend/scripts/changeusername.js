const updateUsername = async () => {
  let username = document.getElementById("idusername").value;
  if(checkUsername(username)[0]){
    try {
      const response = await fetch("http://localhost:8000/change/username", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          token: localStorage.getItem("token").split(" ")[1],
          new: username,
        }),
      });
      if (!response.ok) {
        throw new Error(response.status);
      }
      const data = await response.json();
      console.log(data)
      if (data.result) {
        alert("Username cambiato correttamente, disconessione in corso");
        localStorage.removeItem("token");
        window.location.href = "/frontend/html/logout.html";
      }else{
        document.getElementById("error-msg").innerHTML = data.error;
      }
    } catch (error) {
      
      console.log(error)
    }
  }else{
    document.getElementById("error-msg").innerHTML = checkUsername(username)[1]
  }
  
};
