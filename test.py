import streamlit as st
from rrjob_data import job_listings
import os
import time

st.set_page_config(page_title="Resumer Ranker app", layout="wide")

# Uploads Folder
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

# Job Application Dialog
@st.dialog("Job Application Form")
def job_application_form(job):
    st.write(f"Apply for: **{job['title']}**")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    cv = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])

    if st.button("Submit Application"):
        if name and email and phone and cv:
            # Save CV
            safe_title = job['title'].replace(' ', '_').replace('/', '_')
            save_path = os.path.join(
                uploads_folder, f"{email.replace('@','_')}_{safe_title}.pdf"
            )
            with open(save_path, "wb") as f:
                f.write(cv.read())

            st.session_state.application = {
                "job": job["title"],
                "name": name,
                "email": email,
                "phone": phone,
                "cv": cv.name
            }
            st.rerun()
        else:
            st.error("Please fill all fields and upload your CV.")

# --- Page Header ---
col1, col2 = st.columns([6, 3])
with col1:
    st.title("Bluespace Job Application Portal")
with col2:
    st.image(
        "https://cdn.brandfetch.io/idNw1YHdnr/w/543/h/99/theme/dark/logo.png?c=1bxid64Mup7aczewSAYMX&t=1713443558928", 
        use_container_width=True
    )

st.badge("Connected to Talent Factory", color="blue")

# Job Listings in Responsive Rows
cards_per_row = 3  # change to 2 for larger cards
for row_start in range(0, len(job_listings), cards_per_row):
    cols = st.columns(cards_per_row)
    for i, job in enumerate(job_listings[row_start:row_start + cards_per_row]):
        with cols[i]:  # This ensures the button is tied to the same column as the card
            # Job Card with border
            st.markdown(f"""
                <div style="border:1px solid #4294ef; border-radius:8px; padding:16px; 
                            height:350px; display:flex; flex-direction:column; 
                            justify-content:space-between; overflow-y:auto;">
                    <h2>{job['title']}</h2>
                    <p>{job['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            # Small space
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

            # Apply button stays under the card in the same column
            if st.button("Apply Now", key=f"apply_button_{row_start + i}"):
                job_application_form(job)

import time

# --- Confirmation after submission ---
if "application" in st.session_state:
    app = st.session_state.application
    placeholder = st.empty()

    # Fade out message after submission
    fade_message = f""" 
        <style>
        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            80% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
        .fade-out {{
            animation: fadeOut 3s forwards;
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            font-family: sans-serif;
        }}
        </style>
        <div class="fade-out">
            ✅ Application submitted for <b>{app['job']}</b> by {app['name']} ({app['email']})
        </div>
    """

    placeholder.markdown(fade_message, unsafe_allow_html=True)

    time.sleep(3)  # wait for fade to finish
    placeholder.empty()
    del st.session_state.application
