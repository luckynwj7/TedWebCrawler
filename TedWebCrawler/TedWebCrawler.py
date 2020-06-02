from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import sys

creatorFile = open("C:\\result\\1 Creator.wonjong.Noh.txt", 'w', encoding="UTF8")
creatorFile.close

language = ""
while True:
    print ("추출할 언어(한국어:ko, 영어:en)입력")
    language = input()
    if language != "en" and language != "ko":
        print("지원하지 않는 언어입니다. 다시 입력해주세요.")
    else:
        break

startPage = 1
endPage = 2
while True:
    print ("검색을 시작할 페이지 입력")
    startPage = input()
    if int(startPage) < 1:
        print("0보다 큰 정수를 입력하세요.")
    else:
        break

while True:
    print("검색을 종료할 페이지 입력")
    endPage = input()
    if int(endPage) < int(startPage):
        print("범위를 초과하였습니다. 다시 입력해주세요. 현재 시작 페이지는 " + startPage + "입니다.")
    else:
        break

print("로딩 지연 시간 입력(정수로 입력하세요. 2초가 적당하며, PC의 인터넷 연결 상태에 따라 결과가 달라질 수 있습니다)")
sleepTime = input()



currentPath = os.path.dirname( os.path.abspath( __file__ ) )
print("실행 파일 경로 : " + currentPath)
try:
    driver = webdriver.Chrome(currentPath + '\chromedriver.exe')
except:
    print("실행 파일 경로 내에 버전에 맞는 크롬 드라이버가 없어 10초 후 실행을 종료합니다.")
    sleep(10)
    sys.exit()

"""1페이지부터 106페이지까지"""
serverNum = 1
for serverNum in range(int(startPage), int(endPage)):
    tempUrl = "https://www.ted.com/talks?language=ko&page=" + str(serverNum)

    html = urlopen(tempUrl)
    bsObject = BeautifulSoup(html, "html.parser")
    bsObject = bsObject.find_all('div', class_='talk-link')
    findLink = []
    errorCount = 1

    for link in bsObject:
        strObject = str(link)
        startPosition = strObject.find("<a")
        strObject = strObject[startPosition+1:len(strObject)]
        startPosition = strObject.find("href")
        endPosition = strObject.find("language=ko")
        strObject = strObject[startPosition+6:endPosition-1]
        strObject = "https://www.ted.com" + strObject + "/transcript?language=" + language
        findLink.append(strObject)

    for inLink in findLink:
        print("-------------------------구분자-------------------------")
        """링크 내에서 제목 찾기"""
        testObj = inLink
        try:
            html = urlopen(testObj)
        except:
            exceptFile = open("C:\\result\\2 linkErrorFile " + str(errorCount) + "(page" + str(serverNum) +").txt", 'w', encoding="UTF8")
            exceptFile.write(inLink)
            errorCount += 1
            exceptFile.close
            continue
        bsObject = BeautifulSoup(html, "html.parser")
        bsObject = bsObject.find_all('title')
        strObject = str(bsObject)
        startPosition = strObject.find(":")
        endPosition = strObject.find("TED Talk")
        strObject = strObject[startPosition+2:endPosition-3]
        titleName = strObject
        if titleName == "" :
            exceptFile = open("C:\\result\\2 titleNameErrorFile " + str(errorCount) + "(page" + str(serverNum) +").txt", 'w', encoding="UTF8")
            exceptFile.write(inLink)
            errorCount += 1
            exceptFile.close
            continue

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

        print(titleName + "\n")
        if os.path.isfile("C:\\result\\" + titleName + ".txt") :
            print(titleName + "가 이미 존재함")
            continue

        savePath = "C:\\result\\" + titleName + ".txt"


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
        sleep(int(sleepTime))
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
        indexErrorFlag = False
        for text in lastStrList:
            try:
                result += timeList[count]
            except:
                IndexErrorFlag = True
                break
            result += "\n"
            result += text
            result += "\n\n"
            count +=1

        if indexErrorFlag :
            exceptFile = open("C:\\result\\2 timeErrorFile " + str(errorCount) + "(page" + str(serverNum) +").txt", 'w', encoding="UTF8")
            exceptFile.write(inLink)
            errorCount += 1
            exceptFile.close
            indexErrorFlag = False
            continue
        
        print(result)



        f = open(savePath, 'w', encoding="UTF8")
        f.write(result)
        f.close