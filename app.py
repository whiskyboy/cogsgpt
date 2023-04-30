import os
import re
import shutil
import tempfile
import gradio as gr
import requests
from cogsgpt import CogsGPT


class Client:
    def __init__(self):
        self._client = CogsGPT(temperature=0.2, verbose=True)

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

    def _download_media(self, url):
        ext = url.split('.')[-1]
        response = requests.get(url, stream=True)
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.' + ext, delete=False) as media_file:
            shutil.copyfileobj(response.raw, media_file)
        return media_file.name

    def add_text(self, chatbot, text_input):
        self._text_input = text_input
        if self._text_input == "":
            return chatbot
        
        chatbot += [(self._text_input, None)]

        image_urls, audio_urls = self._extract_medias(self._text_input)
        for image_url in image_urls:
            if image_url.startswith('http'):
                image_url = self._download_media(image_url)
            chatbot += [((image_url,), None)]
        for audio_url in audio_urls:
            if audio_url.startswith('http'):
                audio_url = self._download_media(audio_url)
            chatbot += [((audio_url,), None)]

        return chatbot

    def parse_task(self):
        if self._text_input == "":
            return
        
        self._task_list = self._client.parse_tasks(self._text_input)
        return self._task_list

    def execute_task(self):
        if self._text_input == "":
            return
        
        self._task_result_list = self._client.execute_tasks(self._task_list)
        return self._task_result_list

    def generate_response(self, chatbot):
        if self._text_input == "":
            return chatbot
        
        self._response = self._client.generate_response(self._text_input, self._task_result_list)
        chatbot += [(None, self._response)]

        image_urls, audio_urls = self._extract_medias(self._response)
        for image_url in image_urls:
            if image_url.startswith('http'):
                image_url = self._download_media(image_url)
            chatbot += [(None, (image_url,))]
        for audio_url in audio_urls:
            if audio_url.startswith('http'):
                audio_url = self._download_media(audio_url)
            chatbot += [(None, (audio_url,))]

        # self._client.save_context(self._input, self._response)

        return chatbot

def set_key(state, openai_api_key):
    os.environ["OPENAI_API_TYPE"] = "openai"
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    state["client"] = Client()
    return state, openai_api_key

def add_text(state, chatbot, text_input):
    if "client" not in state:
        return chatbot, "Please set your OpenAI API key first!!!"

    chatbot = state["client"].add_text(chatbot, text_input)
    return chatbot, ""

def parse_task(state, chatbot):
    if "client" not in state:
        return chatbot, None
    
    task_list = state["client"].parse_task()
    return chatbot, task_list

def execute_task(state, chatbot):
    if "client" not in state:
        return chatbot, None
    
    task_result_list = state["client"].execute_task()
    return chatbot, task_result_list

def generate_response(state, chatbot):
    if "client" not in state:
        return chatbot
    
    chatbot = state["client"].generate_response(chatbot)
    return chatbot


css = ".json {height: 527px; overflow: scroll;} .json-holder {height: 527px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={})

    gr.Markdown("<h1><center>CogsGPT</center></h1>")
    gr.Markdown("<p align='center' style='font-size: 20px;'>A conversational system which integrates ChatGPT with Azure Cognitive Services to achieve multimodal capabilities.</p>")
    gr.Markdown("<p align='center' style='font-size: 18px;'>If you find it useful, please consider giving it a star on <a href='https://github.com/whiskyboy/cogsgpt'>Github</a>! :)</p>")
    gr.Markdown("""
    <div style="text-align: center;">
        <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/whiskyboy/cogsgpt?style=social" style="display: inline-block;">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/whiskyboy/cogsgpt?style=social" style="display: inline-block;">
        <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/whiskyboy/cogsgpt?style=social" style="display: inline-block;">
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=0.85):
            openai_api_key = gr.Textbox(
                show_label=False,
                placeholder="Set your OpenAI API key here and press Enter",
                lines=1,
                type="password"
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            set_key_btn = gr.Button("Submit")

    # Ouput Row
    with gr.Row():
        with gr.Column(scale=0.6):
            chatbot = gr.Chatbot([], label="Chatbot").style(height=500)
        
        with gr.Column(scale=0.4):
            task_output = gr.JSON(label="Tasks", elem_classes="json")

    # Input Row
    with gr.Row():
        with gr.Column(scale=0.85):
            text_input = gr.Textbox(lines=1, show_label=False, interactive=True,
                                    placeholder="Enter text and press enter. The url must contain the media type. e.g, https://example.com/example.jpg",
                                    ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            send_btn = gr.Button("Send", label="Send", interactive=True)

    # Even binding
    openai_api_key.submit(
        fn=set_key,
        inputs=[state, openai_api_key],
        outputs=[state, openai_api_key])
    set_key_btn.click(
        fn=set_key,
        inputs=[state, openai_api_key],
        outputs=[state, openai_api_key])

    text_input.submit(
        fn=add_text,
        inputs=[state, chatbot, text_input],
        outputs=[chatbot, text_input]).then(
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
        inputs=[state, chatbot, text_input],
        outputs=[chatbot, text_input]).then(
        fn=parse_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=execute_task,
        inputs=[state, chatbot],
        outputs=[chatbot, task_output]).then(
        fn=generate_response,
        inputs=[state, chatbot],
        outputs=[chatbot])
    
    # Examples
    gr.Examples(
        examples=[
            # CV
            "What can I make with these ingredients? ./tests/examples/ingredients.png",
            "Extract the text from the image: ./tests/examples/handwritten-note.jpg",
            "Select images of dog from the list: [./tests/examples/animal-1.jpg, ./tests/examples/animal-2.jpg, ./tests/examples/animal-3.jpg]",
            "Remove the background of the image: ./tests/examples/wedding.png",
            # Speech
            "Convert the text 'CogsGPT is a multi-modal LLM integrated ChatGPT with Azure Cognitive Service' into speech.",
            "Extract the content of audio: ./tests/examples/cogsgpt.wav",
            # Form
            "List all the items and their prices from the receipt: ./tests/examples/receipt.png",
            "Extract the flight schedule table from the file: ./tests/examples/flight-schedule.png, and list all the flights with China Eastern airline.",
            # Complex task
            "Summarize the content in the audio file: ./tests/examples/voa-1min-news.wav, and translate it into Chinese. Then read it out.",
        ],
        inputs=text_input,
    )

demo.launch(show_api=False)