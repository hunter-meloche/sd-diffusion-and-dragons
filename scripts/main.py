import re
import openai
import gradio as gr
from modules import script_callbacks
from modules import generation_parameters_copypaste as params_copypaste

def generate_prompt(text: str):
    # Replace 'placeYourKeyHere' with your actual API key
    openai.api_key = "placeYourKeyHere"

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": f"Please create a detailed prompt for stable diffusion that describes {text}. \
      The generated prompt is not meant to be read by humans. It is meant to be input into stable diffusion to generate an image. \
      Please separate descriptors by comma. Do NOT say anything that does not have to do with the actual prompt. \
      An example of what NOT to say is 'The prompt for stable diffusion to generate an image of golden dragon is as follows:' \
      Only provide the prompt. Do NOT give it direct commands like 'Generate an image'. Instead only describe the subject with your prompt. \
      There should not be any new lines or text outside of the prompt. You should only create one paragraph."}]
    )
	
    return completion.choices[0].message['content']

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as dungeonAI_interface:
        with gr.Row():
            with gr.Column():
                tb_input = gr.Textbox(label='ChatGPT Input', interactive=True)
                btn_generate = gr.Button(value='Generate', variant='primary')
                tb_output = gr.Textbox(label='Output', interactive=False)           

        btn_generate.click(
            fn=generate_prompt,
            inputs=[
                tb_input
            ],
            outputs=tb_output
        )
        
    return [(dungeonAI_interface, "dungeonAI", "dungeonAI_interface")]


script_callbacks.on_ui_tabs(on_ui_tabs)
