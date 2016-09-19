import re
import urllib.request  # импортируем модуль

def writen(html):
    fw = open('written.txt','w', encoding = 'ISO-8859-1')
    fw.write(html)
    fw.close()

    
def clean(titles):
    new_titles = []
    regTag = re.compile('<.*?>', flags= re.DOTALL)
    
    for t in titles:
        clean_t = regTag.sub("", t)
        clean_t = clean_t.replace('&hellip;', '...')
        new_titles.append(clean_t)
        
    for t in new_titles:
        print(t)  


def load():

    i = 288
    while i< 1000:
        
        url = 'http://www.forumishqiptar.com/threads/160'+str(i)  # адрес страницы, которую мы хотим скачать
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  # хотим притворяться браузером

        req = urllib.request.Request(url, headers={'User-Agent':user_agent})  
        # добавили в запрос информацию о том, что мы браузер Мозилла

        try:
            with urllib.request.urlopen(req) as response:
               html = response.read().decode('ISO-8859-1')
               wtiten(html)
               #print(html[:1000])
        except:
            i+=1
            

        res = '<blockquote class=".+?</blockquote>'
        titles = re.findall(res, html, flags= re.DOTALL)
        #print (titles)
        clean(titles)
        i+=1



    #print(len(titles))
    #print(titles[:3])

def main():
    load()

    
if  __name__ == '__main__':
    main()
