import json

import gradio as gr
import nest_asyncio
from pydantic_ai.messages import ToolCallPart

from src.agents import question_agent

nest_asyncio.apply()


def messages_from_agent(prompt: str, chatbot: list[dict], past_messages: list):

    chatbot.append({"role": "user", "content": prompt})
    result = question_agent.run_sync(prompt, message_history=past_messages)
    for message in result.new_messages():
        for call in message.parts:
            if isinstance(call, ToolCallPart):
                call_args = (
                    call.args.args_json
                    if hasattr(call.args, "args_json")
                    else json.dumps(call.args)
                )
                metadata = {
                    "title": f"🛠️ Using {call.tool_name}",
                }

                gr_message = {
                    "role": "assistant",
                    "content": "Parameters: " + call_args,
                    "metadata": metadata,
                }
                chatbot.append(gr_message)

    response = result.data.response
    article_list = ", ".join(result.data.article_list)
    chatbot.append(
        {"role": "assistant", "content": f"{response}\n Links: {article_list}"}
    )
    past_messages = result.all_messages()
    return gr.Textbox(interactive=True), chatbot, past_messages


def handle_retry(chatbot, past_messages: list, retry_data: gr.RetryData):
    new_history = chatbot[: retry_data.index]
    previous_prompt = chatbot[retry_data.index]["content"]
    past_messages = past_messages[: retry_data.index]
    for update in messages_from_agent(previous_prompt, new_history, past_messages):
        return update


def undo(chatbot, past_messages: list, undo_data: gr.UndoData):
    new_history = chatbot[: undo_data.index]
    past_messages = past_messages[: undo_data.index]
    return chatbot[undo_data.index]["content"], new_history, past_messages


def select_data(message: gr.SelectData) -> str:
    return message.value["text"]


with gr.Blocks() as demo:
    gr.HTML(
        """
        <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; padding: 1rem; width: 100%">
            <img src="https://ai.pydantic.dev/img/logo-white.svg" style="max-width: 200px; height: auto">
            <div>
                <h1 style="margin: 0 0 1rem 0">Arxiv Assistant</h1>
                <h3 style="margin: 0 0 0.5rem 0">
                    This assistant answer your questions about Arxiv papers.
                </h3>
            </div>
        </div>
        """
    )

    past_messages = gr.State([])
    chatbot = gr.Chatbot(
        label="Packing Assistant",
        type="messages",
        avatar_images=(None, "https://ai.pydantic.dev/img/logo-white.svg"),
        examples=[
            {
                "text": "What is the relation between context length and accuracy for large language models?"
            },
        ],
    )
    with gr.Row():
        prompt = gr.Textbox(
            lines=1,
            show_label=False,
            placeholder="What is the relation between context length and accuracy for large language models?",
        )
    generation = prompt.submit(
        messages_from_agent,
        inputs=[prompt, chatbot, past_messages],
        outputs=[prompt, chatbot, past_messages],
    )
    chatbot.example_select(select_data, None, [prompt])
    chatbot.retry(
        handle_retry, [chatbot, past_messages], [prompt, chatbot, past_messages]
    )
    chatbot.undo(undo, [chatbot, past_messages], [prompt, chatbot, past_messages])


if __name__ == "__main__":
    demo.launch()
