def replace_history_sentence(template, memory_buffer):
    return template.replace("{history}",memory_buffer)

def replace_instructions_sentence(template, instructions):
    return template.replace("{format_instructions}",instructions)

def replace_input_sentence(template, user_input):
    return template.replace("{input}",user_input)

def replace_input_description(template, description):
    return template.replace("{description}",description)