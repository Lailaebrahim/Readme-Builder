from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from utils import add_root_to_path
root_path = add_root_to_path()
print(root_path)

from helpers import replace_input_sentence, replace_input_description
from common.utils import load_config, parse_safety_settings

config = load_config(f"{root_path}/config/llm.json")
safety_settings = parse_safety_settings(config['safety_settings'])

llm = ChatGoogleGenerativeAI(
    google_api_key=config['api_key'],
    model=config['model'],
    temperature=0.7,
    safety_settings=safety_settings
)

chain = llm | StrOutputParser()

prompt = """
you will be in a loop where you will get feedback every iteration.
your task is to help to build a readme file by selecting the most important files the user should read to understand
the project and make readme out of it
you will be given a tree of dirs and files from a user of his project and your task
is too see the files and dirs from the user and choose which files are important 
and select them where this files will be given to another AI model so he can write readme file
for this files and dirs so your task is to classify the important files for the user based on his description and his feedback.
if there is no feedback don't generate one just make the output with out feedback till the user give you the feedback.
note that you take prompt from user where he tells you what does he need you to focus on.

your max output should be atmost 5 files  (the most important one)

### README Requirements description
{description}

### Input
{input}

### Instructions : 
1. Attempt the task based on the input provided.
2. Output your response.
3. Wait for human feedback.
4. If feedback is given, revise your response based on the feedback and attempt the task again.
5. foucus on using the feedback of the user each iteration.
"""



def generate_prompt(prompt, task_description, user_input, feedback=None):

    if feedback:
        prompt += f"### Feedback\n{feedback}\n"

    prompt = replace_input_description(prompt,task_description)
    prompt += "### Current Input\n" + user_input
    return prompt


def llm_generate(base_prompt, task_description, input_data, feedback=None):
    prompt = generate_prompt(base_prompt, task_description, input_data, feedback)
    llm_response = chain.invoke(prompt)
    return llm_response


def human_in_the_loop(prompt, initial_input, task_description):
    input_data = initial_input
    feedback = None
    loop_active = True
    iteration = 0
    
    while loop_active:
        llm_response = llm_generate(prompt, task_description, input_data, feedback)
        
        print("LLM Response:", llm_response)
        
        human_feedback = input("Enter feedback (or 'exit' to end loop): ")
        
        if human_feedback.lower() == 'exit':
            loop_active = False
        else:
            feedback = human_feedback
        
        iteration += 1
        print(f"Iteration {iteration} completed.")
    
    print("Loop terminated.")


