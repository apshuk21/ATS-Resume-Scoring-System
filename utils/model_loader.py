import os
import asyncio
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage


class ModelLoader:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("OPENAI_API_KEY")
        self._llm = OpenAIChatCompletionClient(model="gpt-4o", api_key=self._api_key)

    @property
    def model_client(self):
        return self._llm


if __name__ == "__main__":

    async def main():
        model_client = ModelLoader().model_client

        response = await model_client.create(
            [UserMessage(content="What is the capital of France?", source="user")]
        )
        print(response)

        output = await model_client.create(
            [UserMessage(content="Who won the first IPL?", source="user")]
        )
        print(output)

        await model_client.close()

    asyncio.run(main=main())
