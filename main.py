import os
import argparse
import logging

from twilio.rest import Client

from speller_agent import SpellerAgentFactory

account_sid = os.getenv('TWILIO_ACCOUNT_SID', None)
auth_token = os.getenv('TWILIO_AUTH_TOKEN', None)

client = Client(account_sid, auth_token)

from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)

import uvicorn

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware


from sl_agent import  SmartloopAgentFactory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BASE_URL = os.getenv("BASE_URL")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assort Health')

    parser.add_argument('command', metavar='<command>', choices=['server'],
                        help='server')

    args = parser.parse_args()

    config_manager = RedisConfigManager()

    telephony_server = TelephonyServer(
        base_url=BASE_URL,
        config_manager=config_manager,
        inbound_call_configs=[
            TwilioInboundCallConfig(
                url="/inbound_call",
                agent_config=ChatGPTAgentConfig(
                    initial_message=BaseMessage(text="Hello welcome to Assort Health"),
                    prompt_preamble="Book an appointment",
                    generate_responses=True,
                ),
                twilio_config=TwilioConfig(
                    account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                    auth_token=os.environ["TWILIO_AUTH_TOKEN"],
                ),
            )
        ],
        agent_factory=SpellerAgentFactory(),
        logger=logger,
    )

    app.include_router(telephony_server.get_router())

    if args.command == 'server':
        uvicorn.run(app, host="0.0.0.0", port=3000)


