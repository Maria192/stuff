import re
import urllib.request
import os
import html

#июль 2015 года

def wtite_themes(text, refer):
    if not os.path.exists(plain):
        os.makedirs(plain)
    fw = open(name,'w', encoding = 'UTF-8')
    fw.write(d[key][0] + ' ' + d[key][1])
    fw.close()
    

def clean(t, refer):
    
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
    regReg = re.compile('\t|\n', flags=re.U | re.DOTALL)
    

    clean_t = regScript.sub("", t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = html.unescape(clean_t)
    clean_t = regReg.sub("", clean_t)
    write(clean_t)

    #os.system(r'C:\Users\Masha\Downloads\mystem-3.0-win7-32bit\mystem -cind ' + new_titles + r' C:\Users\Masha\Downloads\mystem-3.0-win7-32bit\done.txt')
    #print (r'C:\Users\Masha\Downloads\mystem-3.0-win7-32bit\mystem -cind ' + new_titles + r' C:\Users\Masha\Downloads\mystem-3.0-win7-32bit\done.txt')    


def get_types(html):

    pattern = '<ul class="tMenu2">(.+?)</li></ul></ul></div>'
    res = re.search(pattern, html)
    titles = res.group(1)
    pattern = '<a href="(.+?)"><span>'
    refers = re.findall(pattern, titles)
    return refers

    

def load_page(url):
    
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  # хотим притворяться браузером

    req = urllib.request.Request(url, headers={'User-Agent':user_agent})  
    # добавили в запрос информацию о том, что мы браузер Мозилла

    try:
        with urllib.request.urlopen(req) as response:
           html = response.read().decode('utf-8')
    except:
        print('Error at', url)
        
    return html

def amount_of_pages(page): #считает кол-во страниц в теме
    
    pattern = 'Страница 1 из (.+?)	</td>'
    res = re.search(pattern, page)
    pages = res.group(1)
    return pages

def name_of_article(rawText):

    regTag = re.compile('</span></a>(.+)', flags=re.U | re.DOTALL)
    res = re.search(regTag, rawText)
    text = res.group(1)

    clean(text)
    
    
def articles_info(refers): #get information about article
    
    for refer in refers:
        refer = 'http://www.zelpravda.ru' + refer
        article = load_page(refer)
        name_of_article(article)
        regTag = re.compile('<td valign="top">(.+?)<script>', flags=re.U | re.DOTALL)
        res = re.search(regTag, article)
        rawText = res.group(1)
        name_of_article(rawText)
        clean(rawText, refer)
        #print(rawText)
        
    

    

def article_refer(PageWithArticle): #собирает ссылки на статьи
    pattern = '<h1><a href="(.+?)" class="contentpagetitle">'
    refers = re.findall(pattern, PageWithArticle)
    articles_info(refers)


def articles_in_themes(pagesTheme): #загружает все страницы тем
    i = 0
    j = 0
    for refer in pagesTheme:
        while j < int(pagesTheme[refer]):
            PageWithArticle = load_page('http://www.zelpravda.ru' + refer + '?start=' + str(i))
            #print ('http://www.zelpravda.ru' + refer + '?start=' + str(i))
            article_refer(PageWithArticle)
            if '/obrazovanie.html' == refer or '/kultura.html' == refer or '/proisshestvija.html' == refer or '/obschestvo.html' == refer or '/sport.html' == refer or '/turizm.html' == refer:
                i += 4
            else:
                i += 8
            j += 1
        i = 0
        j = 0


def load_themes(refers):

    pagesTheme = {}
    
    for theme in refers:
        page = load_page('http://www.zelpravda.ru' + theme) # найти в конце этой страницы кол-во страниц в теме, пройти по ним циклом, собрать ссылки на новости.
        pages = amount_of_pages(page)
        pagesTheme[theme] = pages
        
    articles_in_themes(pagesTheme) 


def main():

    url = 'http://www.zelpravda.ru/sitemap.html'  # адрес страницы, которую мы хотим скачать
    html = load_page(url)
    refers = get_types(html)
    
    load_themes(refers)
    #print (themes)

    
if  __name__ == '__main__':
    main()
