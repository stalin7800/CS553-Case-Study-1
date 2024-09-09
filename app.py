import gradio as gr
from huggingface_hub import InferenceClient
from transformers import pipeline
import torch
"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
localclient = pipeline("text-generation", "microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")

# load_dotenv()


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
    model,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    if model == "inference":

        for message in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            token = message.choices[0].delta.content

            response += token
            yield response
    else:
        response = localclient(
            message,
            max_length=max_tokens,
            temperature=temperature,
            top_k=0,
            top_p=top_p,
        )[0]["generated_text"]

        yield response

"""

# WELCOME TO THE APP

you bad

"""

# with gr.Blocks() as block:
#     gr.Markdown(
#         """
#         # Welcome to the Chatbot App!
#         This is a simple chatbot that uses the Zephyr-7B model from Hugging Face. 
#         The chatbot can respond to your messages and generate new text based on your input. 
#         You can also provide a system message, set the maximum number of tokens to generate, and adjust the temperature and top-p sampling parameters.
#         """
#     )
    

css = """
<style>




</style>


"""


with gr.Blocks() as demo:

    gr.Markdown(
        '''
    # Welcome to APp


    '''
    )

    gr.ChatInterface(


        respond,
        additional_inputs=[
            gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
            gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
            gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
            gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.95,
                step=0.05,
                label="Top-p (nucleus sampling)",
            ),
            gr.Checkbox(label='Use Local Model', value=False),


        ],
    )





if __name__ == "__main__":
    demo.launch()