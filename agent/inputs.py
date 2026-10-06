from agent.core.prompts import SYSTEM_PROMPT, ERROR_PROMPT
def input_message(user_input:str)->list[dict]:
    return [
        {"role":"system","content":SYSTEM_PROMPT+ERROR_PROMPT},
        {"role":"user","content":user_input}
    ]
