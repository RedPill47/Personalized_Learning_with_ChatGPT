from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI

#from .tools.browser_tools import BrowserTools
#from .tools.search_tools import SearchTools
from .tools.output_storage_tool import store_output, compile_latex

class TutorAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

    def learning_path_tutor(self):
        return Agent(
            role="Learning Path Tutor",
            backstory=dedent("""I'm a professor and personal tutor, designed to construct and adapt learning paths tailored to students' evolving needs."""),
            goal=dedent("""Create personalized course and flashcards that adapt to students' learning styles and preferences."""),
            tools=[
            #SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
            store_output,
            compile_latex,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def practical_tutor(self):
        return Agent(
            role="Practical Tutor",
            backstory=dedent("""I'm a professor and tutor that focuses on applying theoretical knowledge through interactive exercises."""),
            goal=dedent("""Create interactive exercises and quizzes that reinforce the theoretical knowledge of the course."""),
            tools=[
            #SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
            store_output,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def profiler(self):
        return Agent(
            role="Profiler",
            backstory=dedent("""I'm a profiler that analyzes students' learning preferences and strengths."""),
            goal=dedent("""Analyze students' learning preferences and strengths."""),
            tools=[
            store_output,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def digital_teacher(self):
        return Agent(
            role="Digital Teacher",
            backstory=dedent("""I'm a digital teacher responsible for verifying and coordinating all other agents, 
                             ensuring they complete their tasks as expected, and compiling their outputs into a comprehensive report."""),
            goal=dedent("""Verify and coordinate all agents, compile their outputs, and generate a comprehensive report."""),
            tools=[
            store_output,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def communication_chatbot(self):
        return Agent(
            role="Communication Chatbot",
            backstory=dedent("""I'm Tutor AI, a chatbot that serves as the first point of contact for students, providing support and gathering feedback."""),
            goal=dedent("""Facilitate communication and support, ensuring students are engaged and their feedback is incorporated."""),
            tools=[
            #SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )