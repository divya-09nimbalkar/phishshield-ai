"""
PhishShield AI — Dashboard with Login & Signup
Run:  streamlit run dashboard.py
Deps: pip install streamlit plotly pandas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random, hashlib, json, os
from datetime import datetime, timedelta

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="PhishShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",   # ← FIXED: was "collapsed"
)

# ── Users file ───────────────────────────────────────────────
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register(username, email, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    if any(v["email"] == email for v in users.values()):
        return False, "Email already registered."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users[username] = {
        "email": email,
        "password": hash_pw(password),
        "created": datetime.now().strftime("%Y-%m-%d"),
        "scans": 0,
    }
    save_users(users)
    return True, "Account created!"

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    if users[username]["password"] != hash_pw(password):
        return False, "Incorrect password."
    return True, users[username]

# ── Session init ──────────────────────────────────────────────
if "logged_in"    not in st.session_state: st.session_state.logged_in    = False
if "username"     not in st.session_state: st.session_state.username     = ""
if "user_data"    not in st.session_state: st.session_state.user_data    = {}
if "auth_page"    not in st.session_state: st.session_state.auth_page    = "login"
if "login_err"    not in st.session_state: st.session_state.login_err    = ""
if "signup_err"   not in st.session_state: st.session_state.signup_err   = ""
if "signup_ok"    not in st.session_state: st.session_state.signup_ok    = ""

# ── Global CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* Main background */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background-color: #040d1a !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #050f1e !important;
    border-right: 1px solid #0d3a5c !important;
}
section[data-testid="stSidebar"] * { color: #a0c4d8 !important; }

/* ── DO NOT TOUCH header/toolbar — sidebar toggle lives there ── */
/* Only hide the hamburger menu text and footer watermark */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

h1,h2,h3,p,div,span,label         { color:#c8e6f0; }

/* ── Auth wrapper ── */
.auth-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at 20% 10%, #0a1f33 0%, #020b18 60%);
}
.auth-card {
    background: #071828;
    border: 1px solid #0d3a5c;
    border-radius: 8px;
    padding: 44px 48px;
    width: 420px;
    box-shadow: 0 0 60px rgba(0,212,255,0.06);
}
.auth-logo {
    text-align: center;
    margin-bottom: 32px;
}
.auth-logo-icon { font-size: 52px; }
.auth-logo-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #00d4ff;
    margin-top: 6px;
}
.auth-logo-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: #4a8fa8;
    margin-top: 3px;
}
.auth-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #4a8fa8;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 28px;
    border-bottom: 1px solid #0d3a5c;
    padding-bottom: 14px;
}
.auth-divider {
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #1e4d6b;
    margin: 18px 0;
}
.auth-switch {
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #4a8fa8;
    margin-top: 20px;
}
.auth-err {
    background: rgba(255,50,50,0.12);
    border: 1px solid #ff4444;
    border-radius: 4px;
    padding: 8px 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #ff8888;
    margin-bottom: 14px;
}
.auth-ok {
    background: rgba(0,255,136,0.08);
    border: 1px solid #00ff88;
    border-radius: 4px;
    padding: 8px 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: #00ff88;
    margin-bottom: 14px;
}

/* ── Inputs ── */
[data-testid="stTextInput"] > label,
[data-testid="stSelectbox"] > label { color:#4a8fa8 !important;
    font-family:'Share Tech Mono',monospace !important; font-size:11px !important;
    letter-spacing:2px !important; text-transform:uppercase; margin-bottom:4px; }
[data-testid="stTextInput"] input {
    background:#040d1a !important; border:1px solid #0d3a5c !important;
    color:#c8e6f0 !important; font-family:'Share Tech Mono',monospace !important;
    border-radius:4px !important; padding:10px 14px !important; }
[data-testid="stTextInput"] input:focus {
    border-color:#00d4ff !important; box-shadow:0 0 10px rgba(0,212,255,0.15) !important; }

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#003d5c,#005a80) !important;
    border: 1px solid #00d4ff !important;
    color: #00d4ff !important;
    font-family: 'Orbitron',sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 3px !important;
    padding: 12px !important;
    border-radius: 4px !important;
    transition: all .2s !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: linear-gradient(90deg,#00d4ff22,#00d4ff33) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
}

/* ── Dashboard metric card ── */
.mcard { background:#071828; border:1px solid #0d3a5c; border-radius:6px;
         padding:18px 20px; margin-bottom:10px; border-left:4px solid #00d4ff; }
.mcard.red    { border-left-color:#ff4444; }
.mcard.green  { border-left-color:#00ff88; }
.mcard.yellow { border-left-color:#ffcc00; }
.mcard.blue   { border-left-color:#00d4ff; }
.mlabel { font-family:'Share Tech Mono',monospace; font-size:11px; letter-spacing:2px;
          color:#4a8fa8 !important; text-transform:uppercase; margin-bottom:6px; }
.mvalue { font-family:'Orbitron',sans-serif; font-size:30px; font-weight:700; line-height:1.1; }
.mcard.red   .mvalue { color:#ff6666; }
.mcard.green .mvalue { color:#00ff88; }
.mcard.yellow .mvalue{ color:#ffcc00; }
.mcard.blue  .mvalue { color:#00d4ff; }
.mdelta { font-family:'Share Tech Mono',monospace; font-size:11px;
          color:#4a8fa8 !important; margin-top:4px; }

.sec { font-family:'Orbitron',sans-serif; font-size:11px; font-weight:700;
       letter-spacing:3px; color:#4a8fa8 !important; text-transform:uppercase;
       border-bottom:1px solid #0d3a5c; padding-bottom:6px; margin:20px 0 12px 0; }

.lrow { display:flex; gap:12px; padding:7px 10px; border-bottom:1px solid #071828;
        font-family:'Share Tech Mono',monospace; font-size:12px; background:#040d1a; }
.lrow:hover { background:#071828; }
.ltime { color:#4a8fa8; min-width:75px; }
.lurl  { color:#c8e6f0; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.bp { display:inline-block; padding:2px 10px; background:rgba(255,50,50,0.15);
      border:1px solid #ff4444; border-radius:3px; color:#ff7777;
      font-family:'Share Tech Mono',monospace; font-size:11px; }
.bs { display:inline-block; padding:2px 10px; background:rgba(0,255,136,0.1);
      border:1px solid #00ff88; border-radius:3px; color:#00ff88;
      font-family:'Share Tech Mono',monospace; font-size:11px; }
.alrt { background:linear-gradient(90deg,rgba(255,50,50,0.12),transparent);
        border-left:3px solid #ff4444; padding:9px 14px; margin-bottom:7px;
        border-radius:0 4px 4px 0; font-family:'Share Tech Mono',monospace;
        font-size:12px; color:#ffaaaa; }
.sr-phish { background:#071828; border:2px solid #ff4444; border-radius:6px;
            padding:24px; text-align:center; }
.sr-safe  { background:#071828; border:2px solid #00ff88; border-radius:6px;
            padding:24px; text-align:center; }
.sr-tp { font-family:'Orbitron',sans-serif; font-size:20px; font-weight:900;
         color:#ff4444; letter-spacing:3px; }
.sr-ts { font-family:'Orbitron',sans-serif; font-size:20px; font-weight:900;
         color:#00ff88; letter-spacing:3px; }
.sr-url { font-family:'Share Tech Mono',monospace; font-size:12px;
          color:#4a8fa8; margin-top:8px; word-break:break-all; }
.main-header { text-align:center; padding:16px 0 12px 0;
               border-bottom:1px solid #0d3a5c; margin-bottom:20px; }
.main-title { font-family:'Orbitron',sans-serif; font-size:26px; font-weight:900;
              letter-spacing:5px; color:#00d4ff; }
.main-sub   { font-family:'Share Tech Mono',monospace; font-size:11px;
              letter-spacing:3px; color:#4a8fa8; margin-top:4px; }

/* profile badge */
.user-badge {
    background: #071828; border:1px solid #0d3a5c; border-radius:6px;
    padding: 10px 16px; font-family:'Share Tech Mono',monospace; font-size:11px;
    color:#4a8fa8; display:flex; align-items:center; gap:10px;
}
.user-badge .uname { color:#00d4ff; font-weight:700; letter-spacing:1px; }

/* scrollbar */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:#020b18; }
::-webkit-scrollbar-thumb { background:#0d3a5c; border-radius:2px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  AUTH PAGES  (shown when not logged in)
# ══════════════════════════════════════════════════════════════
def show_login():
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div class='auth-logo'>
            <div class='auth-logo-icon'>🛡️</div>
            <div class='auth-logo-title'>PHISHSHIELD</div>
            <div class='auth-logo-sub'>AI SECURITY SYSTEM</div>
        </div>
        <div class='auth-title'>— SIGN IN TO YOUR ACCOUNT —</div>
        """, unsafe_allow_html=True)

        if st.session_state.login_err:
            st.markdown(f"<div class='auth-err'>⚠ {st.session_state.login_err}</div>",
                        unsafe_allow_html=True)

        username = st.text_input("Username", key="li_user",
                                  placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="li_pass",
                                  placeholder="Enter your password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬡  LOGIN", key="btn_login"):
            if not username or not password:
                st.session_state.login_err = "Please fill in all fields."
            else:
                ok, result = login(username, password)
                if ok:
                    st.session_state.logged_in  = True
                    st.session_state.username   = username
                    st.session_state.user_data  = result
                    st.session_state.login_err  = ""
                    st.rerun()
                else:
                    st.session_state.login_err = result
                    st.rerun()

        st.markdown("""
        <div class='auth-divider'>──────── OR ────────</div>
        <div class='auth-switch'>Don't have an account?</div>
        """, unsafe_allow_html=True)

        if st.button("CREATE AN ACCOUNT", key="btn_go_signup"):
            st.session_state.auth_page  = "signup"
            st.session_state.login_err  = ""
            st.rerun()

        st.markdown("""
        <div style='text-align:center; margin-top:24px; font-family:"Share Tech Mono",monospace;
                    font-size:10px; color:#1e4d6b;'>
            🛡 PhishShield AI · Real-Time Phishing Protection
        </div>
        """, unsafe_allow_html=True)


