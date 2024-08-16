import os
from typing import List, Dict
from language_queries import get_query_for_language
import logging

logging.basicConfig(level=logging.INFO)

def list_files(directory: str) -> List[str]:
    """
    list_files function

    Parameters:
        directory (str): The directory path to list files from.

    Returns:
        List[str]: A list of file names in the directory or an error message if something goes wrong.
    """
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        logging.info(f"Listed files in directory: {directory}")
        return files
    except Exception as e:
        logging.error(f"Error listing files in directory {directory}: {str(e)}")
        return [f"Error listing files: {str(e)}"]

def read_file(file_path: str) -> str:
    """
    read_file function

    Parameters:
        file_path (str): The path of the file to read.

    Returns:
        str: The content of the file or an error message if something goes wrong.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Read file: {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    write_file function

    Parameters:
        file_path (str): The path of the file to write.
        content (str): The content to write to the file.

    Returns:
        str: A success message or an error message if something goes wrong.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f"Wrote to file: {file_path}")
        return f"File '{file_path}' has been written successfully."
    except Exception as e:
        logging.error(f"Error writing file {file_path}: {str(e)}")
        return f"Error writing file: {str(e)}"

def parse_file(file_path: str) -> Dict[str, List[str]]:
    """
    parse_file function

    Parameters:
        file_path (str): The path of the file to parse.

    Returns:
        Dict[str, List[str]]: A dictionary with parsed components or an error if parsing fails.
    """
    try:
        import tree_sitter
    except ImportError:
        logging.error("tree-sitter is not installed. Please install it to use advanced parsing.")
        return {}

    try:
        from tree_sitter import Language, Parser
    except ImportError:
        logging.error("Failed to import tree-sitter components. Please check your installation.")
        return {}

    file_extension = os.path.splitext(file_path)[1]
    if file_extension not in ['.py', '.js', '.java']:
        logging.warning(f"Parsing not supported for file type: {file_extension}")
        return {"error": [f"Parsing not supported for this file type: {file_extension}"]}

    language_name = get_query_for_language(file_extension)
    if not language_name:
        logging.warning(f"No query available for language with extension: {file_extension}")
        return {"error": [f"No query available for language with extension: {file_extension}"]}

    try:
        LANGUAGE = Language(f'build/my-languages.so', language_name)
        parser = Parser()
        parser.set_language(LANGUAGE)

        with open(file_path, 'r') as file:
            content = file.read()

        tree = parser.parse(bytes(content, "utf8"))
        query_string = get_query_for_language(file_extension)
        query = LANGUAGE.query(query_string)

        captures = query.captures(tree.root_node)
        
        definitions = {
            "classes": [],
            "functions": [],
            "methods": [],
            "imports": [],
            "exports": []
        }

        for capture in captures:
            capture_type = capture[1]
            name = content[capture[0].start_byte:capture[0].end_byte].strip()
            if capture_type == "definition.class":
                definitions["classes"].append(name)
            elif capture_type == "definition.function":
                definitions["functions"].append(name)
            elif capture_type == "definition.method":
                definitions["methods"].append(name)
            elif capture_type == "name.import":
                definitions["imports"].append(name)
            elif capture_type == "name.export":
                definitions["exports"].append(name)

        logging.info(f"Parsed file: {file_path} with definitions: {definitions}")
        return definitions

    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {str(e)}")
        return {"error": [f"Error parsing file: {str(e)}"]}
