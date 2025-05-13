import streamlit as st
import pandas as pd
import openai
import base64
import smtplib
from email.mime.text import MIMEText

# Constants
USERNAME = "Maithraanand R"
PASSWORD = "password"

# OpenAI API Key
openai.api_key = "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"

# Login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "about" 
if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = "" 

# Download file path
file_path = r"D:\MAITHU\Infyspringboard\PROJECT\Air Quality Index.pbix"

# Encode file data for download
def encode_file(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
    return base64.b64encode(file_data).decode("utf-8")

# Path to your CSV file
AQI_CSV_PATH = r"D:\MAITHU\Infyspringboard\PROJECT\Air Pollution Data.csv"

# Function to load the AQI data
@st.cache_data
def load_aqi_data():
    return pd.read_csv(AQI_CSV_PATH)

# Load the data
aqi_data = load_aqi_data()


# Function to query OpenAI chatbot
def query_chatbot(question, aqi_data):
    context = (
        "You are an expert chatbot specializing in the Air Quality Index (AQI) "
        "in India. You have access to the following AQI data:\n\n"
        f"{aqi_data.head(10).to_string(index=False)}\n\n"
        "Use this data to answer questions factually and concisely."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question},
            ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

# Login function
def login():
    st.title("Login Page")
    st.write("Please enter your login details to access the dashboard.")
    
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    remember_me = st.checkbox("Remember Me")
    login_button = st.button("Login", key="login_button")
    
    if login_button:
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            if remember_me:
                st.session_state.remember_me = True 
            st.success("Login successful! Click below to continue.")
        else:
            st.error("Incorrect username or password.")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.remember_me = False

# Feedback sending function
def send_feedback(feedback_text):
    try:
        smtp_server = "smtp.office365.com"
        smtp_port = 587
        smtp_user = "support@aptpath.in"
        smtp_password = "kjydtmsbmbqtnydk"
        sender_email = "support@aptpath.in"
        receiver_email = "maithraanand2004@gmail.com"

        msg = MIMEText(feedback_text)
        msg["Subject"] = "Feedback from AQI Dashboard"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.session_state.feedback_message = "Feedback successfully sent!"
    except Exception as e:
        st.session_state.feedback_message = f"An error occurred while sending feedback: {e}"

# Automatically login if "Remember Me" is selected
if "remember_me" in st.session_state and st.session_state.remember_me:
    st.session_state.logged_in = True

# Load AQI data
AQI_CSV_PATH = r"D:\MAITHU\Infyspringboard\PROJECT\Air Pollution Data.csv" 
aqi_data = load_aqi_data(AQI_CSV_PATH)

# Display the login page if not logged in
if not st.session_state.logged_in:
    login()
else:
    # Sidebar navigation
    st.sidebar.title("Main Menu")
    about_btn = st.sidebar.button("About Page", key="about_page_btn")
    dashboard_btn = st.sidebar.button("Dashboard", key="dashboard_page_btn")
    chatbot_btn = st.sidebar.button("Chatbot", key="chatbot_page_btn")
    download_btn = st.sidebar.button("Download", key="download_page_btn")
    logout_btn = st.sidebar.button("Logout", key="logout_btn")

    # Handle navigation logic
    if about_btn:
        st.session_state.page = "about"
    elif dashboard_btn:
        st.session_state.page = "dashboard"
    elif chatbot_btn:
        st.session_state.page = "chatbot"
    elif download_btn:
        encoded_file = encode_file(file_path)
        st.download_button(
            label="Download PBIX File",
            data=base64.b64decode(encoded_file),
            file_name="Air Quality Index.pbix",
            mime="application/octet-stream"
        )
    elif logout_btn:
        logout()

    # Content Display based on selected page
    if st.session_state.page == "about":
        st.title("About Air Quality Index (AQI)")
        st.write("""
        ### **What is the Air Quality Index (AQI)?**
        The AQI is a tool used to measure and report the quality of air in a specific area. It simplifies complex air pollution data into a single number or scale, making it easy for people to understand how clean or polluted the air is and what associated health risks may exist.

        ### **Why is the AQI Important?**
        The AQI serves as a valuable tool for safeguarding public health and ensuring environmental sustainability. Poor air quality can have immediate effects, such as irritation of the eyes, nose, and throat, as well as more severe impacts like worsening asthma and other respiratory conditions. Long-term exposure to polluted air is linked to chronic illnesses, including heart disease, lung cancer, and reduced life expectancy.

        ### **AQI Scale and Meaning**
        - **Good (0–50, Green):** Air quality is considered satisfactory, posing little or no risk.
        - **Moderate (51–100, Yellow):** Air quality is acceptable; however, some sensitive individuals may experience minor discomfort.
        - **Unhealthy for Sensitive Groups (101–150, Orange):** Sensitive groups, such as children, the elderly, or those with respiratory conditions, may experience health effects.
        - **Unhealthy (151–200, Red):** Everyone may start to experience adverse health effects.
        - **Very Unhealthy (201–300, Purple):** Health alert—serious health effects can occur.
        - **Hazardous (301–500, Maroon):** Emergency conditions—everyone is likely to be affected.

        ### **How Does Air Pollution Affect Us?**
        Air pollution doesn't just harm our health—it affects ecosystems, economies, and overall quality of life. Prolonged exposure to polluted air can damage crops, reduce visibility, and harm wildlife. It contributes to environmental issues like acid rain, which affects water quality and soil fertility, and the urban heat island effect, which makes cities hotter and less habitable.

        ### **Steps to Improve Air Quality**
        Reducing air pollution requires collective effort and innovative solutions. On a personal level, using public transportation, conserving energy, and reducing waste can make a difference. Community-level initiatives like adopting renewable energy sources, enforcing stricter emission controls, and promoting tree planting are crucial for creating cleaner air and a healthier environment.
        """)
    elif st.session_state.page == "dashboard":
        st.title("Air Quality Index Dashboard")
        st.write("This is a dashboard about Air Quality Index (AQI) in India")
        # Embed Power BI Dashboard using HTML iframe
        power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzE1NjM4Y2UtMzBhNy00NDNmLWEyNmMtMWExNDU5NWU0ZDZhIiwidCI6ImUxZGFlMjBiLWMzZDAtNGI4ZC05MTg5LTEwMzVhMTk1YmE2YiJ9"
        st.markdown(
            f"""
            <iframe src="{power_bi_url}" frameborder="0" allowFullScreen="true" style="width:100%; height: 80vh;"></iframe>
            """,
            unsafe_allow_html=True
        )
    elif st.session_state.page == "chatbot":
        st.title("AQI Chatbot")
        st.write("Ask any questions about AQI in India or the dashboard data below.")
        user_question = st.text_input("Enter your question:")
        if st.button("Ask Chatbot"):
            if user_question.strip():
                response = query_chatbot(user_question, aqi_data)
                st.write("Chatbot Response:")
                st.success(response)
            else:
                st.error("Please enter a question.")

    # Feedback Section
    st.sidebar.title("Feedback")
    feedback_text = st.sidebar.text_area(
        "Enter your feedback:",
        max_chars=500,
        height=150,
    )
    send_btn = st.sidebar.button("Send Feedback", key="send_feedback_btn")

    if send_btn:
        if feedback_text.strip():
            send_feedback(feedback_text)
        else:
            st.session_state.feedback_message = "Please enter some feedback before sending."
    
    # Display feedback message under the text box
    st.sidebar.write(st.session_state.feedback_message)
