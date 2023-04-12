import sys
sys.path.insert(0, "./")

from cogsgpt.awesome_chat import CogsGPT


if __name__ == "__main__":
    cogs_gpt = CogsGPT()
    while True:
        human_input = input('User: ')
        print('Assistant: {}'.format(cogs_gpt.chat(human_input)))