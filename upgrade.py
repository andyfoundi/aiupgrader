#!/usr/local/bin/python

# this script calls open AI api with a specific assistant to conver code from
# old AngularJS (javascript) to the latest Angular (TypeScript).

from datetime import datetime
from dotenv import load_dotenv
from openai import AssistantEventHandler
from openai import OpenAI
from typing_extensions import override
import argparse
import os

load_dotenv()


def print_progress(progress: str, new_section=False):
    # print with blue color
    if new_section:
        print('')
    print(f'\033[94m> {progress}\033[0m')


def print_code(code: str):
    # print with dark gray color
    print(f'\033[90m{code}\033[0m', end="", flush=True)


class EventHandler(AssistantEventHandler):

    response = []

    @override
    def on_text_created(self, text):
        pass

    @override
    def on_text_delta(self, delta, snapshot):
        print_code(delta.value)
        self.response.append(delta.value)

    def on_tool_call_created(self, tool_call):
        pass

    def on_tool_call_delta(self, delta, snapshot):
        pass


class Converter(AssistantEventHandler):

    def __init__(self, client, file_path, assistant, thread, instruction=''):
        self.file_path = file_path
        self.assistant = assistant
        self.thread = thread
        self.client = client
        self.instruction = instruction

    def run(self):
        handler = EventHandler()
        with open(self.file_path, "r") as file:
            code = file.read().strip()
            content = f"{self.instruction}\n{code}"
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id, role='user', content=content)
            print_progress(f'Message {message.id} created')

            with self.client.beta.threads.runs.create_and_stream(
                assistant_id=self.assistant.id,
                thread_id=self.thread.id,
                event_handler=handler,
            ) as stream:
                stream.until_done()

        angular_code = "".join(handler.response)
        output_path = self.file_path.replace(".js", ".ts")
        with open(output_path, "w") as file:
            file.write(angular_code)
            print_progress(f' ... saved to {output_path}')


def upgrade(code_path=None, test_path=None):
    start = datetime.now()
    print_progress(f'Conversion starting at {start}')

    organization = os.getenv("OPENAI_ORGANIZATION")
    client = OpenAI(organization=organization)
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
    assistant = client.beta.assistants.retrieve(assistant_id)
    print_progress(f'Assistant {assistant.id} retrived')
    thread = client.beta.threads.create()
    print_progress(f'Thread {thread.id} created')

    if code_path:
        print_progress(f'Converting code from {code_path}', True)
        code_converter = Converter(client, code_path, assistant, thread)
        code_converter.run()

    if test_path:
        print_progress(f'Converting test from {test_path}', True)
        test_converter = Converter(client, test_path, assistant, thread)
        test_converter.run()

    end = datetime.now()
    # print the string to terminal with blue color
    print('\n')
    print_progress(f'Conversion completed at {end}')
    print_progress(f'Time taken: {end - start}')
    # revert to default color


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Upgrade AngularJS to Angular')
    parser.add_argument('-c', '--code_path', help='path to the code file',
                        default=None, required=False)
    parser.add_argument('-t', '--test_path', help='path to the test file',
                        default=None, required=False)
    args = parser.parse_args()

    code_path = args.code_path
    print_progress(f'code path: {code_path}')
    if code_path:
        assert os.path.exists(code_path)

    test_path = args.test_path
    print_progress(f'test path: {test_path}')
    if test_path:
        assert os.path.exists(test_path)
        assert 'spec' in test_path  # ensure it is a test file

    upgrade(code_path, test_path)
