# DEFINE SOME AWESOME PROMPTS HERE

# parse_task prompts
class ParseTaskPrompts():
    SYSTEM_PROMPT = """#1 Task Planning Stage: Given a list of tasks: {{ task_metas }}, you should parse user input to tasks in JSON format containing task ID, dependency task ID, and arguments such as text, image, audio, from_language, and to_language. The special tag "<GENERATED>-dep_id" refers to a resource generated in the dependency task, while "dep_id" must be in the dependency list. The "args" field must in {{ args_type_list }} , nothing else. The from_language/to_language values must be in {{ supported_language_list }}. If you are not sure about the language value, use the language of user's input."""
    SYSTEM_PROMPT_VAR_LIST = ["task_metas", "args_type_list", "supported_language_list"]

    USER_PROMPT = """The chat log [\n{{history}}\n] may contain the resources I mentioned. Now I input {\n{{input}}\n}. You should select tasks that you are VERY certain are the most useful to answer my request with minimal parsing. Pay more attention to the description of each task when selecting tasks. Your response MUST be a valid JSON string without any additional note. If parsing fails, return an empty JSON []."""
    USER_PROMPT_VAR_LIST = ["history", "input"]

# generate_response prompts
class GenerateResponsePrompts():
    SYSTEM_PROMPT = """#3 Response Generation Stage: With the task execution logs, you need to give a directly response to user's input."""
    SYSTEM_PROMPT_VAR_LIST = []

    USER_PROMPT = """Yes. Please first think carefully and directly answer my request based on the tasks results. Some of the results may not always be correct and require you to make careful consideration in making decisions. Please filter out results that is not relevant to my request. If I request an image or an audio file, your response should also contain the path to the generated image or audio file. If there is nothing in the results, please tell me you can't make it."""
    USER_PROMPT_VAR_LIST = []