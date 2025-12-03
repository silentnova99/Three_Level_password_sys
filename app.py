from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import get_db_connection
import random
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global dictionary to store OTPs temporarily for Level 2 (demo purposes)
otp_store = {}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template("register.html", error="Username already exists")

        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        conn.commit()
        cur.close()
        conn.close()
        flash("Registration successful! Please login.")
        return redirect(url_for("level1"))

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/level1", methods=["GET", "POST"])
def level1():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            return redirect(url_for("level2"))
        else:
            return render_template("level1.html", error="Invalid username or password")

    return render_template("level1.html")


@app.route("/level2", methods=["GET", "POST"])
def level2():
    if "user_id" not in session:
        return redirect(url_for("level1"))

    if request.method == "POST":
        email = request.form["email"]
        otp = request.form.get("otp")

        if otp:
            # User submitted OTP; verify it
            user_otp = otp_store.get(session["user_id"])
            if user_otp == otp:
                # OTP validated, cleanup and move to level 3
                otp_store.pop(session["user_id"], None)
                return redirect(url_for("level3"))
            else:
                return render_template("level2.html", email=email, error="Invalid OTP")
        else:
            # First time on level 2, user enters email; generate OTP
            if email == session["email"]:
                generated_otp = str(random.randint(100000, 999999))
                otp_store[session["user_id"]] = generated_otp
                # In real, send OTP via email. Here, show on screen for demo
                return render_template("level2.html", email=email, otp=generated_otp)
            else:
                return render_template("level2.html", error="Email does not match registered email")

    # GET request or first time load
    return render_template("level2.html", email="")


@app.route("/level3", methods=["GET", "POST"])
def level3():
    if "user_id" not in session:
        return redirect(url_for("level1"))

    # Only generate the QR code and code if it's not already in session
    if request.method == "GET" or "level3_code" not in session:
        code_digits = [str(random.randint(0,9)) for _ in range(3)]
        code_str = "".join(code_digits)
        session["level3_code"] = code_str

        qr_data = f"Your authentication code: {code_str}"
        qr = qrcode.make(qr_data)
        img_buf = io.BytesIO()
        qr.save(img_buf)
        img_buf.seek(0)
        qr_base64 = base64.b64encode(img_buf.getvalue()).decode()
        session["qr_base64"] = qr_base64
    else:
        code_str = session.get("level3_code")
        qr_base64 = session.get("qr_base64")

    if request.method == "POST":
        user_code = request.form.get("code")
        if user_code == code_str:
            session.pop("level3_code", None)
            session.pop("qr_base64", None)
            return redirect(url_for("dashboard"))
        else:
            error = "Incorrect code entered. Please scan QR code and enter correct code."
            return render_template("level3.html", qr_code=qr_base64, error=error)

    return render_template("level3.html", qr_code=qr_base64)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("level1"))
    return render_template("dashboard.html", username=session.get("username"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("level1"))


if __name__ == "__main__":
    app.run(debug=True)
