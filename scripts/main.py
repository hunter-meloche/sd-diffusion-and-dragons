import os
import openai
import gradio as gr
from modules import script_callbacks, generation_parameters_copypaste, ui

KEY_PATH = req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".openai")
KEY = "openAI_API_key"

def read_key_value():
    result = None
    try:
        with open(KEY_PATH, 'r') as file:
            for line in file:
                if line.startswith(KEY):
                    result = line.split('=')[1].strip()
                    break
    except FileNotFoundError:
        print(f"File {KEY_PATH} not found.")
    except IndexError:
        print(f"Key '{KEY}' not found in the file.")
    return result

def write_apiKey(text: str):
    try:
        with open(KEY_PATH, 'w') as file:
            file.write(f"{KEY}={text}")
    except Exception as e:
        print(f"Error writing openAI API key to file: {e}")
    return ""

def find_prompts(fields):
    field_prompt = [x for x in fields if x[1] == "Prompt"][0]
    field_negative_prompt = [x for x in fields if x[1] == "Negative prompt"][0]
    return [field_prompt[0], field_negative_prompt[0]]

def send_prompts(text: str):
    params = generation_parameters_copypaste.parse_generation_parameters(text)
    negative_prompt = params.get("Negative prompt", "")
    return params.get("Prompt", ""), negative_prompt or gr.update()

def generate_description(text: str):
    openai.api_key = read_key_value()
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
    openai.api_key = read_key_value()
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
            with gr.Column(scale=5):
                tb_input = gr.Textbox(label='ChatGPT Input', interactive=True)
                with gr.Row():
                    btn_descGenerate = gr.Button(value='Generate Text Description', variant='primary')
                    btn_imgGenerate = gr.Button(value='Generate Image Prompt', variant='primary')
                with gr.Row():
                    tb_apiKey = gr.Textbox(label='openAI API Key', interactive=True)
                    btn_saveApiKey = gr.Button(value='Save API Key')
            with gr.Column(scale=1):
                ta_info = gr.TextArea(label='Info', value='Diffusion and Dragons:\n\nCreate a textual description to read aloud to your players and generate detailed visual aids.\n\nResults are geared towards fantasy, but can easily be used for other genres.')
            with gr.Column(scale=10):        
                with gr.Row():
                    tb_descOutput = gr.Textbox(label='Text Description', interactive=True, lines=3)
                with gr.Row():
                    with gr.Column():
                        blank1 = gr.Button(visible=False)
                    with gr.Column():
                        btn_desc2imgGenerate = gr.Button(value='Description -> Prompt', variant='primary')
                    with gr.Column():
                        blank2 = gr.Button(visible=False)
                with gr.Row():
                    tb_imgOutput = gr.Textbox(label='Image Prompt', interactive=True)
                with gr.Row():
                    btn_sendTxt2img = gr.Button(value='Send to txt2img')
                    btn_sendImg2img = gr.Button(value='Send to img2img')

        btn_saveApiKey.click(
            fn=write_apiKey,
            inputs=tb_apiKey,
            outputs=tb_apiKey
	)
                
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
        
        btn_sendTxt2img.click(
            fn=send_prompts,
            _js=f"switch_to_txt2img",
            inputs=[tb_imgOutput],
            outputs=find_prompts(ui.txt2img_paste_fields)
        )
        
        btn_sendImg2img.click(
            fn=send_prompts,
            _js=f"switch_to_img2img",
            inputs=[tb_imgOutput],
            outputs=find_prompts(ui.img2img_paste_fields)
        )
        
    return [(dnd_interface, "DnD", "dnd_interface")]


script_callbacks.on_ui_tabs(on_ui_tabs)
