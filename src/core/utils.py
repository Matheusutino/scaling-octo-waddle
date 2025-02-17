import os
import json
import numpy as np
import pandas as pd
from typing import Any, Union

def check_file_not_exists(file_path):
    """
    Check if a file exists at the given path and raise an error if it does.

    Args:
        file_path (str): The path to the file to be checked.

    Raises:
        FileExistsError: If the file exists at the specified path.
    """
    if os.path.isfile(file_path):
        raise FileExistsError(f"The file '{file_path}' already exists.")

def check_directory_exists(directory_path: str) -> None:
    """
    Checks if a directory exists and raises an error if it does.

    Args:
        directory_path (str): The path to the directory to check.

    Raises:
        FileExistsError: If the specified directory already exists.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        raise FileExistsError(f"The directory '{directory_path}' already exists.")

def create_directory(directory_path: str) -> bool:
    """Create a directory if it does not exist. Raise an error if it already exists.

    Args:
        directory_path (str): The path of the directory to create.

    Returns:
        bool: True if the directory was successfully created.
    
    Raises:
        FileExistsError: If the directory already exists.
        OSError: If an error occurs while creating the directory.
    """
    if os.path.exists(directory_path):
        raise FileExistsError(f"The directory '{directory_path}' already exists.")
    
    try:
        os.makedirs(directory_path)
        return True
    except OSError as e:
        print(f"Error creating directory: {e}")
        return False
    
def get_last_element_from_path(file_path: str) -> str:
    """Extract the last element from a given file path.

    Args:
        file_path (str): The file path from which to extract the last element.

    Returns:
        str: The last element of the path, or an empty string if the path is empty.
    """
    return os.path.basename(file_path)

def convert_ndarray_to_list(obj: Any) -> Union[list, Any]:
    """Convert a NumPy ndarray to a Python list for JSON serialization.
    
    Args:
        obj (Any): The object to be converted.
        
    Returns:
        Union[list, Any]: If the input is a NumPy ndarray, returns it as a list. 
                          Otherwise, raises a TypeError.

    Raises:
        TypeError: If the object is not serializable to JSON.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def read_json(file_path) -> dict:
    """Reads a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_value_by_key_json(file_path: str, key: str) -> str:
    """Reads a JSON file and retrieves the value associated with a given key.

    Args:
        file_path (str): The path to the JSON file.
        key (str): The key whose value needs to be fetched.

    Returns:
        any: The value associated with the key, or a message if the key is not found.
    """
    # Read the JSON file
    data = read_json(file_path)
    
    # Return the value for the given key
    return data.get(key, "Key not found")

def save_json(data: dict, filename: str) -> None:
    """Save a dictionary as a JSON file with proper indentation.
    
    Args:
        data (dict): The dictionary to be saved as a JSON file.
        filename (str): The file path where the JSON will be saved.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, default=convert_ndarray_to_list, indent=4)

def replace_character(input_string: str, old_char: str = '/', new_char: str = '_') -> str:
    """
    Replaces all occurrences of a specified character in a string with another character.

    Args:
        input_string (str): The original string in which to replace characters.
        old_char (str): The character to be replaced.
        new_char (str): The character to replace with.

    Returns:
        str: The modified string with all occurrences of old_char replaced by new_char.

    Example:
        >>> replace_character("/home/user/documents/file.txt", '/', '_')
        '_home_user_documents_file.txt'
    """
    return input_string.replace(old_char, new_char)

def get_all_files_in_directory(directory: str):
    """
    Retrieve all files in a specified directory.

    Args:
        directory (str): The path to the directory from which to retrieve files.

    Returns:
        list: A list of file paths in the specified directory.
    """
    files = []
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files.append(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
    return files

def get_all_npy_files_in_directory(directory: str):
    """
    Retrieve all .npy files in a specified directory and its subdirectories.

    Args:
        directory (str): The path to the directory from which to retrieve .npy files.

    Returns:
        list: A list of file paths to .npy files in the specified directory and subdirectories.
    """
    npy_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".npy"):
                    npy_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"An error occurred: {e}")
    return npy_files

def save_results(result_path, results):
    bayesian_search_cv = pd.DataFrame(results.cv_results_)
    bayesian_search_cv.to_csv(f"{result_path}/bayes_search_cv.csv", index=False)

    best_f1_row = bayesian_search_cv.loc[bayesian_search_cv["mean_test_f1_score"].idxmax()]

    best_f1_row = best_f1_row.to_dict()
    save_json(best_f1_row, f"{result_path}/results.json")


def get_prompt(key_name, json_path = "configs/prompts.json"):
    """
    Retrieve the `system_prompt` and `user_prompt` for a given key in a JSON object.

    Args:
        json_data (dict): The JSON object containing prompt configurations.
        key_name (str): The name of the key to retrieve the prompts for.

    Returns:
        dict: A dictionary containing `system_prompt` and `user_prompt` if the key exists, 
              or None if the key is not found.

    Raises:
        KeyError: If the provided key_name does not exist in the json_data.
    """
    json_data = read_json(json_path)
    if key_name in json_data:
        return json_data[key_name]["system_prompt"], json_data[key_name]["user_prompt"]
    else:
        raise KeyError(f"The key '{key_name}' does not exist in the JSON data.")
