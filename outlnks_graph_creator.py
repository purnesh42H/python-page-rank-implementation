#!/usr/bin/env python

import urllib
import re
import time
import os

corpusPath  = os.getcwd() + '\\Corpus\\Task1'
indexFile   = os.getcwd() + '\\G1.txt'
urlFilePath = os.getcwd() + '\\wiki_urls_Task1.txt'
outLinkFile = os.getcwd() + '\\outLinks.txt'
docIdLinkList = []

def getHtmlText(link, fileName):
    with open(fileName, 'r') as htmlFile:
        htmlText        = htmlFile.read()
    return htmlText

def getAllQualifiedUrls(htmlText, regexExpression):
    pattern             = re.compile(regexExpression)
    newLinks            = re.findall(pattern,htmlText)
    return newLinks

def extractOutLinks(inlink, wikiLinks, outFile):
    strOutLinks = ''
    for link in wikiLinks:
        potentialLink = link.split('"')[0]
        newLink = ''
        if ':' not in potentialLink:
            if '#' in potentialLink and 'cite' not in potentialLink.lower():
                if '/wiki/' in potentialLink.lower():
                    newLink = potentialLink.split('#')[0].replace('/wiki/','')
            else:
                newLink = potentialLink
            if newLink in docIdLinkList:
                outFile.write(inlink + ',' + newLink + '\n')

def aggregateByInLink(line, allOccurences, inFile):
    outLinksStr = ''
    for occurence in allOccurences:
        if occurence not in outLinksStr and occurence != line:
            outLinksStr += occurence + ' '
    inFile.write(outLinksStr + '\n')

def getCallers(link, text):
     pattern = re.compile(r'\n(.+?),\b%s\b\n' % link)
     return re.findall(pattern,text)

with open(urlFilePath,'r') as urlFile:
    inLinkList = urlFile.readlines()
    docIdLinkList = map(lambda each: each.split('/')[len(each.split('/')) - 1].replace('\n',''), inLinkList)
    fileIndex = 1
    
    with open(outLinkFile,'a+') as outFile:
        for line in inLinkList:
            htmlText = getHtmlText(line, corpusPath + '\\%s.txt' % line.split('/')[len(line.split('/')) - 1].replace('\n',''))
            wikiLinks = getAllQualifiedUrls(htmlText, '<a href="/wiki/(.+?)"')
            extractOutLinks(line.split('/')[len(line.split('/')) - 1].replace('\n',''), wikiLinks, outFile)
            fileIndex += 1
            print 'File %d' % fileIndex
    fileIndex = 1
    with open(outLinkFile,'r') as outFile:
        outLinkList = outFile.read()
        with open(indexFile,'a+') as inFile:
            for line in docIdLinkList:
                inFile.write(line + ' ')
                fileIndex += 1
                aggregateByInLink(line, getCallers(line, outLinkList), inFile)
                print 'File %d' % fileIndex

    print 'finished'
                               




    
    
