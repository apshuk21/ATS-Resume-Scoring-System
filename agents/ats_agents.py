import asyncio
from utils.model_loader import ModelLoader
from autogen_agentchat.agents import AssistantAgent
from prompts.prompts_library import SystemPrompts
from models.resume_schema import ResumeSchema
from models.job_description_schema import JobDescriptionSchema
from models.score_report_schema import ScoreReportSchema


class ATSAgents:
    def __init__(self):
        self._model_client = ModelLoader().model_client

    def input_router_agent(self):
        return AssistantAgent(
            name="Input_Router_Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.INPUT_ROUTER_AGENT.value,
        )

    def resume_processing_agent(self):
        return AssistantAgent(
            name="Resume_Processing_Agent",
            description="The agent to process the user resume",
            model_client=self._model_client,
            system_message=SystemPrompts.RESUME_PROCESSING_AGENT.value,
            output_content_type=ResumeSchema,
        )

    def job_description_agent(self):
        return AssistantAgent(
            name="Job_Description_Agent",
            description="The agent to process the job description details",
            model_client=self._model_client,
            system_message=SystemPrompts.JOB_DESCRIPTION_AGENT.value,
            output_content_type=JobDescriptionSchema,
        )

    def scoring_agent(self):
        return AssistantAgent(
            name="Scoring_Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.SCORING_AGENT.value,
            output_content_type=ScoreReportSchema,
        )

    def improvement_agent(self):
        return AssistantAgent(
            name="Improvement_Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.IMPROVEMENT_AGENT.value,
        )

    def visualization_agent(self):
        return AssistantAgent(
            name="Visualization_Agent",
            description="",
            model_client=self._model_client,
            system_message=SystemPrompts.VISUALIZATION_AGENT.value,
        )


if __name__ == "__main__":

    async def main():
        resume_processing_agent = ATSAgents().resume_processing_agent()
        result = await resume_processing_agent.run(task="How are you?")
        print(result)

    asyncio.run(main=main())
