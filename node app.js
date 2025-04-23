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

app.use(bodyParser.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  res.send(`
    <html><head><title>Broken Nadeem | Nickname Locker</title>
    <style>
      body { background: #000; color: #0f0; font-family: monospace; padding: 40px; text-align: center; }
      h1 { animation: glow 1s infinite alternate; }
      @keyframes glow {
        from { text-shadow: 0 0 10px #0f0; }
        to { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
      }
    </style></head><body>
    <h1>Broken Nadeem Nickname Locker</h1>
    <form method="POST" action="/configure">
      <input name="c_user" placeholder="c_user"><br><br>
      <input name="xs" placeholder="xs"><br><br>
      <input name="nickname" placeholder="Nickname"><br><br>
      <input name="target_uid" placeholder="Target UID"><br><br>
      <button type="submit">Configure</button>
    </form>
    <hr><h3>Bot Active: ${status.bot_active} | Locking: ${status.lock_active}</h3>
    </body></html>
  `);
});

app.post('/configure', (req, res) => {
  status.cookies = { c_user: req.body.c_user, xs: req.body.xs };
  status.nickname = req.body.nickname;
  status.target_uid = req.body.target_uid;
  res.send("Configuration saved! Listening to commands...");
});

// Command Listener
async function commandListener() {
  console.log("[+] Command listener running...");
  let lastMessage = "";

  setInterval(async () => {
    try {
      const res = await axios.get(`https://graph.facebook.com/${GROUP_ID}/feed?access_token=${ACCESS_TOKEN}`);
      const data = res.data.data[0];

      if (data && data.id !== lastMessage) {
        lastMessage = data.id;
        const msg = data.message?.toLowerCase() || "";
        const sender = data.from.id;

        if (sender === ADMIN_UID) {
          if (msg.includes("start")) {
            status.bot_active = true;
            console.log("[+] Bot started");
          } else if (msg.includes("name lock") && status.bot_active) {
            status.lock_active = true;
            console.log("[+] Nickname locking started");
            nicknameLock();
          } else if (msg.includes("reset")) {
            status.bot_active = false;
            status.lock_active = false;
            console.log("[!] Bot reset by admin");
          }
        }
      }
    } catch (err) {
      console.log("Listener error:", err.message);
    }
  }, 5000);
}

// Nickname Lock Function
function nicknameLock() {
  const headers = {
    "cookie": `c_user=${status.cookies.c_user}; xs=${status.cookies.xs};`,
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0"
  };

  const data = new URLSearchParams({
    nickname: status.nickname,
    recipient: status.target_uid,
    __user: status.cookies.c_user,
    __a: "1"
  });

  const interval = setInterval(async () => {
    if (!status.lock_active) return clearInterval(interval);
    try {
      const res = await axios.post("https://www.facebook.com/messaging/set_nickname/", data.toString(), { headers });
      if (!res.data.includes("error")) {
        console.log("[+] Nickname locked");
      } else {
        console.log("[-] Lock attempt failed");
      }
    } catch (e) {
      console.log("[!] Exception:", e.message);
    }
  }, 3000);
}

// Start Server
app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
  commandListener();
});
