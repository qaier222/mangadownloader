import math
import random

import requests
from bs4 import BeautifulSoup as bs
import os
import time
import sys
import re
from PIL import Image



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
headers2 = {
    'authority': 'bu3.mkklcdnv6tempv3.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://readmanganato.com/',
    'accept-language': 'en-US,en;q=0.9,ar-SA;q=0.8,ar;q=0.7',
}

def deletead(style):
    pattren = "text-align: \w*; max-width: \w*px; max-height: \w*px; margin: \w*px auto; overflow: hidden; display: block;"
    pattren2 = "max-height: \d*px; text-align: center; width: \d*px; margin: \d*px auto; overflow: hidden; max-width: 100%;"
    # print("enters deletead : ",style)
    if style:
        return re.match(pattren,style) or re.match(pattren2,style)
# r = requests.get('https://s61.mkklcdnv6tempv2.com/mangakakalot/b2/bv926033/chapter_3/2.jpg', headers=headers)

def download(urlQ="", chapterslistQ=[], pathQ="", progress_callback="",site=True,pdf=False):
    print("download called")
    print("chapters : ",chapterslistQ)
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if not urlQ:

        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "https://manganato.com/manga-fv982930"  # example

    else:
        url = urlQ
    if url[-1] == "/":
        print("det")
        url = url.rstrip("/")
    r = requests.get(url)
    url = r.url  # to account for redirections
    soup = bs(r.text, "html.parser")
    # print(html.findAll('img'))
    images = soup.findAll('img')
    src = []
    # scripts = soup.findAll("script")
    # for script in scripts:
    #     script.extract()

    # print (src)
    chapters = []
    chaptersnames = []
    print(len(soup.findAll('a')))
    for link in soup.findAll('a'):

        if link.has_attr('href'):
            if str(link['href']).find(url.split("/")[len(url.split("/")) - 1] + "/") != -1:
                # print(link['href'])
                chapters.append(link['href'])
                chaptersnames.append(link.text)

    print("chapters : ", chapters)
    print("chapters names : ", chaptersnames)
    # html = r.text

    print(r.status_code)
    # print(r.history)
    # print(r.url)
    # print(r.reason)
    # print(r.headers)
    # print(r)
    # print(chapters)
    directory = "manga"
    parent_dir = os.getcwd()
    manganame = soup.find("h1").text

    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    manganame = re.sub(rstr, "_", manganame)
    print(manganame)
    if pathQ:
        path = os.path.join(pathQ, manganame)
    else:
        path = os.path.join(parent_dir, directory, manganame)
    path = path.strip()
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + "/poster.jpg", "wb") as img:
        poster = soup.findAll("img")[-2]["src"]
        q = requests.get(poster, headers=headers)

        if not q.ok:
            print(q.status_code)

        for block in q.iter_content(1024):
            if not block:
                break

            img.write(block)
    print(len(chapters))
    chapters = chapters[::-1]  # reversing using list slicing
    chaptersnames = chaptersnames[::-1]
    ogchaptersnames = chaptersnames.copy()
    for index, fix in enumerate(chaptersnames):  # remove illegal path names
        rstr = r"[\/\\\:\*\?\"\<\>\|\.]"  # '/ \ : * ? " < > | .'
        chaptersnames[index] = re.sub(rstr, "_", chaptersnames[index])

    if True:
        print("qlist", len(chapterslistQ))
        i = 1
        for chapternum, chapter in enumerate(chapters):
            if chapterslistQ and not ogchaptersnames[chapternum] in chapterslistQ:
                print("no match")
                print("chaptersnames[chapternum] : ", ogchaptersnames[chapternum])
                continue


            succ = False  # for requesting loop
            # print("enterd 2")
            if os.path.exists(os.path.join(path, chaptersnames[
                chapternum])):  # if a already downloaded exist skip to the next one
                continue
            while not succ:  # for if the requests are too much
                try:
                    r = requests.get(chapter, headers=headers)
                except Exception as e:
                    print("err : ", e)
                    print("too many tries will sleep for two minutes")
                    time.sleep(2 * 60)
                else:
                    succ = True
                    print("downloading : ", chaptersnames[chapternum])
                    chaptername = chaptersnames[chapternum].strip();

            print("r.url ", r.url)
            print(r.status_code)
            soup = bs(r.text, "html.parser")
            src = []
            num = 0
            newsrc = []
            newnum = 0
            images = soup.findAll('img')
            newnew1 = 0

            for index, image in enumerate(images):
                # print("enterd 3")
                # print image source

                if str(image['src']).find("mkk") != -1:
                    # print(image['src'])
                    ex = "." + image['src'].split(".")[len(image['src'].split(".")) - 1]
                    newsrc.append(os.path.join(path, chaptername, str(newnew1) + ex))
                    newnew1 = newnew1 + 1
                    src.append(image['src'])
            # print("src after loop ",src)
            # print("new src after loop",newsrc)
            topdf = []
            for index, imgg in enumerate(src):  # create the images
                # print("enterd 4")


                if not os.path.exists(os.path.join(path, chaptername)):  # 1000teachet/ 0
                    os.mkdir(os.path.join(path,
                                          chaptername.strip()))  # getting the chapter from the url os.mkdir(os.path.join(path,str(str(chapter).split('/')[len(str(r.url).split('/'))-1])))
                with open(os.path.join(path, chaptername, str(index)) + '.jpg',
                          'wb') as handle:  # with open(os.path.join(path,str(chapternum),str(index))+'.jpg', 'wb') as handle:
                    while True:
                        auth = re.search(r"\w*\.\w*\.\w*",imgg).group()
                        headers["authority"] = auth
                        # print(f"imgg : {imgg}")

                        q = requests.get(imgg, headers=headers)
                        if q.ok:
                            break
                        q = requests.get(imgg, headers=headers2)
                        if q.ok:
                            break
                        print("couldnt download image stsus code:",q.status_code)
                        print("will sleep for 1 minutes")
                        time.sleep(1*60)



                    for block in q.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)
                if(pdf):
                    if(index == 0):
                        image1 = Image.open(os.path.join(path, chaptername, str(index)) + '.jpg')
                        im1 = image1.convert('RGB')
                    else:
                        image2 = Image.open(os.path.join(path, chaptername, str(index)) + '.jpg')
                        im2 = image2.convert('RGB')
                        topdf.append(im2)
                newnew = 0
                for index, image in enumerate(images):  # write new src
                    # print("enterd 5")

                    if str(image['src']).find("mkk") != -1:
                        # print("new src ",newsrc)
                        # print("new num ",newnum)
                        image['src'] = newsrc[newnew]
                        newnew = newnew + 1
                try:
                    soup.findAll("a", {"class": "navi-change-chapter-btn-next a-h"})[0]['href'] = os.path.join(path,
                                                                                                               chaptersnames[
                                                                                                                   chapternum + 1],
                                                                                                               "index.html")
                    soup.findAll("a", {"class": "navi-change-chapter-btn-next a-h"})[1]['href'] = os.path.join(path,
                                                                                                               chaptersnames[
                                                                                                                   chapternum + 1],
                                                                                                               "index.html")
                except Exception as e:
                    pass
                try:
                    soup.findAll("a", {"class": "navi-change-chapter-btn-prev a-h"})[0]['href'] = os.path.join(path,
                                                                                                               chaptersnames[
                                                                                                                   chapternum - 1],
                                                                                                               "index.html")
                    soup.findAll("a", {"class": "navi-change-chapter-btn-prev a-h"})[1]['href'] = os.path.join(path,
                                                                                                               chaptersnames[
                                                                                                                   chapternum - 1],
                                                                                                               "index.html")
                except Exception as e:
                    pass
                try:
                    with open("newcss.txt", "r", encoding="utf-8") as new:
                        with open("oldcss.txt", "r", encoding="utf-8") as old:
                            newcss = new.read().replace("tobereplaced", os.path.join(os.getcwd(), "css"))
                            soup = bs(str(soup).replace(old.read(), newcss),"html.parser")
                            # print("css replaced")
                except Exception as e:
                    pass

                try:
                    soup = bs(str(soup).replace("https://readmanganato.com/themes/hm/js/custom-chapter.js?v=1.1.4",
                                             os.path.join(os.getcwd(), "js", "selectchange.js")),"html.parser")
                except Exception as e:
                    print("couldnt replace select script")
                    print(e)

                # try:
                #    print("content")
                #    print(soup.find("div",{"style":"text-align: center; max-width: 620px; max-height: 310px; margin: 10px auto; overflow: hidden; display: block;"}))
                #
                #
                # except Exception as e:
                #     print("couldnt remove ad1")
                #     print(e)

                #
            if (site):
                print("writing html")
                with open(os.path.join(path, chaptername, "index.html"), "w", encoding="utf-8") as file:
                    try:

                        ad = soup.findAll("div",
                                       style=deletead)
                        # print("ad len: ",len(ad))

                        for aa in ad:
                            # print("trying to dec")
                            aa.decompose()
                            # print("deced")

                    except Exception as e:
                        print("couldnt delete ad")
                        print(e)



                    file.write(str(soup))
            if(pdf):
                im1.save(os.path.join(path, chaptername,chaptername+".pdf"),save_all=True, append_images=topdf)
            if progress_callback:
                try:
                    progress_callback.emit(math.ceil((i/len(chapterslistQ))*100))
                except Exception as e:
                    print(e)
                # print("update",update)
            i +=1
        print("finished")
        return "success"

def test(x):
    print("gg.test entees")
    for i in range(10):
        time.sleep(random.randint(0,5))
        try:
            print(x)
            # print((i+1)*10)
            # x((i+1)*10)
            print((i+1)*10)
            x.emit((i+1)*10)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    download()
