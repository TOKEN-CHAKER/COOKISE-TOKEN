const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();

const ADMIN_UID = "61573436296849";
const GROUP_ID = "<YOUR_GROUP_ID>"; // Replace with your group ID
const ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"; // Replace with your group access token

let status = {
    bot_active: false,
    lock_active: false,
    nickname: "",
    target_uid: "",
    cookies: {}
};

app.use(bodyParser.urlencoded({ extended: true }));

const HTML_TEMPLATE = `
<!DOCTYPE html><html>
<head>
    <title>Broken Nadeem | Animated Nickname Locker</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            padding: 40px;
        }
        h1, h3 {
            animation: glow 1s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #0f0; }
            to { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
        }
        .status {
            margin-top: 20px;
            font-size: 20px;
            color: cyan;
        }
    </style>
</head>
<body>
    <h1>Broken Nadeem Nickname Worm Locker</h1>
    <div class="status">
        <p>Bot Active: {{bot_active}}</p>
        <p>Locking: {{lock_active}}</p>
        <p>Target UID: {{target_uid}}</p>
        <p>Nickname: {{nickname}}</p>
    </div>
</body>
</html>
`;

app.get('/', (req, res) => {
    const filledTemplate = HTML_TEMPLATE
        .replace('{{bot_active}}', status.bot_active)
        .replace('{{lock_active}}', status.lock_active)
        .replace('{{target_uid}}', status.target_uid)
        .replace('{{nickname}}', status.nickname);
    res.send(filledTemplate);
});

app.post('/configure', (req, res) => {
    status.cookies = {
        c_user: req.body.c_user,
        xs: req.body.xs
    };
    status.nickname = req.body.nickname;
    status.target_uid = req.body.target_uid;
    res.send("Configured!");
});

async function setNickname() {
    const headers = {
        'cookie': `c_user=${status.cookies.c_user}; xs=${status.cookies.xs};`,
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10)'
    };

    const data = new URLSearchParams({
        nickname: status.nickname,
        recipient: status.target_uid,
        __user: status.cookies.c_user,
        __a: '1'
    });

    while (status.lock_active) {
        try {
            const response = await axios.post("https://www.facebook.com/messaging/set_nickname/", data, { headers });
            if (!response.data.includes("error")) {
                console.log("[+] Nickname Locked Successfully");
            } else {
                console.log("[-] Nickname lock attempt failed");
            }
        } catch (e) {
            console.log("[!] Exception: " + e.message);
        }
        await new Promise(r => setTimeout(r, 2000));
    }
}

async function commandListener() {
    console.log("[+] Command listener started");
    const url = `https://graph.facebook.com/${GROUP_ID}/feed?access_token=${ACCESS_TOKEN}`;
    let last_checked = "";

    while (true) {
        try {
            const res = await axios.get(url);
            const data = res.data.data;
            if (data && data.length > 0) {
                const latest = data[0];
                if (latest.id !== last_checked) {
                    last_checked = latest.id;
                    const message = (latest.message || "").toLowerCase();
                    const sender = latest.from?.id || "";

                    if (sender === ADMIN_UID) {
                        if (message.includes("start")) {
                            status.bot_active = true;
                            console.log("[+] Bot started");
                        } else if (message.includes("name lock") && status.bot_active) {
                            status.lock_active = true;
                            console.log("[*] Nickname locking initiated");
                            setNickname();
                        } else if (message.includes("reset")) {
                            status.bot_active = false;
                            status.lock_active = false;
                            console.log("[!] System reset by admin");
                        }
                    }
                }
            }
        } catch (e) {
            console.log("[!] Listener error: " + e.message);
        }
        await new Promise(r => setTimeout(r, 5000));
    }
}

app.listen(5000, () => {
    console.log("Server running on http://0.0.0.0:5000");
    commandListener();
});
