from utils.model_loader import ModelLoader
from autogen_agentchat.agents import AssistantAgent
from prompts.prompts_library import SystemPrompts


class ATSAgents:
    def __init__(self):
        self._model_client = ModelLoader().model_client

    def resume_processing_agent(self):
        return AssistantAgent(
            name="Resume Processing Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.RESUME_PROCESSING_AGENT,
        )

    def job_description_agent(self):
        return AssistantAgent(
            name="Job Description Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.JOB_DESCRIPTION_AGENT,
        )

    def scoring_agent(self):
        return AssistantAgent(
            name="Scoring Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.SCORING_AGENT,
        )

    def improvement_agent(self):
        return AssistantAgent(
            name="Improvement Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.IMPROVEMENT_AGENT,
        )

    def visualization_agent(self):
        return AssistantAgent(
            name="Visualization Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.VISUALIZATION_AGENT,
        )
