from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

HTML_CODE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Broken Nadeem - Demo FB Reporter</title>
    <style>
        body {
            background: #0d0d0d;
            font-family: 'Courier New', monospace;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #1a1a1a;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 20px red;
            text-align: center;
            width: 320px;
        }
        h2 {
            color: red;
            margin-bottom: 20px;
        }
        input {
            padding: 10px;
            width: 80%;
            border-radius: 8px;
            border: none;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 30px;
            background: red;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        .status {
            margin-top: 20px;
            color: lime;
            font-size: 16px;
        }
        footer {
            margin-top: 30px;
            font-size: 12px;
            color: gray;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Broken Nadeem's Report Tool</h2>
        <form method="POST">
            <input type="text" name="fb_id" placeholder="Enter Facebook ID" required><br>
            <button type="submit">Submit</button>
        </form>
        {% if status %}
        <div class="status">{{ status }}</div>
        {% endif %}
        <footer>Demo UI Only - No real report sent</footer>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    if request.method == "POST":
        fb_id = request.form.get("fb_id")
        time.sleep(1.5)
        status = f"Broken Nadeem ne successfully fake report bhej di ID: {fb_id} pe! (Demo Only)"
    return render_template_string(HTML_CODE, status=status)

if __name__ == "__main__":
    app.run(debug=True)
