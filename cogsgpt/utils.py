from __future__ import annotations

import os
from urllib.parse import urlparse
import tiktoken

from cogsgpt.schema import FileSource

def detect_file_source(file_path: str) -> FileSource:
    """
    Detect whether the input is a local file path or a web URL.

    Args:
        file_path (str): The input file path or web URL.

    Returns:
        FileSource: The detected file source.

    Raises:
        ValueError: If the input is neither a local file path nor a web URL.
    """
    # Check if the input is a local file path
    if os.path.isfile(file_path):
        return FileSource.LOCAL

    # Check if the input is a web URL
    parsed_url = urlparse(file_path)
    if parsed_url.scheme and parsed_url.netloc:
        return FileSource.REMOTE

    # If the input is neither a local file path nor a web URL, raise an exception
    raise ValueError("Input must be a local file path or a web URL")

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The input text string.
        encoding_name (str, optional): The name of the encoding to use. Defaults to "cl100k_base".

    Returns:
        int: The number of tokens in the input text string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens