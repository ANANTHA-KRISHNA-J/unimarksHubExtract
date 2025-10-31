import streamlit as st

# ----------------------------
# 🔐 SIMPLE LOGIN SYSTEM (no deps)
# ----------------------------

# Configure page
st.set_page_config(
    page_title='Hub-Data-Extractor',
    page_icon='unimarks_logo.png',
    layout='wide',
    initial_sidebar_state='collapsed',
    menu_items={'Get help': 'mailto:dsa@unimarkslegal.com'}
)


# Define allowed users
USER_CREDENTIALS = {
    "Arul": "Arulunimarks",
    "Sales": "Salesunimarks",
    "Operations": "Operationsunimarks"
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN PAGE STYLE ---
st.markdown("""
<style>
/* ✅ Force full-page flex centering */
section.main {
    display: flex;
    justify-content: center !important;
    align-items: center !important;
    height: 100vh;
    padding: 0 !important;        /* remove Streamlit padding */
    margin: 0 auto !important;    /* ensure full center horizontally */
}

/* ✅ Remove Streamlit container padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    margin: 0 auto !important;
}

/* 🔹 Login card style */
div[data-testid="stForm"] {
    background-color: #0b1221;
    border-radius: 16px;
    padding: 50px 60px;
    box-shadow: 0 0 25px rgba(0,255,255,0.3);
    border: 1px solid rgba(0,255,255,0.4);
    width: 500px;
    text-align: center;
    margin: auto; /* ✅ keep perfectly centered */
}

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stPasswordInput"] input {
    background-color: #141c2c !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0,255,255,0.4) !important;
    text-align: center;
}

/* Labels */
label {
    color: #a9b3c1 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.4rem !important;
}

/* Title */
.login-title {
    color: cyan;
    font-weight: 600;
    font-size: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

/* Button */
button[kind="primary"] {
    background-color: cyan !important;
    color: #0b1221 !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    width: 100%;
    padding: 10px 0;
    font-size: 1.1rem;
}
button[kind="primary"]:hover {
    background-color: #00e6e6 !important;
    box-shadow: 0 0 10px cyan;
}
</style>
""", unsafe_allow_html=True)


# --- LOGIN FORM ---
if not st.session_state.logged_in:
    st.markdown("""
<h2 style="
    text-align:center;
    color: cyan;
    font-weight: 700;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 10px rgba(0,255,255,0.6);
"> Hub Extractor Login</h2>
""", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    st.stop()  # prevent showing main app when not logged in

# --- LOGOUT + MAIN APP ---
st.sidebar.success(f"Logged in as {st.session_state.username}")
if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # clears everything
    st.experimental_rerun()

# Your main app starts here ↓
from dotenv import load_dotenv
import os
import datetime
import streamlit as st
from helper import fetch_deals, dict_to_table
from langchain_google_genai import ChatGoogleGenerativeAI

# --- PAGE CONFIG ---

# --- CUSTOM UI CSS ---
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
h1 {margin-top: 0rem; padding-top: 0rem;}
h4 {margin-bottom: 0.25rem !important; padding-top: 0.5rem !important;}
div[data-testid="stFormSubmitButton"] + div > div {
    margin-top: -15px !important;
}
div[data-testid="stMultiSelect"], div[data-testid="stDateInput"] {
    max-width: 250px;
}
div.stButton > button {
    display: block;
    margin: 0 auto;
    background-color: #0078ff;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #3399ff;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# --- LOAD API KEYS ---
load_dotenv()
google_api_key = os.getenv('GOOGLE-API-KEY')
llm = ChatGoogleGenerativeAI(
    temperature=0.7,
    max_tokens=100,
    model='models/gemini-2.5-flash-lite',
    api_key=google_api_key
)

# --- STATIC DATA ---
reversepocmaps = {
"76821774": "Priyadharshini",
"76821788": "Sandhiya Durai",
"76821797": "Lavanya Vasu",

"680448818": "Sachin Priya Daniel S",
"714526095": "Shunmuga Priya",

"78470503": "Madesh Krishna",  "408847625": "Samuel J",
"522462019": "Ananthi N",
"78471123": "Hariprasad K",  "523812380": "Mohan M",

"86718745": "Sandhiya Durai",
"149025425": "Admin Pearlpick",
"149053803": "Kamini B",

"149055031": "Mansoor ali",
"149055768": "Suresh Kumar",
"149747514": "Ajay s",
"149749362": "Arul A",  "153245866": "Dinesh Kumar",
"150407859": "Tharani Ravi",
"523817838": "Raj Kamal",
"78642521": "Lenin Samuel",

"154662495": "Support Unimarks",
"159668346": "Legal Intern",
"159721290": "Sree Ramya Vangala",
"159759344": "Naseema A",
"171398516": "Pearlpick Ventures V",  "206374727": "Kavitha Sagayaraj",
"230919210": "Mohammed Tajuddin",  "78469530": "Lavanya Vasu",


"245151011": "Mohitha CS",
"257629073": "Jigar k Patel",
"279925039": "Siva Kumar",
"374660102": "Dinesh R",
"398321190": "Leads Pearlpick Ventures",
"523812209": "dinesh 1",
"565519544": "Vaishali J",
"601770628": "Sophia Jeyakar",  "79184854": "Mary Santo Disha",  "150046306": "Viswesswaar P",
"150057355": "Divya S",
"79299552": "Bhavani Sri",  "150484830": "Amanullah Sulthan",  "180329123": "Vijaya Lakshmi",
"636134420": "Oveya S", "77492250": "Ankith Kumar","78470076": "Ashwini M","149055026": "Ajith Prathap Singh",

}
PocOptions = list(reversepocmaps.values())

reversestagemaps = {
    'Qualified': 'qualifiedtobuy',
    'Proposal Sent': 'contractsent',
    'In Progress': 'decisionmakerboughtin',
    'Awaiting Payment': '14261535',
    'Payment Processed': '14440564',
    'Closed won': 'closedwon',
    'Closed lost': 'closedlost',
    'Sent to Ops': '14459000',
    'New': 'appointmentscheduled',
    'Negotiation': '14261534'
}
DealStagesOptions = list(reversestagemaps.keys())
DealTypesOptions = ['newaffiliate', 'Existing Affiliate', 'newbusiness', 'Existing Business']
# 🔓 Full layout reset after login (fixes frozen/locked scrolling)
st.markdown("""
<style>
/* Restore Streamlit default layout after login */
section.main {
    display: block !important;
    align-items: unset !important;
    justify-content: unset !important;
    height: auto !important;
    overflow: visible !important;
    padding: 2rem 1rem !important;
}

/* Ensure page and body are scrollable */
html, body {
    height: auto !important;
    overflow: auto !important;
}

/* Remove any leftover full-height behavior */
[data-testid="stAppViewContainer"] {
    height: auto !important;
    overflow: auto !important;
}
</style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.subheader('HUB-Extractor')

stdate, nddate, dtype, dstage, pocfilter = st.columns(5)
with stdate:
    startdate = st.date_input('Extract Deals From(Date):', min_value=datetime.date(2021, 1, 1))
with nddate:
    enddate = st.date_input('Extract Deals Till(Date):')
with dtype:
    selectdealtypes = st.multiselect('Select Deal Type:', options=DealTypesOptions, placeholder='Default: All')
with dstage:
    selectdealstage = st.multiselect('Select Deal Stage:', options=DealStagesOptions, placeholder='Default: Closed Deals')
with pocfilter:
    pocfilters1 = st.multiselect('**POC**', options=PocOptions, placeholder='Default: All')

default_stages_option = ['closedwon', '14459000', '14440564']
finaldealstages = [reversestagemaps[label] for label in selectdealstage] if selectdealstage else default_stages_option
finaldealtypes = selectdealtypes if selectdealtypes else DealTypesOptions
pocfilters = [key for key, value in reversepocmaps.items() if value in pocfilters1] if pocfilters1 else list(reversepocmaps.keys())

form = {
    "start_date": startdate.strftime("%Y-%m-%d"),
    "end_date": enddate.strftime("%Y-%m-%d"),
    "dealtypes": finaldealtypes,
    "dealstages": finaldealstages,
    "pocfilters": pocfilters
}

# --- DATA EXTRACTION ---
if "df" not in st.session_state:
    st.session_state.df = None
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button('Start Data Extraction', type='primary'):
    count, data_list = fetch_deals.invoke(form)
    if not data_list:
        st.warning("No deals found for the selected filters.")
        st.session_state.count = 0
    else:
        st.session_state.count = count
        df = dict_to_table(data_list)
        st.session_state.df = df
        st.success("✅ Data extracted successfully!")

if st.session_state.count > 0:
    st.markdown(f"Displaying **{st.session_state.count}** deals")

if st.session_state.df is not None:
    st.dataframe(st.session_state.df, hide_index=True)
else:
    st.info("Fetched data will appear here.")

# --- QUERY SECTION ---
st.markdown('<div style="text-align:center;font-size:1.4rem;"><b>Chat with Data</b></div>', unsafe_allow_html=True)

with st.form(key="query_form"):
    query = st.text_area("", placeholder="Type your question and clisk Ask or Ctrl+Enter...")
    ask = st.form_submit_button("Ask")

if ask:
    df = st.session_state.df
    if df is None:
        st.warning("Please extract data first!")
    else:
        if "sum" in query.lower() and "amount" in query.lower():
            total = df["Amount"].sum()
            st.markdown(f"**Answer:** The total sum of Amount is ₹{total:,.2f}")
        elif "average" in query.lower() and "amount" in query.lower():
            avg = df["Amount"].mean()
            st.markdown(f"**Answer:** The average Amount is ₹{avg:,.2f}")
        else:
            dataset = df.to_csv(index=False)
            prompt = f"""
                You are a data analyst with strong arithmetic skills.
                Analyze the following CSV dataset and answer the user's question accurately and briefly.
                Dataset:
                {dataset}
                User's question: {query}
                Give a clear, concise answer (1–2 sentences maximum) based only on the dataset.
            """
            with st.spinner("Using AI..."):
                response = llm.invoke(prompt)
                answer = response.content
                st.markdown(
                    f"""
                    <div style="background-color:#1E1E1E;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-size:1.1rem;
                    border:1px solid #444;
                    box-shadow:0 4px 8px rgba(0,0,0,0.2);
                    margin-top:20px;">
                    <b>Answer:</b><br><br>{answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

st.write("")  # adds small empty space so Streamlit reflows
st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)