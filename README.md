# CogsGPT
A multi-modal LLM integrated ChatGPT with Azure Cognitive Service, inspired by HuggingGPT.

## Overview
This project is inspired by [HuggingGPT](https://github.com/microsoft/JARVIS). As the name CogsGPT suggests, it utilizes the ChatGPT model as the language center and integrates with Azure Cognitive Services to achieve multimodal capabilities to some extent.

Typical user cases include:

- Information extraction: Extract the main information from a doc or an image.
- Image translation: Translate the text in an image to another language.
- Speech summarization: Summarize a long speech into a short audio clip while retaining the main information.
- Speech translation: Translate input speech into another language.

There are more user cases waiting for your exploration!

Here is a demo of creating a poem based on an image and converting it into speech in another language.

![demo](./docs/demo.gif)

## Getting Started

### Prerequisites

#### OpenAI Requirements

First, you need to register an [OpenAI](https://platform.openai.com/) account or deploy an [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service). Follow the official documents to obtain the API key and other resources. 

If you want to use OpenAI API, you need to set these environment variables:
```bash
export OPENAI_API_TYPE="openai"
export OPENAI_API_KEY="<OpenAI API Key>"
export OPENAI_MODEL_NAME="<OpenAI Model Name>"
```

If you want to use Azure OpenAI Service, you need to set these environment variables:
```bash
export OPENAI_API_TYPE="azure"
export OPENAI_API_BASE="<Azure OpenAI Service Endpoint>"
export OPENAI_API_KEY="<Azure OpenAI Service Key>"
export OPENAI_MODEL_NAME="<Deployment Name>"
export OPENAI_MODEL_VERSION="<Model Version>"
```

#### Azure Cognitive Service Requirements

Next, you need also to deploy an [Azure Cognitive Service](https://azure.microsoft.com/en-us/products/cognitive-services/). Follow the official documents to obtain the deployment key and other resources, and set these environment variables:
```bash
export COGS_ENDPOINT="<Azure Cognitive Service Endpoint>"
export COGS_KEY="<Azure Cognitive Service Key>"
export COGS_REGION="<Azure Cognitive Service Region>"
```

#### Platform Requirements

At last, follow the [instruction](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/setup-platform?tabs=windows%2Cubuntu%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi&pivots=programming-language-python#platform-requirements) here to check your platfrom requirments (which is necessary to use Azure Speech SDK for Python)

### Quick Install

You can now install CogsGPT with pip:
```bash
pip install cogsgpt
```

### Usage

You can use CogsGPT in your own application to process image or audio inputs within 3 lines of codes:
```python
from cogsgpt import CogsGPT

agent = CogsGPT()
agent.chat("What's the content in a.jpg?")
```

Or you can experience an interactive console application with the following command:
```bash
python ./tests/test_awesome_chat.py
```

Enjoy your chat!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contributing

As an open source project, we welcome contributions and suggestions. Please follow the [fork and pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow to contribute to this project. Please do not try to push directly to this repo unless you are maintainer.

## Contact

If you have any questions, please feel free to contact us via <weitian.bnu@gmail.com>