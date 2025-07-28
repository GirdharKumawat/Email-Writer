import streamlit as st
from io import BytesIO
import PyPDF2
import re
from urllib.parse import urlparse
import time
from LangchainClass import Email_Writer

email_writer = Email_Writer()

# Page configuration
st.set_page_config(
    page_title="Job Application Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .input-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .output-section {
        background-color: #e8f5e8;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .feature-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 3px solid #667eea;
    }
    
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
   
    """Extract text content from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

 

def generate_application_email(job_description, resume_text):
    print("Generating email with job description:", job_description)
    if  job_description['role']=="" :
        st.warning("⚠️ No job description at Url. ")
        print("No job description at Url")
        return " No job description at Url"
    
    email = email_writer.generate_email(job_description, resume_text)
    return  email
   
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📧 Job Application Email Generator</h1>
        <p>Transform your job applications with AI-powered email generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔗 Job Information")
        job_url = st.text_input(
            "Job Posting URL",
            placeholder="https://example.com/job-posting",
            help="Enter the full URL of the job posting you're applying for"
        )
        
        # URL validation feedback
       
    with col2:
        st.subheader("📄 Resume Upload")
        uploaded_file = st.file_uploader(
            "Upload Your Resume (PDF)",
            type=['pdf'],
            help="Upload your resume in PDF format. Make sure it contains your contact information."
        )
    
    
    # Generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Generate Application Email", key="generate_btn"):
        # Validation
        if not job_url:
            st.error("❌ Please enter a job posting URL")
            return
        
        if uploaded_file is None:
            st.error("❌ Please upload your resume PDF")
            return
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Extract resume text
            status_text.text("📄 Processing resume...")
            progress_bar.progress(25)
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if not resume_text:
                st.error("❌ Could not extract text from resume. Please ensure it's a valid PDF.")
                return
            
            # Step 2: Fetch job description
            status_text.text("🔗 Fetching job description...")
            progress_bar.progress(50)
            job_description = email_writer.get_job_description(job_url)
            
            
            if not job_description:
                st.warning("⚠️ Could not fetch job description. Proceeding with resume information only.")
                job_description = "Job description not available"
            
            # Step 3: Generate email
            status_text.text("✉️ Generating application email...")
            progress_bar.progress(75)
            
            email_content = generate_application_email(job_description, resume_text)
            
            # Step 4: Complete
            status_text.text("✅ Email generated successfully!")
            progress_bar.progress(100)
            
            time.sleep(0.5)  # Brief pause for user experience
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display success message
            if email_content != " No job description at Url":
                st.markdown("""
                <div class="status-success">
                    <strong>🎉 Success!</strong> Your application email has been generated successfully.
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="status-error">
                <strong>❌ Error:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)
            return
    
    # Output Section (only show if email is generated)
    if 'email_content' in locals():
         
        # Email preview with copy functionality
        if email_content!="No job description at Url":
            st.subheader("📋 Email Content")
            st.text_area(
                "Generated Email (Ready to Copy)",
                value=email_content,
                height=400,
                help="Copy this email content and paste it into your email client. Review and customize as needed."
            )
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy to Clipboard", key="copy_btn"):
                    st.info("💡 Use Ctrl+A to select all, then Ctrl+C to copy the email content above")
            
   
  

if __name__ == "__main__":
    main()