import csv
import random
import copy


class ConfusionMatrix:
    def __init__(self, combination):
        self.combination = combination
        self.TP = 0
        self.FP = 0
        self.FN = 0
        self.TN = 0
        self.accuracy = 0
        self.precision = 0
        self.recall = 0

    def __str__(self):
        result = ("="*(len(self.combination)*5)+"=========\n")
        result += ("--- " + str(self.combination)+"  ---\n")
        result += ("||| TN = " + str(self.TN) +
                   "\t | \tFN = " + str(self.FN) + " |||\n")
        result += ("-"*(len(self.combination)*5)+"---------\n")
        result += ("||| FP = " + str(self.FP) +
                   "\t | \tTP = " + str(self.TP) + " |||\n")
        result += ("="*(len(self.combination)*5)+"=========\n")
        return result

    def stringToFile(self):
        tempList = copy.deepcopy(self.combination)
        tempList.append(self.TP)
        tempList.append(self.FP)
        tempList.append(self.FN)
        tempList.append(self.TN)
        return tempList

    def compAll(self):
        if (self.TP+self.TN+self.FP+self.FN) != 0:
            self.accuracy = (self.TP+self.TN)/(self.TP+self.TN+self.FP+self.FN)
        if (self.TP+self.FP) != 0:
            self.precision = (self.TP/(self.TP+self.FP))
        if (self.TP+self.FN) != 0:
            self.recall = (self.TP/(self.TP+self.FN))

    def getReady(self):
        self.compAll()
        return self.stringToFile()


class Rows:
    def __init__(self, allRows, allPossibilities, fileName):

        self.fileName = fileName

        self.highestAccuracyCM = ConfusionMatrix(list())
        self.highestPrecisionCM = ConfusionMatrix(list())
        self.highestRecallCM = ConfusionMatrix(list())
        self.highestTP = ConfusionMatrix(list())

        self.allRows = allRows
        self.allPossibilities = allPossibilities
        self.confusionMatrix = list()

        self.computeCMValues()
        # self.computeCMEvaluator()
        # self.findHighestEvaluator()

    def computeScore(self, row, combination):
        resultList = list()
        score = 0
        for j in range(len(combination)):
            value = float(combination[j])
            resultList.append(value)
            score += (value*row.rowInfo[j+2])
        return (round(score, 2), resultList)

    def computeCMValues(self):
        with open(self.fileName, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            for curComb in self.allPossibilities:
                score, floatCompList, tempCM = 0, list(), ConfusionMatrix(list())
                for row in self.allRows:
                    score, floatCompList = self.computeScore(row, curComb)
                    tempCM = ConfusionMatrix(floatCompList)
                    if score/5 < 0.6:
                        if (row.realScore == 0 or row.realScore == 1):  # TN
                            tempCM.TN += 1
                        else:  # FN
                            tempCM.FN += 1
                    else:
                        if (row.realScore == 0 or row.realScore == 1):  # FP
                            tempCM.FP += 1
                        else:  # TP
                            tempCM.TP += 1
                writer.writerow(tempCM.getReady())
                self.findHighestEvaluator(tempCM)
                self.confusionMatrix.append(tempCM)

    # def computeCMEvaluator(self):
    #     for cm in self.confusionMatrix:
    #         cm.compAll()

    def findHighestEvaluator(self, cm):
        # for cm in self.confusionMatrix:
        if cm.accuracy > self.highestAccuracyCM.accuracy:
            self.highestAccuracyCM = cm
        if cm.precision > self.highestPrecisionCM.precision:
            self.highestPrecisionCM = cm
        if cm.recall > self.highestRecallCM.recall:
            self.highestRecallCM = cm

        if cm.TP > self.highestTP.TP:
            self.highestTP = cm


class Row:
    def __init__(self, rowInfo):
        self.rowInfo = rowInfo
        self.id = rowInfo[0]
        self.realScore = rowInfo[1]


def getPossibilities(fileName):
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            yield row


def createExample(numFactor):
    result = list()
    for _ in range(150):
        tempResult = list()
        for _ in range(numFactor+2):
            tempResult.append(random.randint(0, 5))
        result.append(tempResult)
    return result


def main():
    allPossibilities = getPossibilities('six.csv')
    example = createExample(6)

    rows = Rows([Row(x) for x in example], allPossibilities, 'delete.csv')

    print(rows.highestAccuracyCM)
    print(rows.highestPrecisionCM)
    print(rows.highestRecallCM)


main()
