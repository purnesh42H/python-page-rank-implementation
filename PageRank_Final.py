#!/usr/bin/env python

import urllib
import re
import os
import math
import operator
import decimal
decimal.getcontext().prec = 10

G1_FilePath = os.getcwd() + '\\G1.txt'
G2_FilePath = os.getcwd() + '\\G2.txt'
Test_FilePath = os.getcwd() + '\\Test_Graph.txt'
statisticReport = os.getcwd() + '\\Task_1_Report.txt'
Task2_G1_Perplexity_File = os.getcwd() + '\\Task_2_G1_Perplexity.txt'
Task2_G2_Perplexity_File = os.getcwd() + '\\Task_2_G2_Perplexity.txt'
Task2_G1_Top50_File = os.getcwd() + '\\Task_2_G1_Top50.txt'
Task2_G2_Top50_File = os.getcwd() + '\\Task_2_G2_Top50.txt'

graphPages  = {}
d           = 0.85

class Page:
    
    def __init__(self, page, rank, inLinkPages, noOfOutLinks):
        self.page = page
        self.rank = rank
        self.inLinkPages = inLinkPages
        self.noOfOutLinks = noOfOutLinks  
        
    def setRank(self, value):
        self.rank = value

    def setnoOfOutLinks (self, value):
        self.noOfOutLinks = value

    def setinLinkPages (self, value):
        self.inLinkPages = value

def getSinkNodes():
    return {k:v for k,v in graphPages.iteritems() if v.noOfOutLinks == 0}

def getSourceNodes():
    return {k:v for k,v in graphPages.iteritems() if len(v.inLinkPages) == 0}

def getOutLinks(page):
    return {k:v for k,v in graphPages.iteritems() if page in v.inLinkPages}


def perplexity(entropy):
    return (pow (2, decimal.Decimal(entropy)))

def entropy(rank):
    entropy = rank * float(math.log(rank, 2))
    return entropy
    
def initializegraphPages(graphFile):
    with open(graphFile, 'r') as textFile:
        for line in textFile.readlines():
            if line == '' or line == 's' or line == '\n':
                continue
            pages = line.replace(' \n','').replace('\n','').split(' ')
            if(pages[0] != '' and pages[0] != 's'):
                if pages[0] in graphPages:
                    graphPages[pages[0]].setinLinkPages(pages[1:len(pages)])
                else:
                    graphPages[pages[0]] = (Page
                                        (pages[0], (float(1)/len(pages)),
                                        pages[1:len(pages)], 0))
            for restPage in pages[1:len(pages)]:
                if(restPage != '' and restPage != 's'):
                    if restPage in graphPages:
                        graphPages[restPage].noOfOutLinks += 1
                    else:
                        graphPages[restPage] = (Page
                                            (pages[0], (float(1)/len(pages)),
                                            [], 1))
            print '%d' % len(pages)
            print '%lf' % graphPages[restPage].rank
            raw_input()
            
            
def buildStatistics(graphName):
    with open(statisticReport, 'a+') as textFile:
        textFile.write(graphName + ":\n")
        noOutLinks = float(len(getSinkNodes()))/len(graphPages)
        noInLinks = float(len(getSourceNodes()))/len(graphPages)
        textFile.write("Proportion of pages with no out links: %f\n" % noOutLinks)
        textFile.write("Proportion of pages with no in links: %f\n" % noInLinks)
    
def calculatePageRank(sinkNodes):
    sinkPR = 0
    for node in sinkNodes:
        sinkPR += graphPages[node].rank

    pageIndex = 0
    totalEntropy = 0
    noOfPages = len(graphPages)
    
    for page in graphPages:
        newPR = (1-d)/noOfPages
        newPR += d*sinkPR/noOfPages
        inLinks = graphPages[page].inLinkPages
        for link in inLinks:
            newPR += d*graphPages[link].rank/graphPages[link].noOfOutLinks
        graphPages[page].setRank(newPR)
        totalEntropy += entropy(newPR)
        print 'entropy: %lf' % totalEntropy
    return perplexity(-totalEntropy)

initializegraphPages(G2_FilePath)#Test_FilePath)
sinkNodes   = getSinkNodes()
sourceNodes = getSourceNodes()
print 'Graph is consumed'
buildStatistics(G2_FilePath.split('\\')[len(G1_FilePath.split('\\')) - 1].replace('.txt',''))

with open(Task2_G2_Perplexity_File, 'a+') as textFile:
    convergence = 0
    round = 0
    prevPerplexity = 0
    curPerplexity = 0
    while convergence < 4:
        curPerplexity = calculatePageRank(sinkNodes)
        print 'round: %d, %s\n' % (round, str(curPerplexity))
        textFile.write('round: %d, %s\n' % (round, str(curPerplexity)))
        if abs((curPerplexity - prevPerplexity)) < 1:
            convergence += 1
        else:
            convergence = 0
        round += 1
        prevPerplexity = curPerplexity

with open(Task2_G2_Top50_File, 'a+') as textFile:
    pagesByRank = sorted(graphPages, key = lambda x: graphPages[x].rank)
    pageIndex = 0
    for page in reversed(pagesByRank):
        if(pageIndex > 50):
            break
        textFile.write('%s %f\n' % (page, graphPages[page].rank))
        pageIndex += 1
    


