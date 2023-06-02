import argparse
import os
import glob
import shutil
from scripts.generator import data_parse_template

template_path = "./templates"
generated_template_path = "./generated_templates"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--move-generated", action="store_true", default=False, help="Move generated templates flag.")
    parser.add_argument("--prompt-count-multiplier", type=int, default=1, help="Prompt count multiplier.")
    parser.add_argument("--max-prompt-count", type=int, default=1000, help="Maximum prompt count per output prompt file.")

    args = parser.parse_args()

    if not_positive_integer(args.prompt_count_multiplier):
        args.prompt_count_multiplier = 1

    if not_positive_integer(args.max_prompt_count):
        args.max_prompt_count = 1000

    print(f"Move Generated Prompt Templates (to {generated_template_path}): {args.move_generated}")
    print(f"Prompt Count Multiplier: {args.prompt_count_multiplier}")
    print(f"Maximum Prompt Count (per file): {args.max_prompt_count}")

    template_list = create_template_list(args.move_generated)

    for template in template_list:
        data_parse_template(template, args.prompt_count_multiplier, args.max_prompt_count)

def create_template_list(move_generated):
    if move_generated:
        os.makedirs(generated_template_path, exist_ok=True)

    template_files = glob.glob(os.path.join(template_path, "*.txt"))
    template_list = []
    
    for template_file in template_files:
        with open(template_file, 'r') as os_file:
            template = os_file.read()
            print(f"Template in {template_file}:", template)
            template_list.append(template)
        os_file.close
        if move_generated:
            shutil.move(template_file, generated_template_path)


    return template_list

def not_positive_integer(var):
    if isinstance(var, int) and var > 0:
        return False
    return True

if __name__ == "__main__":
    main()

