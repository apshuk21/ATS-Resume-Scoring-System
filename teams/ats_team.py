from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from agents.ats_agents import ATSAgents
from autogen_agentchat.messages import StructuredMessage
from models.resume_schema import ResumeSchema
from models.job_description_schema import JobDescriptionSchema
from models.score_report_schema import ScoreReportSchema
from models.improvement_report_schema import ImprovementReportSchema
from models.visualization_payload_schema import VisualizationPayloadSchema
from autogen_agentchat.conditions import TextMentionTermination


class ATSTeam:
    def __init__(self):
        self._builder = DiGraphBuilder()
        self._ats_agents = ATSAgents()

        self._input_router_agent = self._ats_agents.input_router_agent()
        self._resume_processing_agent = self._ats_agents.resume_processing_agent()
        self._job_description_agent = self._ats_agents.job_description_agent()
        self._scoring_report_agent = self._ats_agents.scoring_agent()
        self._improvement_agent = self._ats_agents.improvement_agent()
        self._visualization_agent = self._ats_agents.visualization_agent()

        self._termination_condition = TextMentionTermination("TERMINATE")

    def _add_all_agents(self):
        self._builder.add_node(self._input_router_agent).add_node(
            self._resume_processing_agent
        ).add_node(self._job_description_agent).add_node(
            self._scoring_report_agent
        ).add_node(
            self._improvement_agent
        ).add_node(
            self._visualization_agent
        )

    def _add_routing_edges(self):
        # Parallel agents
        self._builder.add_edge(self._input_router_agent, self._resume_processing_agent)
        self._builder.add_edge(self._input_router_agent, self._job_description_agent)

        # Sequential agents
        self._builder.add_edge(
            self._resume_processing_agent, self._scoring_report_agent
        )
        self._builder.add_edge(self._job_description_agent, self._scoring_report_agent)

        self._builder.add_edge(self._scoring_report_agent, self._improvement_agent)

        self._builder.add_edge(self._scoring_report_agent, self._visualization_agent)

        self._builder.add_edge(self._improvement_agent, self._visualization_agent)

    def create_graph_flow(self):
        self._add_all_agents()
        self._add_routing_edges()

        self._builder.set_entry_point(self._input_router_agent)

        graph = self._builder.build()

        return GraphFlow(
            participants=self._builder.get_participants(),
            graph=graph,
            termination_condition=self._termination_condition,
            custom_message_types=[
                StructuredMessage[ResumeSchema],
                StructuredMessage[JobDescriptionSchema],
                StructuredMessage[ScoreReportSchema],
                StructuredMessage[ImprovementReportSchema],
                StructuredMessage[VisualizationPayloadSchema],
            ],
        )
