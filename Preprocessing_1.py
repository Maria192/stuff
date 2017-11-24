# installations: docx2txt, pdf.miner.six
# author: Terekhina Maria

import docx2txt
import io
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def remove_ending(text):
    '''
    Remove bibliography.
    '''
    text = re.sub('(Литература|Список( использованной)? литературы|Библиография)(\.)?.*', '', text, flags=re.S)
    return text


def remove_begining(text):
    '''
    Remove all before introduction
    '''
    text = re.sub('.*?Введение(\.)?', 'Введение', text, flags=re.S)
    return text


def clean_text(text):
    '''
    Remove page numbers and system symbols
    '''
    text = re.sub('\n+', '\n', text)
    text = re.sub('\f', '\n', text)
    text = re.sub('\n+( )*[0-9]+( )*\n+', '', text)
    text = remove_begining(text)
    text = remove_ending(text)
    return text


def convert_pdf_to_txt(path):
    '''
    Convert pdf to plain text
    '''
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return clean_text(text)


def document_to_text(path):
    '''
    Choose a convertor for the file: pdf or docx
    '''
    if path[-5:] == ".docx":
        text = docx2txt.process(path)
        return clean_text(text)
    elif path[-4:] == ".pdf":
        return convert_pdf_to_txt(path)


if __name__ == '__main__':
    print(document_to_text(input('Введите полный путь к файлу: ')))

