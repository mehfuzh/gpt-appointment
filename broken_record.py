from vocode.streaming.agent.base_agent import RespondAgent
from vocode.streaming.models.agent import AgentConfig
from typing import Optional, Tuple, AsyncGenerator

class BrokenRecordAgentConfig(AgentConfig, type="agent_broken_record"):
    message: str

class BrokenRecordAgent(RespondAgent[BrokenRecordAgentConfig]):

    # is_interrupt is True when the human has just interrupted the bot's last response
    def respond(
        self, human_input, is_interrupt: bool = False
    ) -> tuple[Optional[str], bool]:
        return self.agent_config.message

    async def generate_response(
        self, human_input, is_interrupt: bool = False
    ) -> AsyncGenerator[Tuple[str, bool], None]: # message and whether or not the message is interruptible
        """Returns a generator that yields the agent's response one sentence at a time."""
        yield self.agent_config.message, False