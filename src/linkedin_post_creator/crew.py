from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LinkedinPostCreator():
    """LinkedinPostCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Initialize search tools - using only SerperDevTool since WebsiteSearchTool requires OpenAI
        self.serper_tool = SerperDevTool()
        
        # Initialize Gemini LLM
        self.llm = LLM(
            model="gemini/gemini-2.5-pro-preview-03-25",
            api_key=os.getenv("GEMINI_API_KEY")
        )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def career_coach(self) -> Agent:
        return Agent(
            config=self.agents_config['career_coach'],
            tools=[self.serper_tool],
            llm=self.llm,
            verbose=True
        )

    @agent
    def linkedin_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_writer'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def content_critic(self) -> Agent:
        return Agent(
            config=self.agents_config['content_critic'],
            llm=self.llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
        )

    @task
    def content_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_review_task'],
            output_file='linkedin_post.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LinkedinPostCreator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
