import chainlit as cl
import litellm

assert litellm.supports_function_calling(model="ollama/llama3.2") == True

@cl.on_chat_start
def start_chat():     
    system_message = {
        "role": "system",
        "content": "You are a helpful assistant who tries their best to answer questions."
    }
    cl.user_session.set("message_history", [system_message])

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    messages = cl.user_session.get("message_history")
    messages.append({
        "role": "user",
        "content": message.content
    })

    response = await litellm.acompletion(
        model='ollama/llama3.2', 
        messages=messages,
        stream=True
    )

    async for chunk in response:
        if chunk:
            content = chunk.choices[0].delta.content
            if content:
                await msg.stream_token(content)

    messages.append({
        "role": "assistant",
        "content": msg.content
    })

    await msg.update()