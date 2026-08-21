const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const chat = document.getElementById("chat");
const themeBtn = document.getElementById("themeBtn");

// Send message
function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    // Add user message
    addMessage(text, "user");

    input.value = "";

    // Temporary AI response
    setTimeout(() => {

        addMessage(
            "I received your request. AI connection will be added in the next step. 🚀",
            "ai"
        );

    }, 500);
}


// Add message to chat
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
}


// Prevent HTML injection
function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Suggestion buttons
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

    if (document.body.classList.contains("dark")) {

        themeBtn.textContent = "☀️";

    } else {

        themeBtn.textContent = "🌙";

    }

});
