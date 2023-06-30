import json
import gradio as gr
import scripts.generator as spg

keywords = spg.load_data()

def reload_data():
    global keywords
    keywords = spg.load_data()
    return gr.Dropdown.update(choices=list(keywords))

def get_keyword_values(keyword):
    if keyword in keywords:
        values = keywords[keyword]
    else:
        values = []

    result = "\r\n- ".join(values)
    result = f"""### {len(values)} values:\r\n- {result}"""
    
    return result

def append_main_keyword(template_value, keyword):
    if keyword in keywords:
        value = f"#{str(keyword)}#"
    else:
        value = ""

    return template_value + " " + value

def append_random_keyword(template_value, keyword):
    if keyword in keywords:
        value = f"%{str(keyword)}%"
    else:
        value = ""

    return template_value + " " + value

def generate_test_output(template_value):
    prompt, main_keyword_list, random_keyword_list = spg.data_parse_test(keywords, template_value)

    total_prompt_count = 1
    main_keyword_list_with_length = []
    for main_keyword in main_keyword_list:
        if main_keyword in keywords:
            values = keywords[main_keyword]
            main_keyword_list_with_length.append(f"{main_keyword} ({len(values)})")
        else:
            values = ["dummy"]
            main_keyword_list_with_length.append(f"{main_keyword} (?)")

        total_prompt_count = total_prompt_count * len(values)
        
    total_prompts_value = f"""<h3><span><em>Total Prompt Count: {total_prompt_count} x Prompt Count Multiplier</em></span></h3>"""

    main_keywords_value = "\r\n- ".join(main_keyword_list_with_length)
    main_keywords_value = f"""### Main Keywords:\r\n- {main_keywords_value}"""

    random_keywords_value = "\r\n- ".join(random_keyword_list)
    random_keywords_value = f"""### Random Keywords:\r\n- {random_keywords_value}"""

    return prompt, total_prompts_value, main_keywords_value, random_keywords_value

def generate_prompts(template_value, prompt_count_multiplier_value, max_prompt_count_value):
    gen_main_keyword_list, gen_random_keyword_list, text_prompts_length, prompt_list_chunks_length, created_file_list = spg.data_parse_template(keywords, template_value, int(prompt_count_multiplier_value), int(max_prompt_count_value), None, True)

    created_file_value = "\r\n- ".join(created_file_list)
    created_file_value = f""" Main keywords": {gen_main_keyword_list}
    Random keywords: {gen_random_keyword_list}
    Generated Prompt Count: {text_prompts_length}
    File Count: {prompt_list_chunks_length}
    Output Files:
    - {created_file_value}
    """

    return created_file_value

template = None
with gr.Blocks() as spg_interface:
    with gr.Row():
        gr.Markdown("""# Simple Prompt Generator""")
    with gr.Row().style(equal_height=False):
        with gr.Column(variant="panel"):
            gr.HTML(value="<span class='hh'>Data</span>")
            reload_button = gr.Button("Reload Keywords")
            keyword_combobox = gr.Dropdown(choices=list(keywords), label="Select Keyword")
            reload_button.click(fn=reload_data, inputs=[], outputs=[keyword_combobox])
            with gr.Row().style(equal_height=False):
                main_button = gr.Button("Main (All Values)")
                random_button = gr.Button("Random (Random Values)")
            keyword_values = gr.Markdown()
            keyword_combobox.change(get_keyword_values, keyword_combobox, keyword_values)
        with gr.Column(variant="panel"):
            gr.HTML(value="<span class='hh'>Template</span>")
            template = gr.Textbox(lines=5, label="Template")
            main_button.click(fn=append_main_keyword, inputs=[template, keyword_combobox], outputs=template)
            random_button.click(fn=append_random_keyword, inputs=[template, keyword_combobox], outputs=template)
            test_button = gr.Button("Test Template")
            test_prompt = gr.Textbox(lines=5, label="Test Prompt")
            total_prompts = gr.Markdown()
            with gr.Row().style(equal_height=False):
                main_keywords = gr.Markdown()
                random_keywords = gr.Markdown()
            test_button.click(fn=generate_test_output, inputs=[template], outputs=[test_prompt, total_prompts, main_keywords, random_keywords])
        with gr.Column(variant="panel"):
            gr.HTML(value="<span class='hh'>Output</span>")
            prompt_count_multiplier = gr.Slider(minimum=1, maximum=50, value=int(1), label="Prompt Count Multiplier", step=int(1))
            max_prompt_count = gr.Slider(minimum=1, maximum=10000, value=int(500), label="Maximum Prompt Count (per file)", step=int(10))
            generate_button = gr.Button("Generate Prompts")
            output_files = gr.Markdown()
            generate_button.click(fn=generate_prompts, inputs=[template, prompt_count_multiplier, max_prompt_count], outputs=[output_files])
            
spg_interface.launch(share=False, server_port=9393)