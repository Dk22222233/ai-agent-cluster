from core.prompts import SYSTEM_PROMPT
def initial_messagge(user_input:str)->list[dict]:
    return [
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":user_input}
    ]
