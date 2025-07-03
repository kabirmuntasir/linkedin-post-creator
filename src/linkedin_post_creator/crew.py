from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List
import os
from dotenv import load_dotenv


@CrewBase
class LinkedinPostCreator:
    """LinkedinPostCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()

        # Load environment variables
        load_dotenv()

        # Initialize search tool
        self.serper_tool = SerperDevTool()

        # Load model config from environment
        model_provider = os.getenv("MODEL_PROVIDER", "gemini-pro")
        model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
        api_key = os.getenv("GEMINI_API_KEY")

        print("LLM Provider env var:", model_provider)
        print(f"🔥 Model Name: {model_name}")
        print("Using API key:", api_key[:8] + "...")

        # Initialize LLM
        self.llm = LLM(model=model_name, provider=model_provider, api_key=api_key)
        print(f"🔥 Using model: {model_name}, provider: {model_provider}")


    @agent
    def career_coach(self) -> Agent:
        return Agent(
            config=self.agents_config["career_coach"],
            tools=[self.serper_tool],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def linkedin_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["linkedin_writer"], llm=self.llm, verbose=True
        )

    @agent
    def content_critic(self) -> Agent:
        return Agent(
            config=self.agents_config["content_critic"], llm=self.llm, verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_creation_task"],
        )

    @task
    def content_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_review_task"],
            output_file="linkedin_post.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LinkedinPostCreator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
