class MinMaxSolver:

    def __init__(self):
        self.config = []

    def set_config(self, config):
        self.config = config

    def findBestMove(self):
        pos = -1
        value = -2
        for i in range(0, 9):
            if self.config[i] == 0:
                self.config[i] = 1
                score = -self.minimax(-1)
                self.config[i] = 0
                if score > value:
                    value = score
                    pos = i
        return pos


    def minimax(self, player):
        x = self.analyzeboard()
        if x != 0:
            return x*player
        pos = -1
        value = -2
        for i in range(0, 9):
            if self.config[i] == 0:
                self.config[i] = player
                score = -self.minimax((player * -1))
                if score > value:
                    value = score
                    pos = i
                self.config[i] = 0
        if pos == -1:
            return 0
        return value


    #This function is used to draw the self.config's current state every time the user turn arrives.
    def ConstBoard(self):
        print("Current State Of self.config: \n\n");
        for i in range (0,9):
            if((i>0) and (i%3)==0):
                print("\n");
            if(self.config[i]==0):
                print("- ",end=" ");
            if (self.config[i]==1):
                print("O ",end=" ");
            if(self.config[i]==-1):
                print("X ",end=" ");
        print("\n\n");

    #This function is used to analyze a game.
    def analyzeboard(self):
        cb = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in range(0,8):
            if (self.config[cb[i][0]] != 0 and
               self.config[cb[i][0]] == self.config[cb[i][1]] and
               self.config[cb[i][0]] == self.config[cb[i][2]]):
                return self.config[cb[i][2]]
        return 0
