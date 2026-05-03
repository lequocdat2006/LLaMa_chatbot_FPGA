import string
import re
def tokenization(text):
    translator = str.maketrans('', '', string.punctuation)
    text_no_punc = text.translate(translator)
    tokens = text_no_punc.split()
    return tokens
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
    for paragraph in paragraphs:
        tokens = tokenization(paragraph)
        print(tokens)
        nomalization(tokens)
        print(tokens)
main()