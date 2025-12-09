let socket = null;
let currentUser = null;

// -------------------------------
// API CALLS: REGISTER + LOGIN
// -------------------------------

async function registerUser(username, password) {
    const res = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    return await res.json();
}

async function loginUser(username, password) {
    const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    return await res.json();
}


// -------------------------------
// CONNECT TO WEBSOCKET
// -------------------------------

function connectWebSocket(username) {
    socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
        socket.send(JSON.stringify({ username }));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        const box = document.createElement("div");
        box.className = "message";

        if (data.type === "system") {
            box.innerHTML = `<span class="system">${data.message}</span>`;
        } 
        else if (data.type === "chat") {
            box.innerHTML = `
                <span class="username">${data.username}</span>
                <span class="text">${data.message}</span>
            `;
        }

        messages.appendChild(box);
        messages.scrollTop = messages.scrollHeight;
    };
}


// -------------------------------
// SEND MESSAGE (ENTER + BUTTON)
// -------------------------------

function sendMessage() {
    const text = msgInput.value.trim();
    if (!text) return;

    socket.send(JSON.stringify({
        username: currentUser,
        message: text
    }));

    msgInput.value = "";
}

sendBtn.onclick = sendMessage;

msgInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") sendMessage();
});


// -------------------------------
// LOGIN / SIGNUP UI HANDLING
// -------------------------------

let mode = "login";

loginTab.onclick = () => {
    mode = "login";
    loginTab.classList.add("active");
    signupTab.classList.remove("active");

    msg.className = "";
    msg.innerText = "";

    actionBtn.innerText = "Login";
};

signupTab.onclick = () => {
    mode = "signup";
    signupTab.classList.add("active");
    loginTab.classList.remove("active");

    msg.className = "";
    msg.innerText = "";

    actionBtn.innerText = "Create Account";
};


// -------------------------------
// MAIN LOGIN / SIGNUP ACTION BUTTON
// -------------------------------

actionBtn.onclick = async () => {
    const u = username.value.trim();
    const p = password.value.trim();

    if (!u || !p) {
        msg.className = "error";
        msg.innerText = "Fill all fields";
        return;
    }

    // ----------------------
    // SIGNUP
    // ----------------------
    if (mode === "signup") {
        const res = await registerUser(u, p);

        if (!res.ok) {
            msg.className = "error";
            msg.innerText = res.msg;
            return;
        }

        msg.className = "success";
        msg.innerText = res.msg; // "Account created"
        return;
    }

    // ----------------------
    // LOGIN
    // ----------------------
    if (mode === "login") {
        const res = await loginUser(u, p);

        if (!res.ok) {
            msg.className = "error";
            msg.innerText = res.msg;
            return;
        }

        msg.className = "success";
        msg.innerText = "Login successful!";

        currentUser = u;

        // show chat
        authBox.classList.add("hidden");
        chat.classList.remove("hidden");
        chatTitle.innerText = "Welcome " + u;

        connectWebSocket(u);
    }
};
