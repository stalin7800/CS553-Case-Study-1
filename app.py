import gradio as gr
from huggingface_hub import InferenceClient
from transformers import pipeline
import torch
from prometheus_client import start_http_server, Summary, Counter, Gauge

REQUEST_COUNTER = Counter('request_counter', 'Number of requests')
SUCCESS_COUNTER = Counter('success_counter', 'Number of successful requests')
FAILURE_COUNTER = Counter('failure_counter', 'Number of failed requests')
DURATION = Summary('request_latency_seconds', 'Request latency in seconds')
API_CALLS = Counter('api_calls', 'Number of API calls')
LOCAL_CALLS = Counter('local_calls', 'Number of local calls')


#used reference from 
"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
#localclient = pipeline("text-generation", "microsoft/Phi-3-mini-4k-instruct", torch_dtype=torch.bfloat16, device_map="auto")

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

    REQUEST_COUNTER.inc()
    request_timer = DURATION.time()
    
    try:
        response_html = ''
        messages = [{"role": "system", "content": system_message}]
    
        for val in history:
            if val[0]:
                messages.append({"role": "user", "content": val[0]})
                response_html += f'<div class="user">{val[0]}</div>'
    
            if val[1]:
                messages.append({"role": "assistant", "content": val[1]})
                response_html += f'<div class="assistant">{val[1]}</div>'
    
        messages.append({"role": "user", "content": message})
    
        response = ""
    
        if not model:
    
            for message in client.chat_completion(
                messages,
                max_tokens=max_tokens,
                stream=True,
                temperature=temperature,
                top_p=top_p,
            ):
                token = message.choices[0].delta.content
    
                response += token

                API_CALLS.inc()
                yield response
        #else:
          #  response = ''
    
           # for message in localclient(message, max_length=max_tokens, temperature=temperature, top_p=top_p):
           #     response += message['generated_text']
                
          #  LOCAL_CALLS.inc()
          #  yield response_html + response
        SUCCESS_COUNTER.inc()
    except Exception as e:
        FAILURE_COUNTER.inc()
        yield f"An error occured: {e}"
    finally:
        request_timer.observe_duration()

def test_respond():
    test = respond('Hello!',[],'You only respond hello.',5,1,1.5,False)
    
    with open('log.txt','w') as f:
        f.write(f'{type(test)}\n')

    assert type(test) == dict





css = """

body, #root, .gradio-container {
    background-color: #C4122E !important;
    color: white;
}

#logo {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
}

"""


with gr.Blocks(css=css) as demo:

    # Add logo at the top left corner
    with gr.Row():
        gr.Image(
            value="wpilogo.png",  # Replace with the path or URL to your logo image
            label=None,
            elem_id="logo",
            width=50,  # Adjust size as needed
        )
    
    gr.Markdown(
        '''
    # Welcome to  the WPI ChatBot!

    This is a simple chatbot that uses the Zephyr-7B model from Hugging Face.
    The chatbot can respond to your messages and generate new text based on your input.
    You can also provide a system message, set the maximum number of tokens to generate, and adjust the temperature and top-p sampling parameters.
    The purpose of this chatbot is to aid WPI students with all questions related to WPI. This can range from degree requirements to student clubs.

    Have Fun!


    '''
    )

    gr.ChatInterface(


        respond,
        additional_inputs=[
            gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
            gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens: Length of response"),
            gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature: Creativeness of the response"),
            gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.95,
                step=0.05,
                label="Top-p (nucleus sampling): Diversity of next token",
            ),
            gr.Checkbox(label='Use Local Model', value=False),


        ],

    )





if __name__ == "__main__":
    start_http_server(8000)
    demo.launch(share = False)
