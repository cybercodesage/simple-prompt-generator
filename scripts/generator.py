import json, random, re
from itertools import product
from datetime import datetime
from pathlib import Path

def data_parse_template(data_file, template, prompt_count_multiplier, max_prompt_count, shuffled, gui=False):
        
    prompt = ''
    prompt_list = []
    final_prompt_list = []
    
    main_keyword_list = re.findall(r"#([^#]+)#", template)
                
    combinations = list(product(*[data_file[main_keyword] for main_keyword in main_keyword_list]))
    
    for p in range(prompt_count_multiplier):
        for combination in combinations:
            prompt = template
            for key, value in zip(main_keyword_list, combination):
                prompt = prompt.replace(f"#{key}#", value)
            prompt_list.append(prompt)

    random_keyword_list = re.findall(r"%([^%]+)%", template)
        
    for prompt_instance in prompt_list:
        final_prompt = prompt_instance
        for random_keyword in random_keyword_list:
            keyword = f'%{random_keyword}%'
            final_prompt = final_prompt.replace(keyword, random.choice(data_file[random_keyword]), 1)
            
        final_prompt_list.append(final_prompt)

    if (gui):
        text_prompts_length, prompt_list_chunks_length, created_file_list = write_file(final_prompt_list, create_file_name(main_keyword_list, random_keyword_list), max_prompt_count, shuffled, template)
    else:
        text_prompts_length, prompt_list_chunks_length, created_file_list = write_file(final_prompt_list, create_file_name(main_keyword_list, random_keyword_list), max_prompt_count, shuffled)

    return main_keyword_list, random_keyword_list, text_prompts_length, prompt_list_chunks_length, created_file_list

def data_parse_test(data_file, template):
    main_keyword_list = re.findall(r"#([^#]+)#", template)
    random_keyword_list = re.findall(r"%([^%]+)%", template)
               
    prompt = template

    for main_keyword in main_keyword_list:
        prompt = prompt.replace(f"#{main_keyword}#", random.choice(data_file[main_keyword]), 1)

    for random_keyword in random_keyword_list:
        prompt = prompt.replace(f"%{random_keyword}%", random.choice(data_file[random_keyword]), 1)

    return prompt, main_keyword_list, random_keyword_list


def divide_prompts(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def load_data():
    with open('./data/data.json', 'r', encoding = "utf8") as os_file:
        data_file = json.loads(os_file.read())
    return data_file
    
def create_file_name(main_keyword_list, random_keyword_list):
    main_keyword_string = ""
    random_keyword_string = ""
    if len(main_keyword_list) > 0:
        main_keyword_string = "_".join(main_keyword_list)
    if len(random_keyword_list) > 0:
        random_keyword_string = "_".join(random_keyword_list)
       
    if main_keyword_string and random_keyword_string:
        return main_keyword_string + "#" + random_keyword_string
    elif main_keyword_string:
        return main_keyword_string
    elif random_keyword_string:
        return random_keyword_string
    else:
        return "prompt_file"
    
def shuffle_prompts(prompt_list, shuffled):
    shuffled_prompts = []
    for prompt in prompt_list:
        shuffled_prompts.append(prompt + "\n")
        shuffled_prompts_sub = []
        if shuffled:
            parts = prompt.split(", ")
            for i in range(shuffled):
                random.shuffle(parts)
                shuffled_prompt = ", ".join(parts)
                shuffled_prompts_sub.append(shuffled_prompt + "\n")
            shuffled_prompts.extend(shuffled_prompts_sub)
    return shuffled_prompts
    
def write_file(text_prompts, file_name, max_prompt_count, shuffled, template=None):   
    prompt_list_chunks = list(divide_prompts(text_prompts, max_prompt_count))
    
    prompt_path = "./prompt_files/"
    Path(prompt_path).mkdir(parents=True, exist_ok=True)

    if template:
        generated_template_path = "./generated_templates/"
        Path(generated_template_path).mkdir(parents=True, exist_ok=True)
        template_file_to_create = generated_template_path + file_name + "-template.txt"
        with open(template_file_to_create, "w", encoding = "utf-8") as template_output_file:
            template_output_file.writelines(template)
            template_output_file.close()

    created_file_list = []
    for prompt_chunk in prompt_list_chunks:
        shuffled_chunk = shuffle_prompts(prompt_chunk, shuffled)
        time_string = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        file_to_create = prompt_path + file_name + "#" + time_string + ".txt"
        with open(file_to_create, "w", encoding = "utf-8") as output_file:
            output_file.writelines(shuffled_chunk)
            output_file.close()
        created_file_list.append(file_to_create)

    return len(text_prompts), len(prompt_list_chunks), created_file_list