import argparse
import os
import glob
import shutil
import scripts.generator as spg

template_path = "./templates"
generated_template_path = "./generated_templates"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--move-generated", action="store_true", default=False, help="Move generated templates flag.")
    parser.add_argument("--prompt-count-multiplier", type=int, default=1, help="Prompt count multiplier.")
    parser.add_argument("--max-prompt-count", type=int, default=1000, help="Maximum prompt count per output prompt file.")
    parser.add_argument("--shuffled", nargs="?", const=1, type=int, default=None, help="Specify the shuffle count (default: None).")

    args = parser.parse_args()

    if not_positive_integer(args.prompt_count_multiplier):
        args.prompt_count_multiplier = 1

    if not_positive_integer(args.max_prompt_count):
        args.max_prompt_count = 1000

    if args.shuffled is not None and args.shuffled < 1:
        parser.error("The shuffle count must be a positive integer.")

    print(f"Move Generated Prompt Templates (to {generated_template_path}): {args.move_generated}")
    print(f"Prompt Count Multiplier: {args.prompt_count_multiplier}")
    print(f"Maximum Prompt Count (per file): {args.max_prompt_count}")
    print(f"Shuffle (count): {args.shuffled}")

    template_list = create_template_list(args.move_generated)
    keywords = spg.load_data()

    for template in template_list:
        main_keyword_list, random_keyword_list, text_prompts_length, prompt_list_chunks_length, created_file_list = spg.data_parse_template(keywords, template, args.prompt_count_multiplier, args.max_prompt_count, args.shuffled)
        print("Main keywords", main_keyword_list)
        print("Random keywords:", random_keyword_list)
        print("Prompt Count:", text_prompts_length)
        print("Max. Prompt Count:", args.max_prompt_count)
        print("File Count:", prompt_list_chunks_length)
        for created_file in created_file_list:
            print("Prompt file", created_file, "created.")


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