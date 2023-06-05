import json, random, re
from itertools import product
from datetime import datetime
from pathlib import Path

def data_parse_template(template, prompt_count_multiplier, max_prompt_count, shuffled):
    data_file = load_data()
    
    prompt = ''
    prompt_list = []
    final_prompt_list = []
    
    main_keyword_list = re.findall(r"#([^#]+)#",template)
    print("Main keywords", main_keyword_list)
            
    combinations = list(product(*[data_file[main_keyword] for main_keyword in main_keyword_list]))
    
    for p in range(prompt_count_multiplier):
        for combination in combinations:
            prompt = template
            for key, value in zip(main_keyword_list, combination):
                prompt = prompt.replace(f"#{key}#", value)
            prompt_list.append(prompt)

    random_keyword_list = re.findall(r"%([^%]+)%",template)
    print("Random keywords:", random_keyword_list)
    
    for prompt_instance in prompt_list:
        final_prompt = prompt_instance
        for random_keyword in random_keyword_list:
            keyword = f'%{random_keyword}%'
            final_prompt = final_prompt.replace(keyword, random.choice(data_file[random_keyword]), 1)
            
        final_prompt_list.append(final_prompt)
          
    write_file(final_prompt_list, create_file_name(main_keyword_list, random_keyword_list), max_prompt_count, shuffled)

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
    
def write_file(text_prompts, file_name, max_prompt_count, shuffled):
    print("Prompt Count:", len(text_prompts))
    print("Max. Prompt Count:", max_prompt_count)
        
    prompt_list_chunks = list(divide_prompts(text_prompts, max_prompt_count))
    
    print("File Count:", len(prompt_list_chunks))
    
    prompt_path = "./prompt_files/"
    Path(prompt_path).mkdir(parents=True, exist_ok=True)

    for prompt_chunk in prompt_list_chunks:
        shuffled_chunk = shuffle_prompts(prompt_chunk, shuffled)
        time_string = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        file_to_create = prompt_path + file_name + "#" + time_string + '.txt'
        with open(file_to_create, "w", encoding = "utf-8") as output_file:
            output_file.writelines(shuffled_chunk)
        print("Prompt file", file_to_create, "created.")