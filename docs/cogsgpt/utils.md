Module cogsgpt.utils
====================

Functions
---------

    
`detect_file_source(file_path: str) ‑> cogsgpt.schema.FileSource`
:   Detect whether the input is a local file path or a web URL.
    
    Args:
        file_path (str): The input file path or web URL.
    
    Returns:
        FileSource: The detected file source.
    
    Raises:
        ValueError: If the input is neither a local file path nor a web URL.