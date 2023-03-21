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
      messages=[{"role": "system", "content": \
      "You are a helpful assistant that creates extremely detailed prompts for stable diffusion. \
      You will generate prompts based on user input. \
      Please separate descriptors by comma. \
      Your response should contain ONLY the image generation prompt and NO explanation. \
      Do NOT respond with text like 'Generate an image of a'."}, \
      {"role": "user", "content": \
      f"Please create a detailed prompt for stable diffusion that describes {text}. \
      The generated prompt is not meant to be read by humans. \
      It is meant to be input into stable diffusion to generate an image. \
      Please separate descriptors by comma. \
      Do NOT say anything that does not have to do with the actual prompt. \
      An example of what NOT to say is 'The prompt for stable diffusion to generate an image of golden dragon is as follows:' \
      Only provide the prompt. \
      Do NOT give it direct commands like 'Generate an image'. \
      Instead only describe the subject with your prompt."}]
    )
	
    return completion.choices[0].message['content']

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as dnd_interface:
        with gr.Row():
            with gr.Column():
                tb_input = gr.Textbox(label='ChatGPT Input', interactive=True)
                btn_descGenerate = gr.Button(value='Generate Text Description', variant='primary')
		btn_imgGenerate = gr.Button(value='Generate Image Prompt', variant='primary')
		
	    with gr.Column():        
                with gr.Row():
                    tb_descOutput = gr.Textbox(label='Text Description', interactive=False)
		with gr.Row():
		    btn_desc2imgGenerate = gr.Button(value='Description -> Prompt', variant='primary')
                with gr.Row():
                    tb_imgOutput = gr.Textbox(label='Image Prompt', interactive=False)

        btn_imgGenerate.click(
            fn=generate_prompt,
            inputs=[
                tb_input
            ],
            outputs=tb_imgOutput
        )
        
    return [(dnd_interface, "DnD", "dnd_interface")]


script_callbacks.on_ui_tabs(on_ui_tabs)
