from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(
    __name__,
    template_folder="front_end/templates",
    static_folder="front_end/static"
)

# Secret key for session
app.secret_key = "your_secret_key_here"

# Mock Data for destinations
MOCK_DATA = {
    "delhi": {
        "flights": [
            {"name": "IndiGo", "price": "₹3,500", "duration": "2h 15m"},
            {"name": "Vistara", "price": "₹4,200", "duration": "2h 05m"}
        ],
        "buses": [
            {"name": "RedBus", "price": "₹800", "duration": "10h"},
            {"name": "HRTC", "price": "₹650", "duration": "11h"}
        ],
        "trains": [
            {"name": "Shatabdi Express", "price": "₹1,200", "duration": "7h"},
            {"name": "Rajdhani Express", "price": "₹2,500", "duration": "6h"}
        ],
        "hotels": [
            {"name": "The Leela Palace", "rating": "5★", "price": "₹18,000"},
            {"name": "Hotel The Royal Plaza", "rating": "4★", "price": "₹6,000"}
        ],
        "restaurants": [
            {"name": "Bukhara", "cuisine": "North Indian", "price": "₹₹₹"},
            {"name": "Paranthe Wali Gali", "cuisine": "Street Food", "price": "₹"}
        ],
        "destinations": [
            {"name": "India Gate", "type": "Monument"},
            {"name": "Qutub Minar", "type": "UNESCO Site"}
        ]
    }
}

# ----------------------------
# User storage (mock)
# ----------------------------
# For now, we store users in a dict. Replace with DB later
USERS = {}  # key=email, value={"name": name, "password": password}

# -----------------------------------
# Routes
# -----------------------------------

@app.route("/")
def index():
    return render_template("index.html")

# --- Signup Route ---
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if not (name and email and password and confirm_password):
            return render_template("signup.html", error="Please fill all fields")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        if email in USERS:
            return render_template("signup.html", error="Email already registered. Please login.")

        # Store user
        USERS[email] = {"name": name, "password": password}
        return render_template("login.html", success="Signup successful! Please login.")

    return render_template("signup.html")

# --- Login Route ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = USERS.get(email)
        if user and user["password"] == password:
            session["logged_in"] = True
            session["email"] = email
            session["name"] = user["name"]
            return redirect(url_for("planner"))
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

# --- Logout Route ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# --- Planner Route (protected) ---
@app.route("/planner")
def planner():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("planner.html", username=session.get("name"), email=session.get("email"))

# --- Results Route (protected) ---
@app.route("/results")
def results():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    destination = request.args.get("destination", "Unknown")
    results = MOCK_DATA.get(destination.lower(), {})
    return render_template("results.html", destination=destination, results=results)

# --- Optional API Endpoint ---
@app.route("/api/plan")
def api_plan():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    destination = request.args.get("destination", "Unknown").lower()
    import time
    time.sleep(1)  # simulate delay

    data = MOCK_DATA.get(destination, {})
    if not data:
        return jsonify({"error": "No data found for this destination."}), 404

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
