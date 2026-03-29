import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info,schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read the content of a file
    - Write to a file (create or update)
    - Run a Python file with optional arguments

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)
    verbos_flag = False

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbos_flag = True
    prompt = sys.argv[1]

    messages = [
        types.Content(role='user', parts=[types.Part(text=prompt)])
    ]

    available_function = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,

        ]
    )
    config = types.GenerateContentConfig(
        tools=[available_function],
        system_instruction=system_prompt
    )
    

    response = client.models.generate_content(
        model='gemini-1.5-flash', 
        contents=messages,
        config=config
    )
    if response is None or response.usage_metadata is None:
        print("Response is mailformed.")
        return
    if verbos_flag:
        print(f"User prompts: {prompt}")
        print(f"Prompt  token: {response.usage_metadata.prompt_token_count}")
        print(f"Response  token: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, verbos_flag)
            print(result)
            print(f"Calling functions: {function_call.name}({function_call.args})")
    else:
        print(response.text)

    


main()