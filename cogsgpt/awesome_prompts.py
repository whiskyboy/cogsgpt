# DEFINE SOME AWESOME PROMPTS HERE

# parse_task prompts
class ParseTaskPrompts():
    SYSTEM_PROMPT = """#1 Task Planning Stage: Given a list of tasks: {{ task_metas }}, you should parse user input to tasks in JSON format containing task ID, dependency task ID, and arguments such as text, image, audio, from_language, and to_language. The special tag "<GENERATED>-dep_id" refers to a resource generated in the dependency task, while "dep_id" must be in the dependency list. The "args" field must in {{ args_type_list }} , nothing else. The from_language/to_language values must be in {{ supported_language_list }}. If you are not sure about the language value, use the language of user's input as default."""
    SYSTEM_PROMPT_VAR_LIST = ["task_metas", "args_type_list", "supported_language_list"]

    USER_PROMPT = """The chat log [\n{{history}}\n] may contain the resources I mentioned. Now I input {\n{{input}}\n}. You should select tasks that could answer my input with minimal parsing. Avoid selecting unnecessary tasks. If parsing fails, return an empty JSON []."""
    USER_PROMPT_VAR_LIST = ["history", "input"]

# generate_response prompts
class GenerateResponsePrompts():
    SYSTEM_PROMPT = """#3 Response Generation Stage: With the task execution logs, the AI assistant needs to give a directly response to user's input."""
    SYSTEM_PROMPT_VAR_LIST = []

    USER_PROMPT = """Yes. Please first think carefully and directly answer my request based on the inference results. Some of the inferences may not always turn out to be correct and require you to make careful consideration in making decisions. Please filter out information that is not relevant to my request. If I request an image file or an audio file, your response should contain the file path. If there is nothing in the results, please tell me you can't make it. """
    USER_PROMPT_VAR_LIST = []