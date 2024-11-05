"""Pipeline."""
from typing import List
from datetime import datetime
import json
from functools import cached_property
from openai import AsyncOpenAI
from pydantic import BaseModel
from .message import Message, ChatHistory, Role
from .tools import (
    TOOL_CALL_MAP,
    LIST_AVAILABLE_SLOTS,
    BOOK_APPOINTMENT,
    SEARCH_FITNESS_INFORMATION
    )
from ..env_settings import OPENAI_API_KEY

class Pipeline(BaseModel):
    """"ML pipeline class."""
    @cached_property
    def openai_client(self) -> AsyncOpenAI:
        """OpenAI client."""
        return AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30,
            max_retries=2,
        )
    
    @cached_property
    def client_info(self) -> dict:
        """Client info."""
        return {
            'client_name': 'Jane Doe',
            'client_email': 'jane.doe@gmail.com'
        }

    async def tool_call(self, messages: ChatHistory) -> ChatHistory:
        """Call method for tool call."""
        completion = await (
            self
            .openai_client
            .chat
            .completions
            .create(
                messages=messages.render(
                    system_prompt_id='tool_call_system',
                    system_kwargs={
                        'date_time': datetime.now().strftime('%A, %Y-%m-%d %H:%M'),
                        **self.client_info
                    }
                    ),
                model='gpt-4o',
                temperature=0,
                top_p=1,
                max_tokens=512,
                tools=[LIST_AVAILABLE_SLOTS, BOOK_APPOINTMENT, SEARCH_FITNESS_INFORMATION],
            )
        )

        new_messages = messages

        if completion.choices[0].message.tool_calls:
            data = []
            for tool_call in completion.choices[0].message.tool_calls:
                fn_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                data.append(
                    (
                        fn_name,
                        await TOOL_CALL_MAP[fn_name](**arguments)
                        )
                    )
            msg = '\n'.join(f"{fn_name}: {result}" for fn_name, result in data)
            new_messages.append(
                Message(content=f"[TOOL CALLS]\n{msg}", role=Role.ASSISTANT)
                )
        else:
            new_messages.append(
                Message(
                    content=completion.choices[0].message.content,
                    role=Role.ASSISTANT
                    )
                )

        print(new_messages[-1].content)
        return new_messages

    async def summarization_call(self, messages: ChatHistory) -> ChatHistory:
        """Call method for summarization call."""
        completion = await (
            self
            .openai_client
            .chat
            .completions
            .create(
                messages=messages.render(
                    system_prompt_id='summarization_system',
                    system_kwargs={
                        'date_time': datetime.now().strftime('%A, %Y-%m-%d %H:%M'),
                        **self.client_info
                    }
                    ),
                model='gpt-4o',
                temperature=0,
                top_p=1,
                max_tokens=512,
            )
        )

        new_messages = messages

        new_messages.append(
            Message(
                content=completion.choices[0].message.content,
                role=Role.ASSISTANT
            )
        )

        return new_messages

    async def __call__(self, messages: List[Message]) -> Message:
        """Call method for pipeline."""
        history = ChatHistory(messages)

        # run tool call
        history = await self.tool_call(history)

        # if tool calls were ran, run summarization
        if '[TOOL CALLS]' in history[-1].content:
            history = await self.summarization_call(history.switch())

        return history[-1]
