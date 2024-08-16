# language_queries.py

LANGUAGE_QUERIES = {
    "python": """
(class_definition
  name: (identifier) @name.definition.class) @definition.class

(function_definition
  name: (identifier) @name.definition.function) @definition.function

(import_statement
  name: (dotted_name (identifier) @name.import)) @import

(import_from_statement
  name: (dotted_name (identifier) @name.import)
  (import_from_clause (identifier) @name.import)) @import
""",
    "javascript": """
(class_declaration
  name: (identifier) @name.definition.class) @definition.class

(function_declaration
  name: (identifier) @name.definition.function) @definition.function

(method_definition
  name: (property_identifier) @name.definition.method) @definition.method

(import_statement
  (import_clause (identifier) @name.import)) @import

(export_statement
  (export_clause (identifier) @name.export)) @export
""",
    "java": """
(class_declaration
  name: (identifier) @name.definition.class) @definition.class

(method_declaration
  name: (identifier) @name.definition.method) @definition.method

(import_declaration
  name: (scoped_identifier) @name.import) @import
""",
}

def get_query_for_language(file_extension):
    """
    get_query_for_language function

    Parameters:
        file_extension (str): The file extension to determine the language (e.g., .py, .js, .java)

    Returns:
        str: The query string for the specified language or an empty string if not supported.
    """
    extension_to_language = {
        ".py": "python",
        ".js": "javascript",
        ".java": "java",
    }
    language = extension_to_language.get(file_extension.lower())
    return LANGUAGE_QUERIES.get(language, "")