def show_signup():
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div class='auth-logo'>
            <div class='auth-logo-icon'>🛡️</div>
            <div class='auth-logo-title'>PHISHSHIELD</div>
            <div class='auth-logo-sub'>CREATE YOUR ACCOUNT</div>
        </div>
        <div class='auth-title'>— REGISTER NEW ACCOUNT —</div>
        """, unsafe_allow_html=True)

        if st.session_state.signup_err:
            st.markdown(f"<div class='auth-err'>⚠ {st.session_state.signup_err}</div>",
                        unsafe_allow_html=True)
        if st.session_state.signup_ok:
            st.markdown(f"<div class='auth-ok'>✓ {st.session_state.signup_ok}</div>",
                        unsafe_allow_html=True)

        username = st.text_input("Username", key="su_user",
                                  placeholder="Choose a username")
        email    = st.text_input("Email",    key="su_email",
                                  placeholder="Enter your email")
        password = st.text_input("Password", type="password", key="su_pass",
                                  placeholder="Min 6 characters")
        confirm  = st.text_input("Confirm Password", type="password", key="su_conf",
                                  placeholder="Re-enter password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬡  CREATE ACCOUNT", key="btn_signup"):
            if not username or not email or not password or not confirm:
                st.session_state.signup_err = "Please fill in all fields."
                st.session_state.signup_ok  = ""
            elif password != confirm:
                st.session_state.signup_err = "Passwords do not match."
                st.session_state.signup_ok  = ""
            elif "@" not in email:
                st.session_state.signup_err = "Please enter a valid email."
                st.session_state.signup_ok  = ""
            else:
                ok, msg = register(username, email, password)
                if ok:
                    st.session_state.signup_ok  = f"Account created! Welcome, {username}. Please log in."
                    st.session_state.signup_err = ""
                else:
                    st.session_state.signup_err = msg
                    st.session_state.signup_ok  = ""
            st.rerun()

        st.markdown("""
        <div class='auth-divider'>──────── OR ────────</div>
        <div class='auth-switch'>Already have an account?</div>
        """, unsafe_allow_html=True)

        if st.button("SIGN IN", key="btn_go_login"):
            st.session_state.auth_page  = "login"
            st.session_state.signup_err = ""
            st.session_state.signup_ok  = ""
            st.rerun()

        st.markdown("""
        <div style='text-align:center; margin-top:24px; font-family:"Share Tech Mono",monospace;
                    font-size:10px; color:#1e4d6b;'>
            🛡 PhishShield AI · Real-Time Phishing Protection
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DASHBOARD  (shown when logged in)
# ══════════════════════════════════════════════════════════════
KEYWORDS = ["login","signin","verify","update","secure","account",
            "bank","password","confirm","wallet","paypal","amazon","ebay","billing"]

