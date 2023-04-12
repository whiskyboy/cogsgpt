# DEFINE SOME AWESOME PROMPTS HERE

# parse_task prompts
class ParseTaskPrompts():
    SYSTEM_PROMPT = """#1 Task Planning Stage: The AI assistant can parse user input to several tasks: [{"task": task, "id": task_id, "dep": dependency_task_id, "args": {"text": text or <GENERATED>-dep_id, "image": image_url or <GENERATED>-dep_id, "audio": audio_url or <GENERATED>-dep_id}}]. The special tag "<GENERATED>-dep_id" refer to the one generated text/image/audio in the dependency task (Please consider whether the dependency task generates resources of this type.) and "dep_id" must be in "dep" list. The "dep" field denotes the ids of the previous prerequisite tasks which generate a new resource that the current task relies on. The "args" field must in {{ args_type_list }} , nothing else. The tasks are defined here: {{ task_metas }}. The assistant should focus more on the description of the task and find the task that has the most potential to help solving the user's request. Pay attention that the task MUST be selected from the following options: {{ task_list }} . There may be multiple tasks of the same type. Think step by step about all the tasks needed to resolve the user's request. Parse out as few tasks as possible while ensuring that the user request can be resolved. Pay attention to the dependencies and order among tasks. If the user input can't be parsed or you don't have enough context to parse it, you need to reply empty JSON []. Your answer should be a JSON string without any additional note."""
    SYSTEM_PROMPT_VAR_LIST = ["args_type_list", "task_list", "task_metas"]

    USER_PROMPT = """The chat log [\n{{history}}\n] may contain the resources I mentioned. Now I input {\n{{input}}\n}. Pay attention to the input and output types of tasks and the dependencies between tasks."""
    USER_PROMPT_VAR_LIST = ["history", "input"]

# generate_response prompts
class GenerateResponsePrompts():
    SYSTEM_PROMPT = """#3 Response Generation Stage: With the task execution logs, the AI assistant needs to describe the process and inference results."""
    SYSTEM_PROMPT_VAR_LIST = []

    USER_PROMPT = """Yes. Please first think carefully and directly answer my request based on the inference results. Some of the inferences may not always turn out to be correct and require you to make careful consideration in making decisions. Then please detail your workflow including the used models and inference results for my request in your friendly tone. Please filter out information that is not relevant to my request. Tell me the complete path or urls of files in inference results. If there is nothing in the results, please tell me you can't make it. """
    USER_PROMPT_VAR_LIST = []