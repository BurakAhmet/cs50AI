import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    loaded = dict()

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if file.endswith(".txt"):
            with open(path) as f:
                loaded[file] = f.read()

    return loaded


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    phrases = nltk.word_tokenize(document.lower())
    words = [x for x in phrases if x not in string.punctuation and x not in nltk.corpus.stopwords.words("english")]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    counter = dict()
    for document in documents:
        for word in set(documents[document]):
            try:
                counter[word] += 1
            except KeyError:
                # Initialize the dictionary
                counter[word] = 1

    idf_dict = {x: math.log(len(documents) / counter[x]) for x  in counter}

    return idf_dict



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    for file, words in files.items():
        tf_idfs[file] = 0
        for word in query:
            if word in words:
                tf_idfs[file] += idfs[word] * words.count(word)

    sorted_list = sorted(tf_idfs, key=lambda x: tf_idfs[x], reverse=True)

    return sorted_list[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = dict()

    for sentence, words in sentences.items():
        rank = 0
        word_count = 0
        for word in query:
            if word in words:
                rank += idfs[word]
                word_count += words.count(word)

        if rank != 0 and word_count != 0:
            density = word_count / len(words)
            ranks[sentence] = (rank, density)

    sorted_list = [x[0] for x in sorted(ranks.items(), key=lambda y: (y[1], y[1]), reverse=True)]

    return sorted_list[:n]


if __name__ == "__main__":
    main()
