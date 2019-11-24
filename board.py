import mapFeatures
import queue

class grid:
    turn=0
    board=[]
    costs=[]
    hubs=[]
    def __init__(self, mountains, oceans,numPlayers,hubs=[]):
        if(len(hubs)==0):
            for i in range(0,numPlayers):
                self.hubs.append(None)
        else:
            self.hubs=hubs
        for i in range(0,13):
            self.board.append([])
            for j in range(0,20):
                #print(i,j)
                self.board[i].append([[0,1],[1,1]])

        #print(self.board)
        for mountain in mountains:
            #print(mountain)
            self.set(mountain[0],mountain[1],2)
        for ocean in oceans:
            #print(ocean)
            for neighbor in self.get_neighbors(ocean):
                #print(neighbor)
                self.set(ocean,neighbor[0],3)
        for i in range(0,13):
            self.costs.append([])
            for j in range(0,20):
                self.costs[i].append(self.computeCosts((i,j)))


    def cost(self,point1,point2):
        offset=sum((point1[0]-point2[0],point1[1]-point2[1]))
        if(offset<0):
            change=(point2[0]-point1[0],point2[1]-point1[1])
            return self.board[point1[0]][point1[1]][change[0]][change[1]]
        elif(offset>0):
            change=(point1[0]-point2[0],point1[1]-point2[1])
            return self.board[point2[0]][point2[1]][change[0]][change[1]]

    def set(self,point1,point2,cost):
        offset=sum((point1[0]-point2[0],point1[1]-point2[1]))
        if(offset<0):
            change=(point2[0]-point1[0],point2[1]-point1[1])
            self.board[point1[0]][point1[1]][change[0]][change[1]]=cost
        elif(offset>0):
            change=(point1[0]-point2[0],point1[1]-point2[1])
            self.board[point2[0]][point2[1]][change[0]][change[1]]=cost

    def size(self):
        return (len(self.board),len(self.board[0]))
    def get_moves(self,hub):
        moves=[]
        if(hub==None):
            for i in range(0,self.size()[0]):
                for j in range(0,self.size()[1]):
                    if(len(self.get_neighbors((i,j)))!=0):
                        moves.append((i,j))
            return moves
        visited=[{},{},{}]
        visited[0][hub]=None
        toVisit=[]
        toVisit.extend(self.get_neighbors(hub,0,0))
        while(len(toVisit)!=0):
            check=toVisit.pop(0)
            if(check[0] not in visited[0]):
                visited[0][check[0]]=None
                toVisit.extend(self.get_neighbors(check[0],0,0))
        for point in visited[0].keys():
            for neighbor in self.get_neighbors(point,1,1):
                if(neighbor[0] not in visited[0] and neighbor[0] not in visited[1]):
                    visited[1][neighbor[0]]=point
        for point in visited[0].keys():
            for neighbor in self.get_neighbors(point,2,2):
                if(neighbor[0] not in visited[0] and neighbor[0] not in visited[1] and neighbor[0] not in visited[2]):
                    visited[2][neighbor[0]]=point
        for point in visited[1].keys():
            for neighbor in self.get_neighbors(point,1,1):
                if(neighbor[0] not in visited[0] and neighbor[0] not in visited[1] and neighbor[0] not in visited[2]):
                    visited[2][neighbor[0]]=point
        moves=[]
        for point in visited[2].keys():
            if(visited[2][point] in visited[0]):
                moves.append([(point,visited[2][point])])
            else:
                moves.append([(point,visited[2][point]),(visited[1][visited[2][point]],point)])
        temp=visited[1].keys()
        for i in range(1,len(temp)):
            for j in range(0,i-1):
                moves.append([(temp[i],visited[1][temp[i]]),(visited[1][temp[j]],temp[j])])
        return moves

    def get_neighbors(self,point, mincost=1,maxcost=2):
        neighbors=[]
        if(point[0]+1<len(self.board)):
            if(point[1]+1<len(self.board[0])):
                cost = self.board[point[0]][point[1]][1][1]
                if(cost>=mincost and cost<=maxcost):
                    neighbors.append(((point[0]+1,point[1]+1),cost))
            cost = self.board[point[0]][point[1]][1][0]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0]+1,point[1]),cost))
        if(point[1]+1<len(self.board[0])):
            cost = self.board[point[0]][point[1]][0][1]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0],point[1]+1),cost))
        if(point[0]>0):
            if(point[1]>0):
                cost = self.board[point[0]-1][point[1]-1][1][1]
                if(cost>=mincost and cost<=maxcost):
                    neighbors.append(((point[0]-1,point[1]-1),cost))
            cost = self.board[point[0]-1][point[1]][1][0]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0]-1,point[1]),cost))
        if(point[1]>0):
            cost = self.board[point[0]][point[1]-1][0][1]
            if(cost>=mincost and cost<=maxcost):
                neighbors.append(((point[0],point[1]-1),cost))
        return neighbors
        
    def computeCosts(self,point):
        out=[]
        for i in range(0,self.size()[0]):
            temp=[]
            for j in range(0,self.size()[1]):
                temp.append(2*self.size()[0]*self.size()[1])
            out.append(temp)
        toCheck=queue.PriorityQueue()
        out[point[0]][point[1]]=0
        toCheck.put((0,point))
        while(not toCheck.empty()):
            value,test=toCheck.get()
            #print(value,test)
            for neighbor in self.get_neighbors(test,0,2):
                if(out[test[0]][test[1]]+neighbor[1]<out[neighbor[0][0]][neighbor[0][1]]):
                    #print(out[test[0]][test[1]]+neighbor[1],out[neighbor[0][0]][neighbor[0][1]])
                    out[neighbor[0][0]][neighbor[0][1]]=out[test[0]][test[1]]+neighbor[1]
                    toCheck.put((out[neighbor[0][0]][neighbor[0][1]],neighbor[0]))
            #print()
        return out

    def make_move(self,playerNum,move):
        #print(move)
        if(self.turn!=playerNum):
            return False
        if(self.hubs[playerNum]==None):
            self.hubs[playerNum]=move
        else:
            for track in move:
                print(track)
                self.set(track[0],track[1],0)
        self.next_turn()
        return True

    def unmake_move(self,root,playerNum,move):
        for track in move:
            print(track)
            self.set(track[0],track[1],root.cost(track[0],track[1]))
            self.turn=self.turn-1
            self.turn=self.turn%len(self.hubs)
        return True

    def check_winner(self,players,hands):
        totals=[]
        for i in range(0,len(self.hubs)):
            if(self.hubs[i]==None):
                totals.append(None)
                continue
            totals.append(0)
            tempcosts=self.computeCosts(self.hubs[i])
            #print(tempcosts)
            for city in hands[players[i][0]].values():
                totals[i]+=tempcosts[city[0]][city[1]]
        for i in range(0,len(totals)):
            if(totals[i]==0):
                return i,totals
        return False,totals

    def next_turn(self):
        self.turn+=1
        self.turn=self.turn%len(self.hubs)

    def get_turn(self):
        return 2*self.turn-1

