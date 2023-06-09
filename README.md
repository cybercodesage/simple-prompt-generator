# Simple Prompt Generator

## Project Description

This Python-based project is designed to generate simple prompts for AI image generation projects such as DALL-E and Stable Diffusion. It uses template files to produce prompts, replacing special "Main Keywords" and "Random Keywords" within the templates with corresponding values from a data file.

Main Keywords are enclosed with the character `#`, for example `#simple-action#`, and Random Keywords are enclosed with character `%`, for example `%artist%`.

The project generates a list of combinations for Main Keywords and produces a prompt for each combination. Random Keywords are replaced randomly within the generated prompts, ensuring the overall prompt count doesn't change. Additionally, the argument `--prompt-count-multiplier` can be used to multiply the number of prompts generated.

## Requirements

Python 3.x is required to run this project. If you don't use GUI, no additional packages are needed. In order to use GUI function setup.bat (setup.sh) should be executed one time.

## Usage

If GUI will be used, `python gui.py` command should be executed at command-line. GUI functions are self-explanatory. However, you may want to read command-line instructions below for efficent usage of GUI. GUI does not support "shuffle" function at the moment.

For command-line;

1. Prepare your template files: Template files must be text (`.txt`) files and contain a single-line template string. You can use multiple template files. The templates should be stored in the `./templates` directory.

2. Prepare your data: The data for replacing keywords in templates should be stored in a JSON file named `data.json` located in the `./data` directory.

3. Run the script: Use the command `python main.py` to run the script. You can add the following optional arguments:
    - `--move-generated`: If this argument is passed, the template files will be moved to the `./generated_templates` directory after prompt generation.
    - `--prompt-count-multiplier`: This argument specifies the multiplier for the number of prompts generated. It accepts a positive integer value and defaults to `1` if not specified.
    - `--max-prompt-count`: Maximum prompt count per output prompt file. The output files are splited if total number of prompts exceeds this number. It accepts a positive integer value and defaults to `1000` if not specified.
    - `--shuffled`: Its defualt value is None. If set in command line without any paramaters (positive integers) as `--shuffled` its default value is set to 1 otherwise the parameter is used as its value (`--shuffled n` means its value n). It generates n more prompts following the original prompt which are shuffled by using parts of the original prompt splitted by commas (,). The shuffled prompts are not calculated as new prompts therefore the prompt count may exceed `max-prompt-count` in a prompt file. That is, if 700 prompts is generated and `--shuffled 3` is used with `--max-prompt-count 500`, each prompt file contains 1500 prompts not 500.

## Examples

Assuming you have a template file with the following content:

"a painting of a valley by %artist%, trending on #art-site#, #time-of-day#"

And your `data.json` contains the following values:

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

You should modify the sample template files and the data file or create new ones to better suit your purpose. `./samples` directory contains sample files.
