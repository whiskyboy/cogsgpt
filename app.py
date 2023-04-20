import os
import re
import shutil
import gradio as gr
from cogsgpt import CogsGPT


class Client:
    def __init__(self):
        self._client = CogsGPT()

    def _move_file(self, src):
        """
        move file from src to public/images or public/audios
        """
        file_name = os.path.basename(src)
        file_type = file_name.split(".")[-1]

        if file_type in ["jpg", "jpeg", "png", "gif", "bmp"]:
            dst = os.path.join("public/images", file_name)
        elif file_type in ["mp3", "wav", "ogg", "flac"]:
            dst = os.path.join("public/audios", file_name)
        else:
            raise ValueError("Unsupported file type")
        
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)

        return dst

    def _extract_medias(self, message):
        image_pattern = re.compile(r"(http(s?):|\/)?([\.\/_\w:-])*?\.(jpg|jpeg|tiff|gif|png)")
        image_urls = []
        for match in image_pattern.finditer(message):
            if match.group(0) not in image_urls:
                image_urls.append(match.group(0))

        audio_pattern = re.compile(r"(http(s?):|\/)?([\.\/_\w:-])*?\.(flac|wav)")
        audio_urls = []
        for match in audio_pattern.finditer(message):
            if match.group(0) not in audio_urls:
                audio_urls.append(match.group(0))

        return image_urls, audio_urls

    def add_text(self, chatbot, text_input, image_input=None, audio_input=None):
        if text_input:
            self._message = text_input
            chatbot += [[text_input, None]]
        if image_input:
            # image_path = self._move_file(image_input)
            self._message += f"\nimage path:({image_input})"
            chatbot += [[(image_input,), None]]
        if audio_input:
            # audio_path = self._move_file(audio_input)
            self._message += f"\naudio_path: ({audio_input})"
            chatbot += [[(audio_input,), None]]

        return chatbot

    def parse_task(self):
        self._task_list = self._client._parse_tasks(self._message)
        return self._task_list

    def execute_task(self):
        self._task_result_list = self._client._execute_tasks(self._message, self._task_list)
        return self._task_result_list

    def generate_response(self, chatbot):
        self._response = self._client._generate_response(self._message, self._task_result_list)
        chatbot += [[None, self._response]]

        image_urls, audio_urls = self._extract_medias(self._response)
        for image_url in image_urls:
            chatbot += [[None, (image_url,)]]
        for audio_url in audio_urls:
            chatbot += [[None, (audio_url,)]]

        self._client._save_context(self._message, self._response)

        return chatbot


def add_text(state, chatbot, text_input, image_input=None, audio_input=None):
    chatbot = state["client"].add_text(chatbot, text_input, image_input, audio_input)
    # chatbot += [[None, "Parsing tasks..."]]
    return chatbot, "", None, None

def parse_task(state, chatbot):
    task_list = state["client"].parse_task()
    # chatbot += [[None, "Executing tasks..."]]
    return chatbot, task_list

def execute_task(state, chatbot):
    task_result_list = state["client"].execute_task()
    # chatbot += [[None, "Generating response..."]]
    return chatbot, task_result_list

def generate_response(state, chatbot):
    return state["client"].generate_response(chatbot)


with gr.Blocks() as demo:
    state = gr.State(value={"client": Client()})

    gr.Markdown("<h1><center>CogsGPT</center></h1>")
    gr.Markdown("<p align='center' style='font-size: 20px;'>A multi-modal LLM integrated ChatGPT with Azure Cognitive Service, inspired by <a href='https://huggingface.co/spaces/microsoft/HuggingGPT'>HuggingGPT</a>.</p>")

    # Ouput Row
    gr.Markdown("<h3>Output</h3>")
    with gr.Row():
        with gr.Column(scale=0.6):
            chatbot = gr.Chatbot([], label="CogsGPT").style(height=500)
        
        with gr.Column(scale=0.4):
            task_output = gr.JSON(label="Tasks").style(container=True)
            # image_output = gr.Image(type="filepath", label="Image", interactive=False).style(height=200)
            # audio_output = gr.Audio(type="filepath", label="Audio", interactive=False).style(height=100)

    # Input Row
    gr.Markdown("<h3>Input</h3>")
    with gr.Row():
        with gr.Column(scale=0.85):
            text_input = gr.Textbox(lines=1, show_label=False, interactive=True,
                                    placeholder="Type a message to start the conversation..."
                                    ).style(container=False)
        with gr.Column(scale=0.15):
            send_btn = gr.Button("Send", label="Send", interactive=True)

    # Optional Input Row
    with gr.Row():
        with gr.Column(scale=0.5):
            with gr.Accordion("Image (Optional)", open=True):
                image_input = gr.Image(type="filepath", show_label=False, interactive=True)
        with gr.Column(scale=0.5):
            with gr.Accordion("Audio (Optional)", open=True):
                audio_input = gr.Audio(type="filepath", show_label=False, interactive=True)

    # Even binding
    text_input.submit(
        fn=add_text,
        inputs=[state, chatbot, text_input, image_input, audio_input],
        outputs=[chatbot, text_input, image_input, audio_input]).then(
        fn=parse_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=execute_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=generate_response,
        inputs=[state, chatbot],
        outputs=[chatbot])
    send_btn.click(
        fn=add_text,
        inputs=[state, chatbot, text_input, image_input, audio_input],
        outputs=[chatbot, text_input, image_input, audio_input]).then(
        fn=parse_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=execute_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=generate_response,
        inputs=[state, chatbot],
        outputs=[chatbot])

demo.launch(show_api=False)