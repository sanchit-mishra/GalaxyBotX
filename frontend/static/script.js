// script.js
function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const chatLog = document.getElementById("chatLog");

    fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        chatLog.innerHTML += `<div style="border-radius: 20px;height: auto;overflow-y: auto;margin-bottom: 10px;border: 1px solid #ddd;padding: 10px;border-radius: 4px;background-color: #5896EB; color:#ffffff"><b>You:</b> ${userInput}</div>`;
        const botMessage = data.message ? data.message : data;
        chatLog.innerHTML += `<div style="border-radius: 20px;height: auto;overflow-y: auto;margin-bottom: 10px;border: 1px solid #ddd;padding: 10px;border-radius: 4px;background-color: #ffffff; "><b>Galaxy BotX:</b> ${botMessage}</div>`;
        document.getElementById("userInput").value = "";  // Clear input field
    });
}
