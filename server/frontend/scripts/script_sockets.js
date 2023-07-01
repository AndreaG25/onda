let token = localStorage.token.split(' ')[1]
let ws = new WebSocket("ws://localhost:6500/ws/" + token);
console.log(ws)

ws.onmessage = function(event) {
    console.log(event)
    console.log("Notifica ricevuta:", event.data);
    let c = event.data
    if (event.data[0] == "#") {
        c = c.slice(1);
      document.getElementById("messages").innerHTML += newNotification(c);
      setTimeout(function () {
         document.getElementById("messages").innerHTML = "";
      }, 10000);
   }
};

/*
window.addEventListener('beforeunload', function() {
    ws.close()
});*/

const newNotification= (data) => {
    let s = `
    <div class="notification" onclick="location.href='./inbox.html';">
        ${data}
    </div>
    `
    return s
}