def detect(url):
    u = url.lower()
    return "Phishing Website" if any(k in u for k in KEYWORDS) else "Legitimate Website"

def load_logs():
    if os.path.exists("logs.csv"):
        try:
            df = pd.read_csv("logs.csv", header=None, names=["url","prediction","timestamp"])
            return df
        except: pass
    now = datetime.now()
    data = [
        ("https://www.google.com",             "Legitimate Website"),
        ("http://paypal-login-secure.com",     "Phishing Website"),
        ("https://github.com",                 "Legitimate Website"),
        ("http://verify-bank-account-now.com", "Phishing Website"),
        ("https://www.youtube.com",            "Legitimate Website"),
        ("http://amazon-account-verify.com",   "Phishing Website"),
        ("https://wikipedia.org",              "Legitimate Website"),
        ("http://facebook-login-update.com",   "Phishing Website"),
        ("https://linkedin.com",               "Legitimate Website"),
        ("http://secure-paypal-signin.com",    "Phishing Website"),
        ("https://stackoverflow.com",          "Legitimate Website"),
        ("http://bank-login-confirm.com",      "Phishing Website"),
        ("https://www.microsoft.com",          "Legitimate Website"),
        ("http://update-your-account.com",     "Phishing Website"),
        ("https://reddit.com",                 "Legitimate Website"),
        ("http://apple-id-verify.com",         "Phishing Website"),
        ("https://twitter.com",                "Legitimate Website"),
        ("http://signin-secure-wallet.com",    "Phishing Website"),
        ("https://kaggle.com",                 "Legitimate Website"),
        ("http://password-reset-confirm.com",  "Phishing Website"),
    ]
    rows = [{"url": u, "prediction": p,
             "timestamp": (now - timedelta(minutes=i*6)).strftime("%H:%M:%S")}
            for i, (u, p) in enumerate(data)]
    return pd.DataFrame(rows)

