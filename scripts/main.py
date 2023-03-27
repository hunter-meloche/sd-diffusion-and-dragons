import os
import openai
import gradio as gr
import numpy as np
from modules import script_callbacks, generation_parameters_copypaste, ui
import modules.shared as shared
from modules.shared import opts, cmd_opts, restricted_opts
from modules.sd_samplers import samplers
from modules.paths import script_path, data_path
from modules.ui_components import FormRow, FormGroup, ToolButton, FormHTML
from modules.call_queue import wrap_gradio_gpu_call, wrap_queued_call, wrap_gradio_call
import modules.generation_parameters_copypaste as parameters_copypaste
import modules.interrogate as interrogate
from modules.ui import create_output_panel
import modules.scripts
from PIL import Image

#Using constants for these since the variation selector isn't visible.
# Important that they exactly match script.js for tooltip to work.
random_symbol = '\U0001f3b2\ufe0f'  # 🎲️
reuse_symbol = '\u267b\ufe0f'  # ♻️
paste_symbol = '\u2199\ufe0f'  # ↙
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
apply_style_symbol = '\U0001f4cb'  # 📋
clear_prompt_symbol = '\U0001F5D1'  # 🗑️
extra_networks_symbol = '\U0001F3B4'  # 🎴
switch_values_symbol = '\U000021C5' # ⇅

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

