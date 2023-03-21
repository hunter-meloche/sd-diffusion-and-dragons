import re
import openai
import gradio as gr
from modules import script_callbacks
from modules import generation_parameters_copypaste as params_copypaste

# Replace 'placeYourKeyHere' with your actual API key
openai.api_key = "placeYourKeyHere"

def generate_description(text: str):
    description = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "system", "content": \
      "You are a skilled fantasy author that writes extremely detailed descriptions. \
      You will generate descriptions based on user input. \
      Your response should contain ONLY the description of the user input. \
      Do NOT respond with text like 'Write a description of a'."}, \
      {"role": "user", "content": \
      f"Please write a detailed description that describes {text}. \
      The written descriptions is meant to be read aloud to an audience. \
      Do NOT say anything that does not have to do with the description of the input. \
      An example of what NOT to say is 'The description for the treasure chest is as follows:' \
      Only provide the description. \
      Do NOT give it direct commands like 'Write a description'. \
      Instead only describe the subject with your writing."}]
    )

    return description.choices[0].message['content']

def generate_imgPrompt(text: str):
    imgPrompt = openai.ChatCompletion.create(
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
	
    return imgPrompt.choices[0].message['content'].replace(".", ",")

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as dnd_interface:
        with gr.Row():
            with gr.Column():
                tb_input = gr.Textbox(label='ChatGPT Input', interactive=True)
                with gr.Row():
                    btn_descGenerate = gr.Button(value='Generate Text Description', variant='primary')
                    btn_imgGenerate = gr.Button(value='Generate Image Prompt', variant='primary')
		
            with gr.Column():        
                with gr.Row():
                    tb_descOutput = gr.Textbox(label='Text Description', interactive=False)
                with gr.Row():
                    btn_desc2imgGenerate = gr.Button(value='Description -> Prompt', variant='primary')
                with gr.Row():
                    tb_imgOutput = gr.Textbox(label='Image Prompt', interactive=False)

        btn_descGenerate.click(
            fn=generate_description,
            inputs=tb_input,
            outputs=tb_descOutput
	)
                
        btn_imgGenerate.click(
            fn=generate_imgPrompt,
            inputs=tb_input,
            outputs=tb_imgOutput
        )
                
        btn_desc2imgGenerate.click(
            fn=generate_imgPrompt,
            inputs=tb_descOutput,
            outputs=tb_imgOutput
        )
        
    return [(dnd_interface, "DnD", "dnd_interface")]


script_callbacks.on_ui_tabs(on_ui_tabs)
