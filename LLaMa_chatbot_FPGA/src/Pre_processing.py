import string
import re
def tokenization(text):
    translator = str.maketrans('', '', string.punctuation)
    text_no_punc = text.translate(translator)
    tokens = text_no_punc.split()
    return tokens
def remove_stopwords(tokens):
    stopwords_1 = {
        "gì", "ai", "đâu", "này", "kia", "đó", "ấy", "nào", "đây",
        "à", "ơi", "nhé", "nhá", "thôi", "đi", "cơ", "mà", "sắp",
        "đã", "đang", "sẽ", "vừa", "từng", "mới", "hơi", "khá", "tôi",
        "anh", "chị", "bạn", "họ", "tao", "ta", "nó", "là", "có",
        "cần", "được", "muốn", "phải", "nên", "bị", "như", "thế", "các",
        "những", "và", "hoặc", "nhưng", "trong", "trên", "dưới", "thì", "để",
        "bởi", "do", "với", "của", "theo", "khi", "từ", "đến", "giữa",
        "về", "ngoài", "càng", "cũng", "vẫn", "lại", "vì", "đối", "nêu", "năm", "dẫn"
    }
    stopwords_2 = {
        "chúng tôi", "chúng ta", "có thể"
    }
    result = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens):
            phrase = tokens[i].lower() + " " + tokens[i + 1].lower()
            if phrase in stopwords_2:
                i += 2
                continue
        if tokens[i].lower() not in stopwords_1:
            result.append(tokens[i])
        i += 1
    return result
def nomalization(tokens):
    for i, token in enumerate(tokens):
        t = token.lower()
        t = re.sub(r'[áàảãạăắằẳẵặâấầẩẫậ]', 'a', t)
        t = re.sub(r'đ', 'd', t)
        t = re.sub(r'[éèẻẽẹêếềểễệ]', 'e', t)
        t = re.sub(r'[íìỉĩị]', 'i', t)
        t = re.sub(r'[óòỏõọôốồổỗộơớờởỡợ]', 'o', t)
        t = re.sub(r'[úùủũụưứừửữự]', 'u', t)
        t = re.sub(r'[ýỳỷỹỵ]', 'y', t)
        tokens[i] = t
def main():
    f = input("Enter file name: ")
    file = open(f, mode = "r", encoding = "utf-8")
    content = file.read()
    file.close()
    paragraphs = content.split("\n")
    file_tokenization = open("tokenization.txt", "w", encoding = "utf-8")
    file_stopword_removal = open("fie_stopword_removal.txt", "w", encoding = "utf-8")
    file_normalization = open("normalization.txt", "w", encoding = "utf-8")
    for paragraph in paragraphs:
        tokens = tokenization(paragraph)
        file_tokenization.write(str(tokens) + '\n')
        tokens = remove_stopwords(tokens)
        file_stopword_removal.write(str(tokens) + '\n')
        nomalization(tokens)
        file_normalization.write(str(tokens) + '\n')
    file_tokenization.close()
    file_stopword_removal.close()
    file_normalization.close()
main()