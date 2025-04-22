from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Termux Token Extractor - Broken Nadeem</title>
    <style>
        body {
            background:#000; color:#0f0; font-family:monospace; padding:30px;
        }
        textarea, input { width:100%; padding:10px; background:#111; color:#0f0; border:1px solid #0f0; }
        button { background:#0f0; color:#000; padding:10px 20px; margin-top:10px; cursor:pointer; font-weight:bold; }
        .box { background:#111; padding:20px; margin-top:20px; border:1px solid #0f0; }
    </style>
</head>
<body>
    <h1>Broken Nadeem - Token Extractor (Termux)</h1>
    <form method="POST">
        <label>Paste Facebook Cookies:</label><br>
        <textarea name="cookie" rows="6" required></textarea><br>
        <button type="submit">Extract Token</button>
    </form>

    {% if token %}
    <div class="box">
        <h3>Token Found:</h3>
        <textarea rows="3">{{ token }}</textarea>
    </div>
    {% elif error %}
    <div class="box" style="color:red;">
        <h3>Error:</h3>
        <p>{{ error }}</p>
    </div>
    {% endif %}
</body>
</html>
'''

def extract_token(cookie):
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0"
    }
    try:
        response = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token_match = re.search(r'EAAG\w+', response.text)
        if token_match:
            return token_match.group(0)
        else:
            raise Exception("Token not found. Invalid cookie or checkpointed account.")
    except Exception as e:
        raise e

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    error = None
    if request.method == 'POST':
        cookie = request.form.get("cookie")
        try:
            token = extract_token(cookie)
        except Exception as e:
            error = str(e)
    return render_template_string(HTML, token=token, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
