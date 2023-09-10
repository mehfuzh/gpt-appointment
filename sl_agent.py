from pydantic import BaseModel
from fastapi import APIRouter

import logging
import typing
from typing import Tuple, Optional
from vocode.streaming.agent.base_agent import  BaseAgent, RespondAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.agent.factory import AgentFactory
from vocode.streaming.models.agent import AgentConfig, AgentType, ChatGPTAgentConfig

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SmartloopAgentConfig(AgentConfig, type="agent_smartloop"):
    pass

class SmartloopAgent(RespondAgent[SmartloopAgentConfig]):
    def __init__(self, agent_config: SmartloopAgentConfig):
        super().__init__(agent_config=agent_config)

    async def respond(
        self,
        human_input,
        conversation_id: str,
        is_interrupt: bool = False,
    ) -> Tuple[Optional[str], bool]:
        return "".join(c + " " for c in human_input), False


class SmartloopAgentFactory(AgentFactory):
    def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
        if agent_config.type == AgentType.CHAT_GPT:
            return ChatGPTAgent(
                agent_config=typing.cast(ChatGPTAgentConfig, agent_config)
            )
        elif agent_config.type == "agent_smartloop":
            return SmartloopAgent(self, agent_config=SmartloopAgentConfig)
        raise Exception("Invalid agent config")
