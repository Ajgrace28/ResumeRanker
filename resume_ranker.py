import streamlit as st
from rrjob_data import job_listings
import pandas as pd

#[theme]
#primaryColor="#4294ef"
#backgroundColor="#fdfeff"
#secondaryBackgroundColor="#cbd9f7"
#textColor="#080808"


st.set_page_config(page_title="Resumer Ranker app", layout="wide")

col1, col2 = st.columns([6, 3])
with col2:
    st.image("https://cdn.brandfetch.io/idNw1YHdnr/w/543/h/99/theme/dark/logo.png?c=1bxid64Mup7aczewSAYMX&t=1713443558928", width=500)
with col1:
    st.title('Bluespace Job Application Portal')

#st.title('Bluespace Job Application Portal')
st.badge("Connected to Talent Factory", color="blue")

st.sidebar.title("Welcome Alex Morgan")
st.sidebar.markdown("Administrator")

# Initialize session state for selected job index
if "selected_job_idx" not in st.session_state:
    st.session_state.selected_job_idx = None
if "show_jobs" not in st.session_state:
    st.session_state.show_jobs = False

# A function to show job listings
#def show_job_listings():
    #st.session_state.show_jobs = True

# A function to toggle job listings visibility
def toggle_job_listings():
    st.session_state.show_jobs = not st.session_state.show_jobs
    st.session_state.selected_job_idx = None  # To hide any open form

# Function to show the application form for selected job index
def set_selected_job(index):
    st.session_state.selected_job_idx = index

#to display each job with an existing form
#if not st.session_state.show_jobs:
    #st.button("View Job Listings", on_click=show_job_listings)

# To Show or hide job listings
btn_label = "Hide Job Listings" if st.session_state.show_jobs else "View Job Listings"
st.button(btn_label, on_click=toggle_job_listings)

if st.session_state.show_jobs:
    for idx, job in enumerate(job_listings):
        with st.container():
            st.subheader(f"{job['title']}")
            st.write(job["description"])

            #For the Apply now button
            st.button(f"Apply Now for {job['title']}", key=f"apply_btn_{idx}", on_click= set_selected_job, args=(idx,))

            if st.session_state.get("selected_job_idx") == idx:
                # Display the application form
                st.markdown("Application Form")         
                with st.form(key=f"apply_form_{idx}"):
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

