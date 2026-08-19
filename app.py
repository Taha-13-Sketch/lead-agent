__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Lead Research Agent", page_icon="🎯")
st.title("🎯 AI B2B Lead Researcher & Email Personalizer")
st.caption("Powered by CrewAI & OpenAI")

# OpenAI API Key Input in Sidebar
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

company_name = st.text_input("Target Company / Prospect Name", "Stripe")
prospect_role = st.text_input("Prospect Role", "VP of Engineering")
value_proposition = st.text_area(
    "Your Service Value Prop",
    "We build custom CrewAI agents to automate internal workflows and cut operational costs by 40%.",
)

if st.button("Generate Cold Email Strategy"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        with st.spinner("Analyzing target company and crafting personalized email..."):
            # Agent 1: Lead Researcher
            researcher = Agent(
                role="Senior Business Researcher",
                goal=f"Analyze {company_name} to identify key focus areas for a {prospect_role}.",
                backstory="You are an expert market analyst who extracts business insights from public company data.",
                verbose=False,
            )

            # Agent 2: B2B Copywriter
            copywriter = Agent(
                role="Expert B2B Outreach Strategist",
                goal="Draft a highly personalized, 3-sentence cold email icebreaker and pitch.",
                backstory="You write high-converting cold emails that avoid spam triggers and feel strictly human.",
                verbose=False,
            )

            # Task 1: Research
            task_research = Task(
                description=f"Identify key focus areas and strategic priorities for {company_name} relevant to a {prospect_role}.",
                expected_output="Bullet points of key company priorities and specific pain points.",
                agent=researcher,
            )

            # Task 2: Copywriting
            task_copy = Task(
                description=f"Using the research, write a 3-sentence email to the {prospect_role} at {company_name}. Link their goals to this value prop: {value_proposition}.",
                expected_output="A clean, professional cold email draft with Subject Line and Body.",
                agent=copywriter,
            )

            # Assemble Crew
            crew = Crew(
                agents=[researcher, copywriter],
                tasks=[task_research, task_copy],
                process=Process.sequential,
            )

            result = crew.kickoff()

            st.success("Analysis Complete!")
            st.markdown("### Output Strategy & Email")
            st.markdown(result.raw)
