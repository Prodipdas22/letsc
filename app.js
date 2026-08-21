const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const chat = document.getElementById("chat");
const themeBtn = document.getElementById("themeBtn");

// Change this after deploying your backend
const API_URL = "https://letsc-lteq.onrender.com/chat";


// Send message
async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");

    input.value = "";

    const loadingMessage = addMessage(
        "Thinking... 🤔",
        "ai"
    );

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        loadingMessage.remove();

        if (data.success && data.answer) {

    addMessage(data.answer, "ai");

} else {

    addMessage(
        "⚠️ LETSC Error:\n" +
        JSON.stringify(data, null, 2),
        "ai"
    );

    console.error("LETSC API response:", data);
        }

    } catch (error) {

        loadingMessage.remove();

        addMessage(
            "Unable to connect to the LETSC AI server.",
            "ai"
        );

        console.error(error);
    }
}


// Add message
function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    if (type === "user") {

        message.innerHTML = `
            <div class="bubble">
                <p>${escapeHTML(text)}</p>
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="bubble">
                <strong>LETSC AI</strong>
                <p>${escapeHTML(text)}</p>
            </div>
        `;

    }

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;

    return message;
}


// Prevent HTML injection
function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Suggestions
function useSuggestion(text) {

    input.value = text;

    input.focus();
}


// Send button
sendBtn.addEventListener("click", sendMessage);


// Enter to send
input.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});


// Dark mode
themeBtn.addEventListener("click", function() {

    document.body.classList.toggle("dark");

    themeBtn.textContent =
        document.body.classList.contains("dark")
            ? "☀️"
            : "🌙";

});
