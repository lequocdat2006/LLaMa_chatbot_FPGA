import string
import re
def tokenization(text):
    translator = str.maketrans('', '', string.punctuation)
    text_no_punc = text.translate(translator)
    tokens = text_no_punc.split()
    return tokens
def remove_stopwords(tokens, vietnamese_stopwords_DIC_PATH):
    if not hasattr(remove_stopwords, "cache"):
        stopwords = set()
        try:
            with open(f"{vietnamese_stopwords_DIC_PATH}/vietnamese-stopwords.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        line = line[0].lower() + line[1:]
                    if line:
                        stopwords.add(line)
        except FileNotFoundError:
            print("Lỗi: Không tìm thấy file 'vietnamese-stopwords.txt'!")
            return tokens
        remove_stopwords.cache = stopwords
        remove_stopwords.max_len = max((len(phrase.split()) for phrase in stopwords), default=0)
    stopwords = remove_stopwords.cache
    max_len = remove_stopwords.max_len
    result = []
    i = 0
    n = len(tokens)
    while i < n:
        match_found = False
        for length in range(min(max_len, n - i), 0, -1):
            phrase = " ".join(tokens[i:i + length])
            if phrase:
                if i == 0:
                    phrase = phrase[0].lower() + phrase[1:]
            if phrase in stopwords:
                i += length
                match_found = True
                break
        if not match_found:
            result.append(tokens[i])
            i += 1
    return result
def make_sentence(tokens):
    sentences = " ".join(tokens)
    return sentences
def pre_processing(input_text, vietnamese_stopwords_DIC_PATH):
    content = input_text
    for i in range(len(content)):
        tokens = tokenization(content[i])
        tokens = remove_stopwords(tokens, vietnamese_stopwords_DIC_PATH)
        content[i] = make_sentence(tokens)
    return content