let user = window.prompt("Inserisci il tuo username: ")
let ws = new WebSocket("ws://localhost:6500/ws/" + user);

ws.onmessage = function(event) {
    console.log(event)
    console.log("Notifica ricevuta:", event.data);
    document.getElementById("messages").innerHTML += newNotification(event.data)
    setTimeout(function() {
        document.getElementById("messages").innerHTML = ''
      }, 10000);
};


const newNotification= (data) => {
    let s = `
    <div class="notification" onclick="location.href='./inbox.html';">
        ${data}
    </div>
    `
    return s
}