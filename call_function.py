from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

working_directory = "calculator"

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    result = ""
    if function_call.name == 'get_files_info':
        result = get_files_info(working_directory, **function_call.args)
    if function_call.name == 'get_file_content':
        result = get_file_content(working_directory, **function_call.args)
    if function_call.name == 'run_python_file':
        result = run_python_file(working_directory, **function_call.args)
    if function_call.name == 'write_file':
        result = write_file(working_directory, **function_call.args)
    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result},
                )
            ],
        )



