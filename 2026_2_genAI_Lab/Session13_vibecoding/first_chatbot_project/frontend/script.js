let lastBotResponse = "";

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function setStatus(state, label) {
  const wrap = document.querySelector(".topbar__status");
  const el = document.getElementById("status-label");
  if (el) el.textContent = label;
  if (!wrap) return;
  wrap.classList.remove("is-busy", "is-error");
  if (state === "busy") wrap.classList.add("is-busy");
  if (state === "error") wrap.classList.add("is-error");
}

function appendMessage(role, text) {
  const chatBox = document.getElementById("chat-box");
  const isUser = role === "user";
  const label = isUser ? "You" : "Assistant";
  const avatarText = isUser ? "U" : "AI";
  const safe = escapeHtml(text);

  chatBox.innerHTML += `
    <div class="message message--${isUser ? "user" : "assistant"}">
      <div class="message__avatar" aria-hidden="true">${avatarText}</div>
      <div>
        <div class="message__meta">${label}</div>
        <div class="message__bubble">${safe.replace(/\n/g, "<br>")}</div>
      </div>
    </div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("input");
  const btnSend = document.getElementById("btn-send");
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage("user", userMessage);
  input.value = "";
  setStatus("busy", "Thinking…");
  if (btnSend) btnSend.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`Request failed (${response.status})`);
    }

    const data = await response.json();
    lastBotResponse = data.response ?? "";
    appendMessage("assistant", lastBotResponse);
    setStatus("ok", "Ready");
  } catch (e) {
    const msg = "Sorry — something went wrong. Check that the backend is running.";
    lastBotResponse = "";
    appendMessage("assistant", msg);
    setStatus("error", "Error");
  } finally {
    if (btnSend) btnSend.disabled = false;
  }
}

function speakLast() {
  if (!lastBotResponse) return;
  const speech = new SpeechSynthesisUtterance(lastBotResponse);
  speech.lang = "en-US";
  window.speechSynthesis.speak(speech);
}

document.getElementById("input")?.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
