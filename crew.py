	
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool
from pydantic import BaseModel, Field
from typing import List
from main import input
from dotenv import load_dotenv

load_dotenv()

tool = WebsiteSearchTool(
	website= input,
	config=dict(
		llm=dict(
			provider="groq", 	
			config=dict(
				model="llama-3.1-8b-instant",
				
			),
		),
		embedder=dict(
			provider="huggingface", 
			config=dict(
				model="BAAI/llm-embedder",
				
			),
		),
	)
)

@CrewBase
class ProductAreaGenerator():
	"""ProductAreaGenerator crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def product_area_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['product_area_strategist'],
			tools=[tool],
			verbose=True
		)

	@agent
	def insights_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['insights_analyst'],
			verbose=True
		)

	@agent
	def implementer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['implementer_agent'],
			verbose=True
		)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def product_area_strategist_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_area_strategist_task'],
		)

	@task
	def insights_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['insights_analyst_task'],
		)
	
	@task
	def implementer_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['implementer_agent_task'],
			output_file= "output/report.json"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ProductAreaGenerator crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

