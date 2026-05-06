'''
Write a Python program that reads a text file and counts the total number of words in it.Handle the case where the file does not exist using exception handling.
'''

def count_words(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
            words = text.split()
            return len(words)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return None

filename = "sample.txt"
word_count = count_words(filename)

if word_count is not None:
    print(f"Total number of words in '{filename}': {word_count}")
