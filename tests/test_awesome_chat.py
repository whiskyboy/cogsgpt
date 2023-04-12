import sys
sys.path.insert(0, "./")

from cogsgpt.awesome_chat import CogsGPT


if __name__ == "__main__":
    cogs_gpt = CogsGPT()
    human_input = "Write a poem for this image: ./samples/presentation.png ?"
    print(cogs_gpt.chat(human_input))