import streamlit as st
from rrjob_data import job_listings
import pandas as pd

#[theme]
#primaryColor="#4294ef"
#backgroundColor="#fdfeff"
#secondaryBackgroundColor="#cbd9f7"
#textColor="#080808"


st.set_page_config(page_title="Resumer Ranker app", layout="wide")

st.title('Welcome to ResumeRanker')

st.markdown("AI Resume Screening.")
st.badge("Connected to Talent Factory", color="blue")

st.sidebar.title("Welcome Alex Morgan")
st.sidebar.markdown("Administrator")

#to display each job with an existing form
if st.button("View Job Listings"):
    for idx, job in enumerate(job_listings):
        with st.container():
            st.subheader(f"{job['title']}")
            st.write(job["description"])

            with st.form(key=f"form_{idx}"):
                st.markdown("#### Apply for this job:")
                name = st.text_input("Full Name", key=f"name_{idx}")
                email = st.text_input("Email", key=f"email_{idx}")
                phone = st.text_input("Phone Number", key=f"phone_{idx}")
                cv = st.file_uploader("Upload CV (PDF only)", type=["pdf"], key=f"cv_{idx}")
                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    if name and email and phone and cv:
                        # Save file (os not functional yet)
                        save_path = os.path.join("uploads", f"{email.replace('@','_')}_{job['title'].replace(' ', '_')}.pdf")
                        with open(save_path, "wb") as f:
                            f.write(cv.read())
                        st.success("Application submitted successfully!")
                    else:
                        st.error("Please fill all fields and upload your CV.")

