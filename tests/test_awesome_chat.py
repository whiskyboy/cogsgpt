import sys
sys.path.insert(0, "./")

from cogsgpt.awesome_chat import CogsGPT


if __name__ == "__main__":
    cogs_gpt = CogsGPT(temperature=0.2, verbose=True)

    test_cases = [
        # CV
        "Describe the content of the image: ./tests/examples/presentation.png",
        "Extract the text from the image: ./tests/examples/handwritten-note.jpg",
        "How many people are there in the image: ./tests/examples/family.png?", 
        "Select images of dog from the list: [./tests/examples/animal-1.jpg, ./tests/examples/animal-2.jpg, ./tests/examples/animal-3.jpg]",
        "Remove the background of the image: ./tests/examples/wedding.png",
        "Crop a thumbnail for the image: ./tests/examples/wedding.png",
        
        # Speech
        "Convert the text 'CogsGPT is a multi-modal LLM integrated ChatGPT with Azure Cognitive Service' into speech.",
        "Extract the content of audio: ./tests/examples/cogsgpt.wav",
        
        # Form
        "List all the items and their prices from the receipt: ./tests/examples/receipt.png",
        "Extract the service address field from the invoice: ./tests/examples/sample-invoice.pdf",
        "Extract the flight schedule table from the file: ./tests/examples/flight-schedule.png, and list all the flights with China Eastern airline.",
        
        # Complex task
        "Summarize the content in the audio file: ./tests/examples/voa-1min-news.wav, and translate it into Chinese. Then read it out.",
    ]

    for test_case in test_cases:
        print('User: {}'.format(test_case))
        print('Assistant: {}'.format(cogs_gpt.chat(test_case)))
        print()

    while True:
        human_input = input('User: ')
        print('Assistant: {}'.format(cogs_gpt.chat(human_input)))