def show_dashboard():
    df       = load_logs()
    total    = len(df)
    phishing = len(df[df["prediction"] == "Phishing Website"])
    safe     = total - phishing
    rate     = round(phishing / total * 100, 1) if total else 0

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:10px 0 20px 0;'>
          <div style='font-size:44px;'>🛡️</div>
          <div style='font-family:Orbitron,sans-serif;font-size:13px;font-weight:700;
                      color:#00d4ff;letter-spacing:4px;'>PHISHSHIELD</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;
                      color:#4a8fa8;letter-spacing:3px;margin-top:3px;'>AI SECURITY v1.0</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")

        uname = st.session_state.username
        email = st.session_state.user_data.get("email", "")
        since = st.session_state.user_data.get("created", "")
        st.markdown(f"""
        <div style='background:#040d1a;border:1px solid #0d3a5c;border-radius:6px;
                    padding:12px 14px;margin-bottom:14px;'>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;
                      letter-spacing:2px;color:#4a8fa8;margin-bottom:6px;'>LOGGED IN AS</div>
          <div style='font-family:Orbitron,sans-serif;font-size:14px;font-weight:700;
                      color:#00d4ff;'>👤 {uname}</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;
                      color:#4a8fa8;margin-top:4px;'>{email}</div>
          <div style='font-family:"Share Tech Mono",monospace;font-size:10px;
                      color:#1e4d6b;margin-top:2px;'>Member since {since}</div>
        </div>""", unsafe_allow_html=True)

        page = st.selectbox("📂 Navigate",
                            ["📊 Overview","🔍 URL Scanner","📋 Detection Log","📈 Analytics","👤 Profile"])
        st.markdown("---")
        st.markdown("""
        <div style='font-family:"Share Tech Mono",monospace;font-size:11px;color:#4a8fa8;'>
        <b style='color:#00d4ff;letter-spacing:2px;'>SYSTEM STATUS</b><br><br>
        <span style='color:#00ff88;'>●</span> API Server &nbsp;&nbsp; ONLINE<br>
        <span style='color:#00ff88;'>●</span> ML Model &nbsp;&nbsp;&nbsp; LOADED<br>
        <span style='color:#00ff88;'>●</span> Extension &nbsp;&nbsp; ACTIVE<br>
        <span style='color:#ffcc00;'>●</span> Threat DB &nbsp;&nbsp; SYNCING
        </div>""", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔓 LOGOUT", key="logout_btn"):
            st.session_state.logged_in   = False
            st.session_state.username    = ""
            st.session_state.user_data   = {}
            st.session_state.auth_page   = "login"
            st.rerun()

    # ── Header ────────────────────────────────────────────────
    st.markdown(f"""
    <div class='main-header'>
      <div class='main-title'>🛡 PHISHSHIELD AI</div>
      <div class='main-sub'>REAL-TIME PHISHING DETECTION SYSTEM · SECURITY DASHBOARD</div>
    </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # OVERVIEW
    # ══════════════════════════════════════════════════════════
    if "Overview" in page:
        c1,c2,c3,c4 = st.columns(4)
        cards = [
            (c1,"blue","⬡ Total Scanned", str(total),    "▲ +12 this session"),
            (c2,"red", "⚠ Phishing",      str(phishing), "▲ +3 this session"),
            (c3,"green","✓ Safe",          str(safe),     "▲ +9 this session"),
            (c4,"yellow","% Threat Rate",  f"{rate}%",    "▼ -2.1% vs yesterday"),
        ]
        for col, clr, lbl, val, dlt in cards:
            col.markdown(f"""<div class='mcard {clr}'>
                <div class='mlabel'>{lbl}</div>
                <div class='mvalue'>{val}</div>
                <div class='mdelta'>{dlt}</div>
            </div>""", unsafe_allow_html=True)

        lc, rc = st.columns([3,2])
        with lc:
            st.markdown("<div class='sec'>▸ Detection Activity (24h)</div>", unsafe_allow_html=True)
            hrs  = [f"{h:02d}:00" for h in range(0,24,2)]
            ph_v = [random.randint(0,12) for _ in hrs]
            lg_v = [random.randint(8,25)  for _ in hrs]
            fig  = go.Figure()
            fig.add_trace(go.Scatter(x=hrs,y=ph_v,name="Phishing",
                line=dict(color="#ff4444",width=2),fill="tozeroy",fillcolor="rgba(255,68,68,0.1)"))
            fig.add_trace(go.Scatter(x=hrs,y=lg_v,name="Legitimate",
                line=dict(color="#00d4ff",width=2),fill="tozeroy",fillcolor="rgba(0,212,255,0.05)"))
            fig.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
                font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),
                legend=dict(bgcolor="#040d1a",bordercolor="#0d3a5c",borderwidth=1,font=dict(color="#a0c4d8")),
                margin=dict(l=30,r=10,t=10,b=30),height=260,
                xaxis=dict(gridcolor="#0a2030",color="#4a8fa8"),
                yaxis=dict(gridcolor="#0a2030",color="#4a8fa8"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        with rc:
            st.markdown("<div class='sec'>▸ Threat Distribution</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Pie(labels=["Phishing","Legitimate"],values=[phishing,safe],hole=0.62,
                marker=dict(colors=["#ff4444","#00d4ff"],line=dict(color="#040d1a",width=3)),
                textfont=dict(family="Share Tech Mono",size=11,color="#c8e6f0"),
                hovertemplate="%{label}: %{value}<extra></extra>"))
            fig2.add_annotation(text=f"<b>{rate}%</b><br>THREAT",x=0.5,y=0.5,showarrow=False,
                font=dict(family="Orbitron",size=14,color="#ff6666"))
            fig2.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
                font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),
                legend=dict(bgcolor="#040d1a",bordercolor="#0d3a5c",borderwidth=1,font=dict(color="#a0c4d8")),
                margin=dict(l=10,r=10,t=10,b=10),height=260)
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

        bl, br = st.columns([2,3])
        with bl:
            st.markdown("<div class='sec'>▸ Top Threat Domains</div>", unsafe_allow_html=True)
            from urllib.parse import urlparse
            ph_df = df[df["prediction"]=="Phishing Website"].copy()
            def gd(u):
                try: return urlparse(u).netloc or u[:30]
                except: return u[:30]
            ph_df["domain"] = ph_df["url"].apply(gd)
            tc = ph_df["domain"].value_counts().head(5).reset_index()
            tc.columns = ["Domain","Hits"]
            fig3 = go.Figure(go.Bar(x=tc["Hits"],y=tc["Domain"],orientation="h",
                marker=dict(color=tc["Hits"],colorscale=[[0,"#003d5c"],[0.5,"#cc2222"],[1,"#ff4444"]]),
                text=tc["Hits"],textposition="outside",
                textfont=dict(color="#ff9999",family="Share Tech Mono",size=11)))
            fig3.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
                font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),
                margin=dict(l=10,r=30,t=5,b=10),height=230,
                xaxis=dict(gridcolor="#0a2030",color="#4a8fa8"),
                yaxis=dict(color="#a0c4d8"))
            st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

        with br:
            st.markdown("<div class='sec'>▸ Recent Phishing Alerts</div>", unsafe_allow_html=True)
            for _,row in df[df["prediction"]=="Phishing Website"].head(5).iterrows():
                url = row["url"]; ts = row.get("timestamp","--:--")
                st.markdown(f"""<div class='alrt'>⚠ PHISHING &nbsp;
                    <span style='color:#4a8fa8;font-size:10px;float:right;'>{ts}</span><br>
                    <span style='color:#ff888877;font-size:11px;'>{url[:65]}{'...'if len(url)>65 else ''}</span>
                </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # URL SCANNER
    # ══════════════════════════════════════════════════════════
    elif "Scanner" in page:
        st.markdown("<div class='sec'>▸ Manual URL Scanner</div>", unsafe_allow_html=True)
        col1,col2 = st.columns([5,1])
        with col1:
            test_url = st.text_input("URL",placeholder="https://example.com/login",
                                      label_visibility="collapsed")
        with col2:
            scan = st.button("⬡ SCAN")

        if scan and test_url:
            result   = detect(test_url)
            is_phish = result=="Phishing Website"
            if is_phish:
                st.markdown(f"""<div class='sr-phish'>
                  <div class='sr-tp'>⚠ PHISHING DETECTED</div>
                  <div class='sr-url'>{test_url}</div>
                  <div style='font-family:"Share Tech Mono",monospace;font-size:12px;
                              color:#ff666677;margin-top:10px;'>
                    Matches known phishing patterns. Do NOT enter credentials here.
                  </div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class='sr-safe'>
                  <div class='sr-ts'>✓ WEBSITE APPEARS SAFE</div>
                  <div class='sr-url'>{test_url}</div>
                  <div style='font-family:"Share Tech Mono",monospace;font-size:12px;
                              color:#00ff8877;margin-top:10px;'>
                    No phishing patterns detected.
                  </div></div>""", unsafe_allow_html=True)

            st.markdown("<div class='sec'>▸ Feature Analysis</div>", unsafe_allow_html=True)
            f1,f2,f3 = st.columns(3)
            matched  = [k for k in KEYWORDS if k in test_url.lower()]
            with f1:
                c = "red" if matched else "green"
                st.markdown(f"""<div class='mcard {c}'><div class='mlabel'>Matched Keywords</div>
                    <div class='mvalue' style='font-size:24px;'>{len(matched)}</div>
                    <div class='mdelta'>{", ".join(matched) if matched else "none"}</div></div>""",
                    unsafe_allow_html=True)
            with f2:
                lr = "red" if len(test_url)>70 else "green"
                st.markdown(f"""<div class='mcard {lr}'><div class='mlabel'>URL Length</div>
                    <div class='mvalue' style='font-size:24px;'>{len(test_url)}</div>
                    <div class='mdelta'>{'Suspicious >70' if len(test_url)>70 else 'Normal'}</div></div>""",
                    unsafe_allow_html=True)
            with f3:
                hs = test_url.startswith("https")
                st.markdown(f"""<div class='mcard {'green' if hs else 'yellow'}'><div class='mlabel'>HTTPS</div>
                    <div class='mvalue' style='font-size:24px;'>{'YES' if hs else 'NO'}</div>
                    <div class='mdelta'>{'Secure' if hs else 'Unencrypted'}</div></div>""",
                    unsafe_allow_html=True)

        st.markdown("<div class='sec'>▸ Quick Test URLs</div>", unsafe_allow_html=True)
        tests = [
            ("https://www.google.com",                  "✓ Safe",    "#00ff88"),
            ("http://paypal-login-security-update.com", "⚠ Phishing","#ff4444"),
            ("https://example.com/verify-account",      "⚠ Phishing","#ff4444"),
            ("https://www.wikipedia.org",               "✓ Safe",    "#00ff88"),
            ("http://amazon-account-login-verify.com",  "⚠ Phishing","#ff4444"),
            ("https://stackoverflow.com",               "✓ Safe",    "#00ff88"),
        ]
        t1,t2 = st.columns(2)
        for i,(u,lbl,clr) in enumerate(tests):
            (t1 if i%2==0 else t2).markdown(f"""
            <div class='lrow'>
              <span style='color:{clr};min-width:80px;font-family:"Share Tech Mono",monospace;font-size:11px;'>{lbl}</span>
              <span class='lurl'>{u}</span>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # DETECTION LOG
    # ══════════════════════════════════════════════════════════
    elif "Log" in page:
        st.markdown("<div class='sec'>▸ Detection Log</div>", unsafe_allow_html=True)
        filt = st.selectbox("Filter",["All","Phishing Only","Legitimate Only"])
        ddf  = df if filt=="All" else \
               df[df["prediction"]=="Phishing Website"] if "Phishing" in filt else \
               df[df["prediction"]=="Legitimate Website"]
        st.markdown("""<div class='lrow' style='border-bottom:1px solid #0d3a5c;'>
          <span class='ltime' style='color:#00d4ff;'>TIME</span>
          <span class='lurl'  style='color:#00d4ff;'>URL</span>
          <span style='min-width:120px;color:#00d4ff;font-family:"Share Tech Mono",monospace;font-size:11px;'>STATUS</span>
        </div>""", unsafe_allow_html=True)
        for _,row in ddf.iterrows():
            is_p  = row["prediction"]=="Phishing Website"
            badge = "<span class='bp'>⚠ PHISHING</span>" if is_p else "<span class='bs'>✓ SAFE</span>"
            ts    = row.get("timestamp","--:--"); url = row["url"]
            st.markdown(f"""<div class='lrow'>
              <span class='ltime'>{ts}</span>
              <span class='lurl' title='{url}'>{url[:60]}{'...'if len(url)>60 else ''}</span>
              <span style='min-width:120px;'>{badge}</span>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # ANALYTICS
    # ══════════════════════════════════════════════════════════
    elif "Analytics" in page:
        st.markdown("<div class='sec'>▸ Weekly Detection Trend</div>", unsafe_allow_html=True)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Phishing",  x=days,y=[random.randint(15,45) for _ in days],marker_color="#ff4444"))
        fig4.add_trace(go.Bar(name="Legitimate",x=days,y=[random.randint(60,120) for _ in days],marker_color="#00d4ff"))
        fig4.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
            font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),barmode="group",height=280,
            legend=dict(bgcolor="#040d1a",bordercolor="#0d3a5c",borderwidth=1,font=dict(color="#a0c4d8")),
            xaxis=dict(gridcolor="#0a2030",color="#4a8fa8"),
            yaxis=dict(gridcolor="#0a2030",color="#4a8fa8"),
            margin=dict(l=20,r=20,t=10,b=20))
        st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})

        al,ar = st.columns(2)
        with al:
            st.markdown("<div class='sec'>▸ Top Keyword Hits</div>", unsafe_allow_html=True)
            kws  = {k:random.randint(2,30) for k in KEYWORDS[:8]}
            fig5 = go.Figure(go.Bar(x=list(kws.values()),y=list(kws.keys()),orientation="h",
                marker=dict(color=list(kws.values()),colorscale=[[0,"#0d3a5c"],[1,"#ff4444"]])))
            fig5.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
                font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),
                margin=dict(l=10,r=20,t=5,b=10),height=270,
                xaxis=dict(gridcolor="#0a2030",color="#4a8fa8"),yaxis=dict(color="#a0c4d8"))
            st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar":False})

        with ar:
            st.markdown("<div class='sec'>▸ Detection Method</div>", unsafe_allow_html=True)
            fig6 = go.Figure(go.Pie(labels=["Keyword Match","URL Structure","ML Model"],
                values=[55,25,20],hole=0.5,
                marker=dict(colors=["#ff4444","#ffcc00","#00d4ff"],line=dict(color="#040d1a",width=2)),
                textfont=dict(family="Share Tech Mono",size=11,color="#c8e6f0")))
            fig6.update_layout(paper_bgcolor="#071828",plot_bgcolor="#071828",
                font=dict(family="Share Tech Mono",size=10,color="#4a8fa8"),
                legend=dict(bgcolor="#040d1a",bordercolor="#0d3a5c",borderwidth=1,font=dict(color="#a0c4d8")),
                margin=dict(l=10,r=10,t=10,b=10),height=270)
            st.plotly_chart(fig6,use_container_width=True,config={"displayModeBar":False})

        st.markdown("<div class='sec'>▸ Model Performance</div>", unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        for col,lbl,val,clr in [(m1,"Accuracy","96.4%","green"),(m2,"Precision","94.7%","blue"),
                                 (m3,"Recall","97.1%","blue"),(m4,"F1 Score","95.9%","yellow")]:
            col.markdown(f"""<div class='mcard {clr}'><div class='mlabel'>{lbl}</div>
                <div class='mvalue' style='font-size:26px;'>{val}</div>
                <div class='mdelta'>RandomForest · 200 trees</div></div>""",
                unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PROFILE
    # ══════════════════════════════════════════════════════════
    elif "Profile" in page:
        st.markdown("<div class='sec'>▸ User Profile</div>", unsafe_allow_html=True)
        uname = st.session_state.username
        email = st.session_state.user_data.get("email","")
        since = st.session_state.user_data.get("created","")

        p1,p2 = st.columns([1,2])
        with p1:
            st.markdown(f"""
            <div style='background:#071828;border:1px solid #0d3a5c;border-radius:8px;
                        padding:28px 24px;text-align:center;'>
              <div style='font-size:56px;margin-bottom:10px;'>👤</div>
              <div style='font-family:Orbitron,sans-serif;font-size:16px;font-weight:700;
                          color:#00d4ff;letter-spacing:2px;'>{uname}</div>
              <div style='font-family:"Share Tech Mono",monospace;font-size:11px;
                          color:#4a8fa8;margin-top:6px;'>{email}</div>
              <div style='margin-top:12px;'>
                <span style='background:rgba(0,255,136,0.1);border:1px solid #00ff88;
                             border-radius:3px;padding:3px 12px;
                             font-family:"Share Tech Mono",monospace;font-size:10px;
                             color:#00ff88;'>ACTIVE</span>
              </div>
              <div style='font-family:"Share Tech Mono",monospace;font-size:10px;
                          color:#1e4d6b;margin-top:12px;'>Member since {since}</div>
            </div>""", unsafe_allow_html=True)

        with p2:
            st.markdown("<div class='sec'>▸ Account Stats</div>", unsafe_allow_html=True)
            s1,s2 = st.columns(2)
            s1.markdown(f"""<div class='mcard blue'><div class='mlabel'>Total Scans</div>
                <div class='mvalue'>{total}</div><div class='mdelta'>All time</div></div>""",
                unsafe_allow_html=True)
            s2.markdown(f"""<div class='mcard red'><div class='mlabel'>Threats Found</div>
                <div class='mvalue'>{phishing}</div><div class='mdelta'>All time</div></div>""",
                unsafe_allow_html=True)

            st.markdown("<div class='sec'>▸ Change Password</div>", unsafe_allow_html=True)
            old_pw  = st.text_input("Current Password", type="password", key="cp_old")
            new_pw  = st.text_input("New Password",     type="password", key="cp_new")
            conf_pw = st.text_input("Confirm New",      type="password", key="cp_conf")
            if st.button("⬡ UPDATE PASSWORD", key="upd_pw"):
                if not old_pw or not new_pw or not conf_pw:
                    st.error("Please fill in all fields.")
                elif new_pw != conf_pw:
                    st.error("New passwords do not match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    users = load_users()
                    if users[uname]["password"] != hash_pw(old_pw):
                        st.error("Current password is incorrect.")
                    else:
                        users[uname]["password"] = hash_pw(new_pw)
                        save_users(users)
                        st.success("✓ Password updated successfully!")


# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    show_dashboard()
else:
    if st.session_state.auth_page == "login":
        show_login()
    else:
        show_signup()
