from agent_llm import SimpleStreamLLM
from agent_prompt import PlaceHoldersPrompt
from agent_runtime import HumanLoopRuntime
from prompt import read_dir_prompt, initial_input

from utils import add_root_to_path
root_path = add_root_to_path()
from common import load_config, parse_safety_settings

config = load_config(f'{root_path}/config/llm.json')
safety_settings = parse_safety_settings(settings=config['safety_settings'])

task_description = "I want to make the readme file about web servers"

llm = SimpleStreamLLM(api_key=config['api_key'],model=config['model'],temperature=0.7,safety_settings=safety_settings)
prompt = PlaceHoldersPrompt(prompt_string=read_dir_prompt,
                            placeholders={
                                '{description}':'',
                                '{input}':initial_input
                            })
agent = HumanLoopRuntime(llm=llm,prompt=prompt)

agent.loop()