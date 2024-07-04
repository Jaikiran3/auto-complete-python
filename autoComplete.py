import os
import sys

ALPHABET_SIZE = 60
MAX_SUGGESTION_SIZE = 10
DICTIONARY_FILE_NAME = "dictionary.txt"

class TrieNode:
    def __init__(self):
        self.children = [None] * ALPHABET_SIZE
        self.is_end_of_word = False


# Helper functions
def get_array_length(arr):
    count = 0
    while count < len(arr) and arr[count]:
        count += 1
    return count


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Trie functions
def insert(root, key):
    current_node = root
    for char in key:
        index = ord(char) - ord('A')
        if current_node.children[index] is None:
            current_node.children[index] = TrieNode()
        current_node = current_node.children[index]
    current_node.is_end_of_word = True


def possible_text_helper(node, key, possible_texts, idx):
    if idx[0] >= MAX_SUGGESTION_SIZE or node is None:
        return
    if node.is_end_of_word:
        possible_texts[idx[0]] = key
        idx[0] += 1
    for i in range(ALPHABET_SIZE):
        if node.children[i] is not None:
            char = chr(ord('A') + i)
            possible_text_helper(node.children[i], key + char, possible_texts, idx)


def search(root, key):
    current_node = root
    for char in key:
        index = ord(char) - ord('A')
        if current_node.children[index] is None:
            return [""] * MAX_SUGGESTION_SIZE
        current_node = current_node.children[index]
    possible_texts = [""] * MAX_SUGGESTION_SIZE
    idx = [0]
    possible_text_helper(current_node, key, possible_texts, idx)
    return possible_texts


def get_suggestions(root, key, suggestion_format):
    result = search(root, key)
    arr_size = get_array_length(result)
    for i in range(arr_size):
        suggestion_format[0] += result[i] + ", "
    return result


def insert_dictionary(auto_completion_node, file_name):
    try:
        with open(file_name, 'r') as dictionary:
            for word in dictionary:
                word = word.strip().upper()
                insert(auto_completion_node, word)
    except FileNotFoundError:
        print("Failed to open the file!")
        sys.exit(0)


def windows_operation(auto_completion_node):
    import msvcrt

    user_input = ""
    result = [""] * MAX_SUGGESTION_SIZE
    shift_key_pressed = False

    while True:
        suggestion_format = [""]

        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\r':
                break
            elif char == b'\t':
                user_input = result[0]
            elif char == b'\b':
                user_input = user_input[:-1]
                if user_input:
                    result = get_suggestions(auto_completion_node, user_input, suggestion_format)
            elif char == b'\xe0':
                shift_key_pressed = True
            else:
                char = char.decode('utf-8')
                if shift_key_pressed:
                    char = char.upper()
                user_input += char
                shift_key_pressed = False
                result = get_suggestions(auto_completion_node, user_input, suggestion_format)

            clear_screen()
            print(f">> {user_input}\n{suggestion_format[0]}")




def main():
    auto_completion_node = TrieNode()
    DICTIONARY_FILE_NAME = "J:\\AutoComplete\\words.txt"
    insert_dictionary(auto_completion_node, DICTIONARY_FILE_NAME)

    print(">> ", end="", flush=True)
    windows_operation(auto_completion_node)


if __name__ == "__main__":
    main()
