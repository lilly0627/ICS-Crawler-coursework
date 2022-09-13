import requests
from bs4 import BeautifulSoup
import re

# For question 2
def pageLength(path: str):
    file1 = open("pageLength.txt", "a") # page with length, "pageLength.txt" in submission
    wordCount = 0
    longestPage = "";
    longestLength = 0;
    with open(path, 'r', encoding='utf-8') as myFile:
        for line in myFile:  # read file line by line
            try:
                link = line.strip()
                response = requests.get(link)
                soup = BeautifulSoup(response.content, 'html.parser')
                for i in re.split(r'(\w+)', soup.get_text().rstrip()):
                    wordCount += 1
                file1.write(link + '    ' + str(wordCount) + '\n')
                if wordCount > longestLength:
                    longestPage = link
                    longestLength = wordCount
                wordCount = 0
                print('Finish    ', link)
            except:
                print("some error occured.")
    print("Longest page is " + longestPage + "   word count: " + str(longestLength))

def longestPage(path: str):
    longestPage = ""
    longestLength = 0
    pageDict = {}
    with open(path, 'r', encoding='utf-8') as myFile:
        for line in myFile:
            link = line.strip().split('    ')[0]
            length = int(line.strip().split('    ')[1])

            pageDict[link] = length

            if length > longestLength:
                longestLength = length
                longestPage = link.split('    ')[0]
    print("Question 2 - Longest Page: ")
    count = 0
    for key, val in sorted(pageDict.items(), key=lambda x: x[1], reverse=True):
        print(key.split(" ")[0] + ", " + str(val))
        count += 1
        if count == 200:
            break
    print("Longest page: " + longestPage + ", word count: " + str(longestLength))

# run methods
#  pageLength('links.txt')
#  longestPage('pageLength.txt')


