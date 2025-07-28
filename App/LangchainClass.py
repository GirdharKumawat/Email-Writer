 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"]  = os.getenv("GROQ_API_KEY")
class Email_Writer():
    def __init__(self):
        self.llm = ChatGroq( model="llama-3.3-70b-versatile",
     temperature=0,
     api_key=os.getenv("GROQ_API_KEY"),
     max_tokens=None,
     timeout=None,
     max_retries=2
    )
     
    def get_job_description(self, job_url):
        loader = WebBaseLoader(web_path = job_url)
        page_data_raw = loader.load().pop().page_content
        format_data = page_data_raw.replace('\n','').replace('  ','')        
        prompt_extract = PromptTemplate.from_template(  """### SCRAPED TEXT FROM WEBSITE: {page_data} ### INSTRUCTION:
      The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: role, experience, skills and description.
      Only return the valid JSON.
### VALID JSON (NO PREAMBLE):
only one object in this format 
***
    "role": "",
    "experience": "",
     "skills": "",
    "description": ""
    ***
"""



)

        chain = prompt_extract | self.llm
        job_description = chain.invoke({"page_data": format_data})
        
        json_parser = JsonOutputParser()
        job_description_dict = json_parser.parse(job_description.content)
        return job_description_dict
    
    def generate_email(self,job_description, resume):
        
        email_prompt_template = PromptTemplate.from_template(
    """
    ### JOB DESCRIPTION:
    {job_description}

    ### INSTRUCTION:
    You are a professional looking to apply for the job described above. and here is your resume {resume}.

    Your task is to write a cold email to the recruiter or hiring manager, expressing genuine interest in the role, aligning your skills and experience with the job description, and requesting an opportunity to connect or interview.

    Keep the tone professional yet approachable. You may also mention one or two key projects, skills, or achievements relevant to the job. Tailor your email to highlight how you are a great fit for this position.

    Do not provide a preamble.

    ### EMAIL (NO PREAMBLE):
    """
)
        
        email_chain = email_prompt_template | self.llm
        email_raw_response = email_chain.invoke({'job_description' : job_description,'resume':" "})
        return email_raw_response.content
    
    
        
        
        
        
        
        
        
        
        
        
        