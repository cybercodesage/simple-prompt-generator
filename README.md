# Simple Prompt Generator

## Project Description

This Python-based project is designed to generate simple prompts for AI image generation projects such as DALL-E and Stable Diffusion. It uses template files to produce prompts, replacing special "Main Keywords" and "Random Keywords" within the templates with corresponding values from a data file.

Main Keywords are enclosed with the character `#`, for example `#simple-action#`, and Random Keywords are enclosed with character `%`, for example `%artist%`.

The project generates a list of combinations for Main Keywords and produces a prompt for each combination. Random Keywords are replaced randomly within the generated prompts, ensuring the overall prompt count doesn't change. Additionally, the argument `--prompt-count-multiplier` can be used to multiply the number of prompts generated.

## Requirements

Python 3.x is required to run this project. No additional packages are needed.

## Usage

1. Prepare your template files: Template files must be text (`.txt`) files and contain a single-line template string. You can use multiple template files. The templates should be stored in the `./templates` directory.

2. Prepare your data: The data for replacing keywords in templates should be stored in a JSON file named `_data.json` located in the `./data` directory.

3. Run the script: Use the command `python main.py` to run the script. You can add the following optional arguments:
    - `--move-generated`: If this argument is passed, the template files will be moved to the `./generated_templates` directory after prompt generation.
    - `--prompt-count-multiplier`: This argument specifies the multiplier for the number of prompts generated. It accepts an integer value and defaults to `1` if not specified.

## Examples

Assuming you have a template file with the following content:

"a painting of a valley by %artist%, trending on #art-site#, #time-of-day#"

And your `_data.json` contains the following values:

{
"artist": ["Brent Heighton", "Brian Donnelly", "Bridget Riley", "Diego Fazio", "Diego Rivera"],
"art-site": ["ArtStation", "Artsy"],
"time-of-day": ["morning", "noon", "night"]
}

Running `python main.py --prompt-count-multiplier 3` will generate 2x3x3 prompts, such as:

1. "a painting of a valley by Brian Donnelly, trending on ArtStation, morning"
2. "a painting of a valley by Diego Fazio, trending on ArtStation, noon"
3. "a painting of a valley by Brent Heighton, trending on ArtStation, night"
4. "a painting of a valley by Diego Fazio, trending on Artsy, morning"
5. ... and more.

The generated prompts will be stored in a file located in the `./prompt_files/` directory. The filename will include the Main Keywords, Random Keywords, and a timestamp.
You can modify this template to better suit your project.
