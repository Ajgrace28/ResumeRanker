import streamlit as st
from rrjob_data import job_listings
import pandas as pd
import os


st.set_page_config(page_title="Resumer Ranker app", layout="wide")

col1, col2 = st.columns([6, 3])
with col2:
    st.image("https://cdn.brandfetch.io/idNw1YHdnr/w/543/h/99/theme/dark/logo.png?c=1bxid64Mup7aczewSAYMX&t=1713443558928", width=500)
with col1:
    st.title('Bluespace Job Application Portal')

#st.title('Bluespace Job Application Portal')
st.badge("Connected to Talent Factory", color="blue")


# Create uploads folder if not exists
#if not os.path.exists("uploads"):
    #os.makedirs("uploads")
num_jobs = len(job_listings)
cols = st.columns(num_jobs)

# Display each job with a form
for idx, job in enumerate(job_listings):
    with cols[idx]:
        st.markdown(f"""
            <div style="border:1px solid #4294ef; border-radius:8px; padding:16px; margin-bottom:16px;
                    height:350px; display:flex; flex-direction:column; justify-content:space-between; overflow-y:auto;">
                <h2>{job['title']}</h2>
                <p>{job['description']}</p>
            </div>
            """,
            unsafe_allow_html=True) #added new code for adding a border using Markdown and HTML
    #with st.container():
        #st.subheader(f"{job['title']}")
        #st.write(job["description"])

        #Unique key for each form to avoid conflicts
        form_key = f"apply_form_{idx}"
        if form_key not in st.session_state:
            st.session_state[form_key] = False #added new code
        
        #To create an "Apply now" button which toggles the form visibility
        if st.button("Apply Now", key=f"apply_button{idx}"):
            st.session_state[form_key] = not st.session_state[form_key] #added new code

        #To show the form if the button was clicked
        if st.session_state[form_key]:  #added new code
            with st.form(key=f"form_{idx}"):
                st.markdown("Apply for this job:")
                name = st.text_input("Full Name", key=f"name_{idx}")
                email = st.text_input("Email", key=f"email_{idx}")
                phone = st.text_input("Phone Number", key=f"phone_{idx}")
                cv = st.file_uploader("Upload CV (PDF only)", type=["pdf"], key=f"cv_{idx}")
                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    if name and email and phone and cv:
                        # Save file
                        os.makedirs("uploads", exist_ok=True)
                        save_path = os.path.join("uploads", f"{email.replace('@','_')}_{job['title'].replace(' ', '_')}.pdf")
                        with open(save_path, "wb") as f:
                            f.write(cv.read())
                        st.success("Application submitted successfully!")
                    else:
                        st.error("Please fill all fields and upload your CV.")
