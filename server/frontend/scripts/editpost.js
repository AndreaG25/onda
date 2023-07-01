const params = new URLSearchParams(window.location.search);
const post = params.get('id_post');

//post4edit
const loadPost = () => {
    fetch("http://localhost:8000/post/post4edit", {
      method: "POST",
      headers: {
         Accept: "application/json",
         "Content-Type": "application/json",
         Authorization: localStorage.getItem("token"),
      },
      body: JSON.stringify({
        token: localStorage.getItem("token").split(" ")[1],
        id_post: "post_" + post
      }),
   })
      .then((response) => response.json())
      .then((response) => {  
        console.log(response)  
        if(response.result){
            document.getElementById("idtitle").value = response.data.title
            document.getElementById("idcontent").value = response.data.content
            document.getElementById("idcomment").checked = response.data.comment_flag;
            document.getElementById("idpublic").checked = response.data.public_flag;
        }else{
            document.getElementById("error-msg").innerHTML = response.error
        }
    });
} 

const editPost = () => {
    let title = document.getElementById("idtitle").value
    let content = document.getElementById("idcontent").value
    if(title != '' && content != ''){
        fetch("http://localhost:8000/post/edit", {
            method: "POST",
            headers: {
               Accept: "application/json",
               "Content-Type": "application/json",
               Authorization: localStorage.getItem("token"),
            },
            body: JSON.stringify({
               token: localStorage.getItem("token").split(" ")[1],
               id_post: "post_" + post,
               title: title,
               content: content,
               comment_flag:
                  document.querySelector('input[id="idcomment"]').checked == true,
               public_flag:
                  document.querySelector('input[id="idpublic"]').checked == true,
            }),
        })
            .then((response) => response.json())
            .then((response) => {  
                if(response.result){
                    alert("Post aggiornato correttamente")
                }else{
                    alert("Errore nell'aggionamento del post")
                }
                window.location.replace("./profile.html")
            })
            .catch((error) => {
                console.log("Errore durante la richiesta:", error);
            });
    }else{
        document.getElementById("error-msg").innerHTML = "I campi non possono essere lasciati vuoti"
    }
}

loadPost()