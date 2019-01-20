def readScores(path):
    listNames = []
    with open(path, "rt") as f:
        scores = f.read()
        nameScores = scores.split('\n')
        for name in nameScores:
            listNames.append(name)
    return listNames
    
    
 
def order(path):
    listNew = []
    listNames = readScores(path)
    dictOrder = dict()
    print(listNames)
    for i in range(len(listNames)):
        nameScore = listNames[i].split()
        dictOrder[int(nameScore[1])] = nameScore[0]
    for key in sorted(dictOrder):
        listNew.append(str(key) + ": " + dictOrder[key] + '\n')
    return listNew
    
    
def updateScore(player, path):
    listNames = readScores(path)
    listNew = ''
    for i in range(len(listNames)):
        nameScore = listNames[i].split()
        if nameScore[0] == player:
            listNew += nameScore[0] + ': ' + str(int(nameScore[1])+1) + '\n'
        else:
            listNew += nameScore[0] + ': ' + nameScore[1] + '\n'
    print(listNew)
    return listNew


print(updateScore('ludi', 'test.txt'))