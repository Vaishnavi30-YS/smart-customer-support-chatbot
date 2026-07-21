function sendMessage() {

    let input = document.getElementById("user-input");

    let message = input.value.trim();


    if (message === "") {
        return;
    }


    let chatBox = document.getElementById("chat-box");


    // Display user message
    let userMessage = document.createElement("div");

    userMessage.className = "user-message";

    userMessage.innerHTML = message;

    chatBox.appendChild(userMessage);



    input.value = "";



    // Bot typing message

    let typing = document.createElement("div");

    typing.className = "bot-message";

    typing.innerHTML = "🤖 Bot is typing...";

    chatBox.appendChild(typing);



    chatBox.scrollTop = chatBox.scrollHeight;



    // Send message to Flask

    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            message: message

        })

    })



    .then(response => response.json())


    .then(data => {


        setTimeout(() => {


            typing.innerHTML = data.reply;


            chatBox.scrollTop = chatBox.scrollHeight;


        }, 1000);


    })



    .catch(error => {


        typing.innerHTML = "⚠️ Something went wrong.";


        console.log(error);


    });


}





// Press Enter to send

document.getElementById("user-input")
.addEventListener("keypress", function(event) {


    if (event.key === "Enter") {

        sendMessage();

    }


});






// Quick buttons

function sendQuickMessage(message) {


    document.getElementById("user-input").value = message;


    sendMessage();


}
function clearChat(){

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = `
        <div class="bot-message">
            Hello! 👋 How can I help you today?
        </div>
    `;

}