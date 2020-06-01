from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os

creatorFile = open("C:\\result\\Creator.wonjong.Noh.txt", 'w', encoding="UTF8")
creatorFile.close

currentPath = os.path.dirname( os.path.abspath( __file__ ) )
driver = webdriver.Chrome(currentPath + '\chromedriver.exe')

"""1페이지부터 106페이지까지"""
serverNum = 1
for serverNum in range(1,106):
    tempUrl = "https://www.ted.com/talks?language=ko&page=" + str(serverNum)

    html = urlopen(tempUrl)
    bsObject = BeautifulSoup(html, "html.parser")
    bsObject = bsObject.find_all('div', class_='talk-link')
    findLink = []

    for link in bsObject:
        strObject = str(link)
        startPosition = strObject.find("<a")
        strObject = strObject[startPosition+1:len(strObject)]
        startPosition = strObject.find("href")
        endPosition = strObject.find("language=ko")
        strObject = strObject[startPosition+6:endPosition-1]
        strObject = "https://www.ted.com" + strObject + "/transcript?language=en"
        findLink.append(strObject)

    for inLink in findLink:
        print("-------------------------구분자-------------------------")
        """링크 내에서 제목 찾기"""
        testObj = inLink
        html = urlopen(testObj)
        bsObject = BeautifulSoup(html, "html.parser")
        bsObject = bsObject.find_all('title')
        strObject = str(bsObject)
        startPosition = strObject.find(":")
        endPosition = strObject.find("TED Talk")
        strObject = strObject[startPosition+2:endPosition-3]
        titleName = strObject
        print(titleName + "\n")


        """링크 내에서 내용 찾기"""
        testObj = inLink
        html = urlopen(testObj)
        bsObject = BeautifulSoup(html, "html.parser")
        bsObject = bsObject.find_all('p')
        strObject = str(bsObject)
        startPosition = 1
        endPosition = strObject.find("TED")
        strObject = strObject[startPosition:endPosition]
        strObject = strObject.replace("<p>","")
        strObject = strObject.replace("</p>, ","!splitArea!")
        prevStrList = strObject.split("!splitArea!")

        lastStrList = []
        """문장에서 개행 제거하기"""
        for scentence in prevStrList:
            scentence = scentence.replace("\n","")
            scentence = scentence.replace("\t","")
            scentence = scentence.replace(".", ". ")
            """의미 있는 문자열만 사용하기"""
            if len(scentence) > 0 :
                lastStrList.append(scentence)

        """링크 내에서 시간초 찾기"""
        timeList = []
        testObj = inLink
        driver.get(testObj)
        sleep(2)
        html = driver.page_source
        bsObject = BeautifulSoup(html, 'html.parser')
        bsObject = bsObject.select('button')
        strObject = str(bsObject)
        strList = strObject.split('>')

        for scentence in strList:
            if scentence[1:2] == ':' or  scentence[2:3] == ':' :
                if scentence[1:2] == ':' :
                    timeList.append(scentence[0:4])
                elif scentence[2:3] == ':':
                    timeList.append(scentence[0:5])


        """컨텐츠 합치기"""
        count = 0
        result = ""
        for text in lastStrList:
            result += timeList[count]
            result += "\n"
            result += text
            result += "\n\n"
            count +=1
        
        print(result)

        """이름으로 지을 수 없는 타이틀 내용 지우기"""
        titleName = titleName.replace("\\","")
        titleName = titleName.replace("/","")
        titleName = titleName.replace("?","")
        titleName = titleName.replace("|","")
        titleName = titleName.replace("*","")
        titleName = titleName.replace('"',"")
        titleName = titleName.replace('<',"")
        titleName = titleName.replace('>',"")
        titleName = titleName.replace(':',"")



        savePath = "C:\\result\\" + titleName + ".txt"
        f = open(savePath, 'w', encoding="UTF8")
        f.write(result)
        f.close