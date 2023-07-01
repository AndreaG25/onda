const newPost = async () => {
   let title = document.getElementById("idtitle").value
   let content = document.getElementById("idcontent").value
   if(title != '' && content != ''){
      try {
         const response = await fetch("http://localhost:8000/post/new", {
            method: "POST",
            headers: {
               Accept: "application/json",
               "Content-Type": "application/json",
               Authorization: localStorage.getItem("token"),
            },
            body: JSON.stringify({
               token: localStorage.getItem("token").split(" ")[1],
               title: title,
               content: content,
               comment_flag:
                  document.querySelector('input[id="idcomment"]').checked == true,
               public_flag:
                  document.querySelector('input[id="idpublic"]').checked == true,
            }),
         });
         if (!response.ok) {
            throw new Error(response.status);
         }
         const data = await response.json();
         if (data.result) {
            window.location.href = "/frontend/html/home.html";
            alert("Post aggiunto correttamente");
         } else {
            document.getElementById("error-msg").innerHTML = data.error;
         }
      } catch (error) {
         document.getElementById("error-msg").innerHTML =
            "Qualcosa è andato storto durante l'aggiunta del post";
      }
   }
   else{
      document.getElementById("error-msg").innerHTML = "I campi non possono essere lasciati vuoti"
   }
};