initial_input = """

The tree of repository:
0x00-shell_basics
0x00-shell_basics/0-current_working_directory
0x00-shell_basics/1-listit
0x00-shell_basics/10-back
0x00-shell_basics/100-lets_move
0x00-shell_basics/101-clean_emacs
0x00-shell_basics/102-tree
0x00-shell_basics/103-commas
0x00-shell_basics/11-lists
0x00-shell_basics/12-file_type
0x00-shell_basics/13-symbolic_link
0x00-shell_basics/14-copy_html
0x00-shell_basics/2-bring_me_home
0x00-shell_basics/3-listfiles
0x00-shell_basics/4-listmorefiles
0x00-shell_basics/5-listfilesdigitonly
0x00-shell_basics/6-firstdirectory
0x00-shell_basics/7-movethatfile
0x00-shell_basics/8-firstdelete
0x00-shell_basics/9-firstdirdeletion
0x00-shell_basics/README.md
0x01-shell_permissions
0x01-shell_permissions/0-iam_betty
0x01-shell_permissions/1-who_am_i
0x01-shell_permissions/10-mirror_permissions
0x01-shell_permissions/100-change_owner_and_group
0x01-shell_permissions/101-symbolic_link_permissions
0x01-shell_permissions/101-symbolic_link_permissions~
0x01-shell_permissions/102-if_only
0x01-shell_permissions/103-Star_Wars
0x01-shell_permissions/11-directories_permissions
0x01-shell_permissions/12-directory_permissions
0x01-shell_permissions/13-change_group
0x01-shell_permissions/2-groups
0x01-shell_permissions/3-new_owner
0x01-shell_permissions/3-new_owner~
0x01-shell_permissions/4-empty
0x01-shell_permissions/5-execute
0x01-shell_permissions/6-multiple_permissions
0x01-shell_permissions/7-everybody
0x01-shell_permissions/8-James_Bond
0x01-shell_permissions/9-John_Doe
0x01-shell_permissions/README.md
0x02-shell_redirections
0x02-shell_redirections/0-hello_world
0x02-shell_redirections/1-confused_smiley
0x02-shell_redirections/10-no_more_js
0x02-shell_redirections/100-empty_casks
0x02-shell_redirections/100-empty_casks~
0x02-shell_redirections/101-gifs
0x02-shell_redirections/11-directories
0x02-shell_redirections/12-newest_files
0x02-shell_redirections/13-unique
0x02-shell_redirections/14-findthatword
0x02-shell_redirections/15-countthatword
0x02-shell_redirections/16-whatsnext
0x02-shell_redirections/17-hidethisword
0x02-shell_redirections/18-letteronly
0x02-shell_redirections/19-AZ
0x02-shell_redirections/2-hellofile
0x02-shell_redirections/20-hiago
0x02-shell_redirections/21-reverse
0x02-shell_redirections/22-users_and_homes
0x02-shell_redirections/3-twofiles
0x02-shell_redirections/4-lastlines
0x02-shell_redirections/5-firstlines
0x02-shell_redirections/6-third_line
0x02-shell_redirections/7-file
0x02-shell_redirections/8-cwd_state
0x02-shell_redirections/9-duplicate_last_line
0x02-shell_redirections/README.md
0x02-shell_redirections/file.txt
0x03-shell_variables_expansions
0x03-shell_variables_expansions/.#102-odd
0x03-shell_variables_expansions/0-alias
0x03-shell_variables_expansions/1-hello_you
0x03-shell_variables_expansions/10-love_exponent_breath
0x03-shell_variables_expansions/100-decimal_to_hexadecimal
0x03-shell_variables_expansions/101-rot13
0x03-shell_variables_expansions/102-odd
0x03-shell_variables_expansions/103-water_and_stir
0x03-shell_variables_expansions/11-binary_to_decimal
0x03-shell_variables_expansions/12-combinations
0x03-shell_variables_expansions/13-print_float
0x03-shell_variables_expansions/2-path
0x03-shell_variables_expansions/3-paths
0x03-shell_variables_expansions/4-global_variables
0x03-shell_variables_expansions/5-local_variables
0x03-shell_variables_expansions/6-create_local_variable
0x03-shell_variables_expansions/7-create_global_variable
0x03-shell_variables_expansions/8-true_knowledge
0x03-shell_variables_expansions/9-divide_and_rule
0x03-shell_variables_expansions/README.md
0x04-loops_conditions_and_parsing
0x04-loops_conditions_and_parsing/0-RSA_public_key.pub
0x04-loops_conditions_and_parsing/README.md
0x06-regular_expressions
0x06-regular_expressions/0-simply_match_school.rb
0x06-regular_expressions/1-repetition_token_0.rb
0x06-regular_expressions/100-textme.rb
0x06-regular_expressions/2-repetition_token_1.rb
0x06-regular_expressions/3-repetition_token_2.rb
0x06-regular_expressions/4-repetition_token_3.rb
0x06-regular_expressions/5-beginning_and_end.rb
0x06-regular_expressions/6-phone_number.rb
0x06-regular_expressions/7-OMG_WHY_ARE_YOU_SHOUTING.rb
0x06-regular_expressions/README.md
0x07-networking_basics
0x07-networking_basics/0-OSI_model
0x07-networking_basics/1-types_of_network
0x07-networking_basics/2-MAC_and_IP_address
0x07-networking_basics/3-UDP_and_TCP
0x07-networking_basics/4-TCP_and_UDP_ports
0x07-networking_basics/5-is_the_host_on_the_network
0x07-networking_basics/README.md
0x08-networking_basics_2
0x08-networking_basics_2/0-change_your_home_IP
0x08-networking_basics_2/1-show_attached_IPs
0x08-networking_basics_2/100-port_listening_on_localhost
0x08-networking_basics_2/README.md
0x0A-configuration_management
0x0A-configuration_management/0-create_a_file.pp
0x0A-configuration_management/1-install_a_package.pp
0x0A-configuration_management/2-execute_a_command.pp
0x0A-configuration_management/README.md
0x0B-ssh
0x0B-ssh/0-use_a_private_key
0x0B-ssh/1-create_ssh_key_pair
0x0B-ssh/100-puppet_ssh_config.pp
0x0B-ssh/2-ssh_config
0x0B-ssh/README.md
0x0C-web_server
0x0C-web_server/0-transfer_file
0x0C-web_server/1-install_nginx_web_server
0x0C-web_server/2-setup_a_domain_name
0x0C-web_server/3-redirection
0x0C-web_server/4-not_found_page_404
0x0C-web_server/7-puppet_install_nginx_web_server.pp
0x0C-web_server/README.md
0x0C-web_server/some_page.html
0x0D-web_stack_debugging_0
0x0D-web_stack_debugging_0/0-give_me_a_page
0x0D-web_stack_debugging_0/README.md
0x0E-web_stack_debugging_1
0x0E-web_stack_debugging_1/0-nginx_likes_port_80
0x0E-web_stack_debugging_1/1-debugging_made_short
0x0E-web_stack_debugging_1/README.md
0x0F-load_balancer
0x0F-load_balancer/0-custom_http_response_header
0x0F-load_balancer/1
0x0F-load_balancer/1-install_load_balancer
0x0F-load_balancer/2-puppet_custom_http_response_header.pp
0x0F-load_balancer/README.md
0x10-https_ssl
0x10-https_ssl/0-world_wide_web
0x10-https_ssl/1-haproxy_ssl_termination
0x10-https_ssl/100-redirect_http_to_https
0x10-https_ssl/README.md
0x11-what_happens_when_your_type_google_com_in_your_browser_and_press_enter
0x11-what_happens_when_your_type_google_com_in_your_browser_and_press_enter/0-blog_post
0x11-what_happens_when_your_type_google_com_in_your_browser_and_press_enter/1-what_happen_when_diagram
0x11-what_happens_when_your_type_google_com_in_your_browser_and_press_enter/2-contribution-to_what-happens-when_github_answer
0x12-web_stack_debugging_2
0x12-web_stack_debugging_2/0-iamsomeoneelse
0x12-web_stack_debugging_2/1-run_nginx_as_nginx
0x12-web_stack_debugging_2/100-fix_in_7_lines_or_less
0x12-web_stack_debugging_2/README.md
0x13-firewall
0x13-firewall/0-block_all_incoming_traffic_but
0x13-firewall/100-port_forwarding
0x13-firewall/README.md
0x14-mysql
0x14-mysql/4-mysql_configuration_primary
0x14-mysql/4-mysql_configuration_replica
0x14-mysql/5-mysql_backup
0x14-mysql/README.md
0x16-api_advanced
0x16-api_advanced/0-main.py
0x16-api_advanced/0-subs.py
0x16-api_advanced/1-main.py
0x16-api_advanced/1-top_ten.py
0x16-api_advanced/2-main.py
0x16-api_advanced/2-recurse.py
0x16-api_advanced/README.md
0x16-api_advanced/python
0x17-web_stack_debugging_3
0x17-web_stack_debugging_3/0-strace_is_your_friend.pp
0x17-web_stack_debugging_3/README.md
0x18-webstack_monitoring
0x18-webstack_monitoring/2-setup_datadog
0x18-webstack_monitoring/README.md
0x19-postmortem
0x19-postmortem/README.md
0x1B-web_stack_debugging_4
0x1B-web_stack_debugging_4/0-the_sky_is_the_limit_not.pp
"""

task_description = "I want to make the readme file about web servers"
human_in_the_loop(prompt, initial_input, task_description)