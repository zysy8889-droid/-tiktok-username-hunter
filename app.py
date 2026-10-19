from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(name)

PAGE = “””

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TikTok Username Hunter</title>
<style>
body {
    background: #10131a;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 25px;
}
.box {
    max-width: 500px;
    margin: 30px auto;
    background: #1c2230;
    padding: 25px;
    border-radius: 16px;
}
input, button {
    padding: 13px;
    margin: 8px;
    border: 0;
    border-radius: 8px;
}
button {
    background: #5b7cfa;
    color: white;
    cursor: pointer;
}
#result {
    margin-top: 20px;
    overflow-wrap: anywhere;
}
</style>
</head>
<body>
<div class="box">
<h2>🎯 أداة فحص اليوزرات</h2>
<p>اكتب اسم المستخدم بدون @</p>
<input id="username" placeholder="مثال: q7vx" maxlength="24">
<button onclick="checkUsername()">فحص اليوزر</button>
<div id="result"></div>
</div>
<script>
async function checkUsername() {
    const username = document.getElementById("username").value.trim();
    const result = document.getElementById("result");
if (!/^[A-Za-z0-9._]{2,24}$/.test(username)) {
    result.textContent = "تأكد من كتابة اليوزر بشكل صحيح.";
    return;
}
result.textContent = "جارٍ الفحص...";
try {
    const response = await fetch("/check?username=" + encodeURIComponent(username));
    const data = await response.json();
    result.textContent = data.message;
} catch (error) {
    result.textContent = "تعذر الاتصال. حاول مرة أخرى.";
}

}
</body>
</html>
"""

@app.route(”/”)
def home():
return render_template_string(PAGE)

@app.route(”/check”)
def check_username():
username = request.args.get(“username”, “”).strip()

if not re.fullmatch(r"[A-Za-z0-9._]{2,24}", username):
    return jsonify(message="صيغة اليوزر غير صحيحة.")
try:
    response = requests.get(
        "https://www.tiktok.com/@" + username,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )
    if response.status_code == 404:
        message = "الصفحة غير موجودة، لكن هذا لا يؤكد أن اليوزر متاح."
    elif response.status_code == 200:
        message = "تعذر تأكيد توفر اليوزر آليًا. تحقق من داخل تيك توك."
    else:
        message = "لم نتمكن من تحديد الحالة. حاول لاحقًا."
    return jsonify(message=message)
except requests.RequestException:
    return jsonify(message="تعذر الاتصال بتيك توك حاليًا.")

if name == “main”:
app.run(host=“0.0.0.0”, port=10000)
