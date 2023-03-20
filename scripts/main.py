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
      messages=[{"role": "system", "content": "You are a helpful assistant. \
      You will generate Stable Diffusion image generation prompts based on user input. \
      Your response should contain ONLY the image generation prompt and NO explanation. \
      Do NOT ever use periods to seperate sentences, instead use ,."}, \
      {"role": "user", "content": f"{text}"}]
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