def generate_imgDescription(gallery):
    openai.api_key = read_key_value()
    print(gallery[0]['name'])
    image = Image.open(gallery[0]['name'])
    prompt = shared.interrogator.interrogate(image.convert("RGB"))
    return prompt

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False, css=".gradio-output-image img {height: 1024px;object-fit: contain;max-width: 100%;}") as dnd_interface:
    
        txt2img_prompt, txt2img_prompt_styles, txt2img_negative_prompt, submit, _, _, txt2img_prompt_style_apply, txt2img_save_style, txt2img_paste, extra_networks_button, token_counter, token_button, negative_token_counter, negative_token_button = ui.create_toprow(is_img2img=False)
        dummy_component = gr.Label(visible=False)
        txt_prompt_img = gr.File(label="", elem_id="txt2img_prompt_image", file_count="single", type="binary", visible=False)

        with FormRow(variant='compact', elem_id="txt2img_extra_networks", visible=False) as extra_networks:
            from modules import ui_extra_networks
            extra_networks_ui = ui_extra_networks.create_ui(extra_networks, extra_networks_button, 'txt2img')

        with gr.Row():
            with gr.Column(scale=6):
                tb_input = gr.Textbox(label='ChatGPT Input', interactive=True)
                with gr.Row():
                    btn_imgGenerate = gr.Button(value='Generate Image Prompt', variant='primary')
                with gr.Row():
                    btn_img2descGenerate = gr.Button(value='Image -> Description', elem_id="interrogate", variant='primary')
                with gr.Row():
                    tb_descOutput = gr.Textbox(label='Text Description', interactive=True, lines=3)
                with gr.Row():
                    btn_descGenerate = gr.Button(value='Generate Text Description', variant='primary')
                with gr.Row():
                    btn_desc2imgGenerate = gr.Button(value='Description -> Prompt', variant='primary')
                with gr.Row():
                    tb_apiKey = gr.Textbox(label='openAI API Key', interactive=True)
                    btn_saveApiKey = gr.Button(value='Save API Key')
                with gr.Row().style(equal_height=False):
                    with gr.Column(variant='compact', elem_id="txt2img_settings"):
                        for category in ui.ordered_ui_categories():
                            if category == "sampler":
                                steps, sampler_index = ui.create_sampler_and_steps_selection(samplers, "DnD")

                            elif category == "dimensions":
                                with FormRow():
                                    with gr.Column(elem_id="DnD_column_size", scale=4):
                                        width = gr.Slider(minimum=64, maximum=2048, step=8, label="Width", value=512, elem_id="DnD_width")
                                        height = gr.Slider(minimum=64, maximum=2048, step=8, label="Height", value=512, elem_id="DnD_height")

                                    res_switch_btn = ToolButton(value=switch_values_symbol, elem_id="DnD_res_switch_btn")
                                    if opts.dimensions_and_batch_together:
                                        with gr.Column(elem_id="DnD_column_batch"):
                                            batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="DnD_batch_count")
                                            batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="DnD_batch_size")

                            elif category == "cfg":
                                cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0, elem_id="DnD_cfg_scale")

                            elif category == "seed":
                                seed, reuse_seed, subseed, reuse_subseed, subseed_strength, seed_resize_from_h, seed_resize_from_w, seed_checkbox = ui.create_seed_inputs('DnD')

                            elif category == "checkboxes":
                                with FormRow(elem_id="DnD_checkboxes", variant="compact"):
                                    restore_faces = gr.Checkbox(label='Restore faces', value=False, visible=len(shared.face_restorers) > 1, elem_id="DnD_restore_faces")
                                    tiling = gr.Checkbox(label='Tiling', value=False, elem_id="DnD_tiling")
                                    enable_hr = gr.Checkbox(label='Hires. fix', value=False, elem_id="txt2img_enable_hr")
                                    hr_final_resolution = FormHTML(value="", elem_id="txtimg_hr_finalres", label="Upscaled resolution", interactive=False)

                            elif category == "hires_fix":
                                with FormGroup(visible=False, elem_id="txt2img_hires_fix") as hr_options:
                                    with FormRow(elem_id="txt2img_hires_fix_row1", variant="compact"):
                                        hr_upscaler = gr.Dropdown(label="Upscaler", elem_id="txt2img_hr_upscaler", choices=[*shared.latent_upscale_modes, *[x.name for x in shared.sd_upscalers]], value=shared.latent_upscale_default_mode)
                                        hr_second_pass_steps = gr.Slider(minimum=0, maximum=150, step=1, label='Hires steps', value=0, elem_id="txt2img_hires_steps")
                                        denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.7, elem_id="txt2img_denoising_strength")

                                    with FormRow(elem_id="txt2img_hires_fix_row2", variant="compact"):
                                        hr_scale = gr.Slider(minimum=1.0, maximum=4.0, step=0.05, label="Upscale by", value=2.0, elem_id="txt2img_hr_scale")
                                        hr_resize_x = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize width to", value=0, elem_id="txt2img_hr_resize_x")
                                        hr_resize_y = gr.Slider(minimum=0, maximum=2048, step=8, label="Resize height to", value=0, elem_id="txt2img_hr_resize_y")

                            elif category == "batch":
                                if not opts.dimensions_and_batch_together:
                                    with FormRow(elem_id="DnD_column_batch"):
                                        batch_count = gr.Slider(minimum=1, step=1, label='Batch count', value=1, elem_id="DnD_batch_count")
                                        batch_size = gr.Slider(minimum=1, maximum=8, step=1, label='Batch size', value=1, elem_id="DnD_batch_size")

                            elif category == "override_settings":
                                with FormRow(elem_id="DnD_override_settings_row") as row:
                                    override_settings = ui.create_override_settings_dropdown('DnD', row)

                            elif category == "scripts":
                                with FormGroup(elem_id="DnD_script_container"):
                                    custom_inputs = modules.scripts.scripts_txt2img.setup_ui()

                hr_resolution_preview_inputs = [enable_hr, width, height, hr_scale, hr_resize_x, hr_resize_y]
                for input in hr_resolution_preview_inputs:
                    input.change(
                        fn=ui.calc_resolution_hires,
                        inputs=hr_resolution_preview_inputs,
                        outputs=[hr_final_resolution],
                        show_progress=True,
                    )
                    input.change(
                        None,
                        _js="onCalcResolutionHires",
                        inputs=hr_resolution_preview_inputs,
                        outputs=[],
                        show_progress=True,
                    )
            with gr.Column(scale=10, elem_id="DnD_settings"):
                DnD_gallery, generation_info, html_info, html_log = create_output_panel("DnD", opts.outdir_txt2img_samples)

            ui.connect_reuse_seed(seed, reuse_seed, generation_info, dummy_component, is_subseed=False)
            ui.connect_reuse_seed(subseed, reuse_subseed, generation_info, dummy_component, is_subseed=True)

            txt2img_args = dict(
                fn=wrap_gradio_gpu_call(modules.txt2img.txt2img, extra_outputs=[None, '', '']),
                _js="submit",
                inputs=[
                    dummy_component,
                    txt2img_prompt,
                    txt2img_negative_prompt,
                    txt2img_prompt_styles,
                    steps,
                    sampler_index,
                    restore_faces,
                    tiling,
                    batch_count,
                    batch_size,
                    cfg_scale,
                    seed,
                    subseed, subseed_strength, seed_resize_from_h, seed_resize_from_w, seed_checkbox,
                    height,
                    width,
                    enable_hr,
                    denoising_strength,
                    hr_scale,
                    hr_upscaler,
                    hr_second_pass_steps,
                    hr_resize_x,
                    hr_resize_y,
                    override_settings,
                ] + custom_inputs,

                outputs=[
                    DnD_gallery,
                    generation_info,
                    html_info,
                    html_log,
                ],
                show_progress=True,
            )

            res_switch_btn.click(lambda w, h: (h, w), inputs=[width, height], outputs=[width, height])

            txt_prompt_img.change(
                fn=modules.images.image_data,
                inputs=[
                    txt_prompt_img
                ],
                outputs=[
                    txt2img_prompt,
                    txt_prompt_img
                ]
            )

            enable_hr.change(
                fn=lambda x: ui.gr_show(x),
                inputs=[enable_hr],
                outputs=[hr_options],
                show_progress = True,
            )

            txt2img_paste_fields = [
                (txt2img_prompt, "Prompt"),
                (txt2img_negative_prompt, "Negative prompt"),
                (steps, "Steps"),
                (sampler_index, "Sampler"),
                (restore_faces, "Face restoration"),
                (cfg_scale, "CFG scale"),
                (seed, "Seed"),
                (width, "Size-1"),
                (height, "Size-2"),
                (batch_size, "Batch size"),
                (subseed, "Variation seed"),
                (subseed_strength, "Variation seed strength"),
                (seed_resize_from_w, "Seed resize from-1"),
                (seed_resize_from_h, "Seed resize from-2"),
                (denoising_strength, "Denoising strength"),
                (enable_hr, lambda d: "Denoising strength" in d),
                (hr_options, lambda d: gr.Row.update(visible="Denoising strength" in d)),
                (hr_scale, "Hires upscale"),
                (hr_upscaler, "Hires upscaler"),
                (hr_second_pass_steps, "Hires steps"),
                (hr_resize_x, "Hires resize-1"),
                (hr_resize_y, "Hires resize-2"),
                *modules.scripts.scripts_txt2img.infotext_fields
            ]
            parameters_copypaste.add_paste_fields("txt2img", None, txt2img_paste_fields, override_settings)
            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                paste_button=txt2img_paste, tabname="txt2img", source_text_component=txt2img_prompt, source_image_component=None,
            ))

            txt2img_preview_params = [
                txt2img_prompt,
                txt2img_negative_prompt,
                steps,
                sampler_index,
                cfg_scale,
                seed,
                width,
                height,
            ]

            token_button.click(fn=wrap_queued_call(ui.update_token_counter), inputs=[txt2img_prompt, steps], outputs=[token_counter])
            negative_token_button.click(fn=wrap_queued_call(ui.update_token_counter), inputs=[txt2img_negative_prompt, steps], outputs=[negative_token_counter])					

            ui_extra_networks.setup_ui(extra_networks_ui, DnD_gallery)
            
        modules.scripts.scripts_current = modules.scripts.scripts_img2img
        modules.scripts.scripts_img2img.initialize_scripts(is_img2img=True)

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
            outputs=txt2img_prompt
        )
                
        btn_desc2imgGenerate.click(
            fn=generate_imgPrompt,
            inputs=tb_descOutput,
            outputs=txt2img_prompt
        )
        
        txt2img_prompt.submit(**txt2img_args)
        submit.click(**txt2img_args)
        
        btn_img2descGenerate.click(
                fn=generate_imgDescription,
                inputs=DnD_gallery,
                outputs=tb_descOutput
        )
        
    return [(dnd_interface, "DnD", "dnd_interface")]


script_callbacks.on_ui_tabs(on_ui_tabs)
