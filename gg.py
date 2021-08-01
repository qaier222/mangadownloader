import requests
from bs4 import BeautifulSoup as bs
import os
import time
import sys

headers = {
    'authority': 's61.mkklcdnv6tempv2.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://readmanganato.com/',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': '^\\^6050247a-28624d^\\^',
    'if-modified-since': 'Tue, 16 Mar 2021 03:22:34 GMT',
}

# r = requests.get('https://s61.mkklcdnv6tempv2.com/mangakakalot/b2/bv926033/chapter_3/2.jpg', headers=headers)


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = "https://manganato.com/manga-lo989297"  # it sholudnt have / at the end

r = requests.get(url)
url = r.url # to account for redirections
soup = bs(r.text, "html.parser")
# print(html.findAll('img'))
images = soup.findAll('img')
src = []
# for image in images:
#     # print image source
#     if str(image['src']).find("mkk") != -1 :
#         print(image['src'])
#         src.append(image['src'])
# print (src)
chapters = []
chaptersnames = []
print(len(soup.findAll('a')))
for link in soup.findAll('a'):

    if link.has_attr('href'):
        if str(link['href']).find(url.split("/")[len(url.split("/"))-1]+"/") != -1:
            # print(link['href'])
            chapters.append(link['href'])
            chaptersnames.append(link.text)

print("chapters : ",chapters)
print("chapters names : ",chaptersnames)
# html = r.text

print(r.status_code)
print(r.history)
print(r.url)
print(r.reason)
print(r.headers)
print(r)
# print(chapters)
directory = "manga"
parent_dir = os.getcwd()
manganame = soup.find("h1").text
print(manganame)
path = os.path.join(parent_dir, directory,manganame)
if not os.path.exists(path):
    os.mkdir(path)
# print(path) #C:\Users\hussain\PycharmProjects\mng\manga\10000teacher
print(len(chapters))
chapters = chapters[::-1] #reversing using list slicing
chaptersnames = chaptersnames[::-1]

if True:
    #print("enterd 1")
    for chapternum,chapter in enumerate(chapters):
        succ = False
        #print("enterd 2")
        if os.path.exists( os.path.join(path,str(chapternum))): #if a already downloaded exist skip to the next one
            continue
        while not succ: #for if the requests are too much
            try:
                r = requests.get(chapter, headers=headers)
            except Exception as e:
                print("too many tries will sleep fro two minutes")
                print("err : ",e)
                time.sleep(2*60)
            else:
                succ=True
                print("downloading : ",chaptersnames[chapternum])


        print("r.url ",r.url)
        print(r.status_code)
        soup = bs(r.text, "html.parser")
        src = []
        num = 0
        newsrc = []
        newnum=0
        images = soup.findAll('img')
        newnew1=0

        for index,image in enumerate(images):
            #print("enterd 3")
            # print image source

            if str(image['src']).find("mkk") != -1 :
                # print(image['src'])
                ex = "."+image['src'].split(".")[len(image['src'].split(".")) - 1]
                newsrc.append(os.path.join(path,str(chapternum),str(newnew1)+ex))
                newnew1=newnew1+1
                src.append(image['src'])
        # print("src after loop ",src)
        # print("new src after loop",newsrc)
        for index,imgg in enumerate(src): # create the images
            #print("enterd 4")
            if not os.path.exists(os.path.join(path,str(chapternum))):# 1000teachet/ 0
                os.mkdir(os.path.join(path,str(chapternum))) # getting the chapter from the url os.mkdir(os.path.join(path,str(str(chapter).split('/')[len(str(r.url).split('/'))-1])))
            with open(os.path.join(path,str(chapternum),str(index))+'.jpg', 'wb') as handle:

                q = requests.get(imgg, headers=headers)


                if not q.ok:
                    print(q.status_code)


                for block in q.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)


            newnew= 0
            for index,image in enumerate(images): #write new src
                #print("enterd 5")

                if str(image['src']).find("mkk") != -1 :
                    # print("new src ",newsrc)
                    # print("new num ",newnum)
                    image['src'] = newsrc[newnew]
                    newnew = newnew+1
            try:
                soup.findAll("a", {"class": "navi-change-chapter-btn-next a-h"})[0]['href'] = os.path.join(path,str(chapternum+1),"index.html")
                soup.findAll("a", {"class": "navi-change-chapter-btn-next a-h"})[1]['href'] = os.path.join(path, str(chapternum + 1), "index.html")
            except Exception as e:
                pass
            try:
                soup.findAll("a", {"class": "navi-change-chapter-btn-prev a-h"})[0]['href'] = os.path.join(path,str(chapternum - 1),"index.html")
                soup.findAll("a", {"class": "navi-change-chapter-btn-prev a-h"})[1]['href'] = os.path.join(path, str(chapternum - 1), "index.html")
            except Exception as e:
                pass
            try:
                with open("newcss.txt","r",encoding="utf-8") as new:
                    with open("oldcss.txt", "r", encoding="utf-8") as old:
                        newcss = new.read().replace("tobereplaced",os.path.join(os.getcwd(),"css"))
                        soup = str(soup).replace(old.read(),newcss)
                        # print("css replaced")
            except Exception as e:
                pass
            # try:
            #    print("content")
            #    print(soup.find("div",{"style":"text-align: center; max-width: 620px; max-height: 310px; margin: 10px auto; overflow: hidden; display: block;"}))
            #
            #
            # except Exception as e:
            #     print("couldnt remove ad1")
            #     print(e)



            #
            with open(os.path.join(path,str(chapternum),"index.html"), "w",encoding="utf-8") as file:

                file.write(str(soup))
    print("finished a chapter loop")