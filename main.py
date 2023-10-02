import copy
import time

initialBoard = [["Grey","DarkPink","LightPurple","LightPink"],
                ["LightPink","Orange","Blue","Turquoise"],
                ["Grey","DarkGreen","LightGreen","Orange"],
                ["DarkPurple","DarkGreen","Red","Turquoise"],
                ["Grey","DarkPurple","Grey","DarkPurple"],
                ["LightPurple","DarkPurple","Orange","DarkPink"],
                ["Blue","LightPurple","LightGreen","Red"],
                ["Turquoise","DarkGreen","DarkPink","Yellow"],
                ["Blue","DarkGreen","Yellow","Turquoise"],
                ["LightGreen","Red","LightGreen","Blue"],
                ["LightPink","Red","Orange","LightPink"],
                ["Yellow","DarkPink","Yellow","LightPurple"],
                [],
                []]

class tube():
    def __init__(self, beads) -> None:
        if len(beads) > 4:
            print("too many beads in"+ beads)
            exit()

        self.tube = beads
        self.numberOfBeads = len(beads)

    def pop(self) -> str:
        if len(self.tube) <= 0:
            print("error popping from tube, current highest = 0")
            exit()

        self.numberOfBeads -= 1
        return self.tube.pop()
    
    def add(self, item) -> None:
        if len(self.tube)  >= 4:
            print("error adding to tube, more than 4 beads")
            exit()

        self.numberOfBeads += 1
        self.tube.append(item)
        return 

    def compareColour(self, index, bead) -> bool:
        if self.tube[index] == bead:
            return True
        return False
    
    def checkIfValidAdd(self, item: str, numberOfBead) -> bool:
        if (self.numberOfBeads + numberOfBead) > 4:
            return False
        if self.numberOfBeads == 0:
            return True
        return self.compareColour((self.numberOfBeads-1),item)
    
    def peek(self) -> str:
        if self.numberOfBeads == 0:
            return None, 0
        count = 1
        current = self.tube[self.numberOfBeads-1]
        for i in range(self.numberOfBeads-1):
            if self.compareColour((self.numberOfBeads-(1+count)),current):
                count += 1
                continue

            break
        return self.tube[self.numberOfBeads-1], count

    def isTubeSolved(self) -> bool:
        checker, count = self.peek()
        if count == 4 or count == 0:
            return True
        return False
    
    def compareTube(self, tube) -> bool:
        if len(self.tube) != len(tube.tube):
            return False
        for index in range(len(self.tube)):
            if not self.compareColour(index, tube.tube[index]):
                return False
        return True

    def __str__(self) -> str:
        string = ""
        for index, item in enumerate(self.tube):
            string += "Bead at position {} is of colour {}\n".format(index, str(item))
        return string

class GameTree():
    def __init__(self, tubes, parent) -> None:
        #size is number of tubes
        self.board = tubes
        self.parent = parent
        self.children = []

    def addChild(self,index, secondIndex, count):
        tubes = []
        for item in self.board:
            temp = copy.deepcopy(item.tube)
            temp2 = tube(temp)
            tubes.append(temp2)
        child = GameTree(tubes, self)
        child.makeMove(index, secondIndex, count)
        self.children.append(child)

    def findAllMoves(self):

        if self.isBoardSolved():
            file = open("log.txt", "w")
            file.write("------------  Reset  ------------\n\n\n\n")
            file.close()

            with open('log.txt', 'a') as file:
                self.printSolution(file)
            exit()

        for index, tube in enumerate(self.board):
            currentBead, count = tube.peek()
            if count == 4:
                continue
            if currentBead == None:
                continue
            for secondIndex, secondTube in enumerate(self.board):
                if tube == secondTube:
                    continue
                if tube.numberOfBeads == count and not secondTube.tube: 
                    continue
                if secondTube.checkIfValidAdd(currentBead, count):
                    self.addChild(index, secondIndex, count)
        
        return self.children

    def makeMove(self, tubeToPop, tubeToAdd, count):
        for i in range(count):
            tempBead = self.board[tubeToPop].pop()
            self.board[tubeToAdd].add(tempBead)
        return 
    
    def isBoardSolved(self) -> bool:
        for item in self.board:
            if item.isTubeSolved():
                continue
            else: 
                return False
        return True
    
    def printSolution(self,file):
        stringSep = "\n-----------------------------------------------------------------------\n"
        file.write(str(self))
        file.write(stringSep)
        if self.parent == None:
            exit()
        file.write(str(self.compareBoard(self.parent)))
        file.write(stringSep)
        self.parent.printSolution(file)

    def compareBoard(self, board) -> str:
        string = ""
        for index, tube in enumerate(self.board):
            if tube.compareTube(board.board[index]):
                continue
            else: 
                string += "tube at position: {}, went from:\n\n{}to:\n\n{}\n\n".format(index, str(board.board[index]), str(tube))
        return string + "\n"

    def __str__(self) -> str:
        string = ""
        for index, item in enumerate(self.board):
            string += "tube at position {} is compromised of: \n\n{}\n\n".format(index, str(item))
        return string + "\n"

def main():
    tempBoard = []
    for initialTube in initialBoard:
        tempTube = tube(initialTube)
        tempBoard.append(tempTube)
    Board = GameTree(tempBoard, None)

    queue = []
    queue.append(Board.findAllMoves())
    count = 0
    test = Board
    while queue:
        count += 1
        current = queue.pop()
        if count > 5000:
            test = current[0]
            break
        print("Number of children in current loop = {}, length of queue = {}, recursion depth = {}".format(len(current), len(queue), count))
        for board in current:
            moves = board.findAllMoves()
            if moves:
                queue.append(moves)
            continue

    file = open("log.txt", "w")
    file.write("------------  Reset  ------------\n\n\n\n")
    file.close()

    with open('log.txt', 'a') as file:
        test.printSolution(file)

    

if __name__ == "__main__":
    main()