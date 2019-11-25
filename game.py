import board
import mapFeatures
import random
import mcts
import minTotalAI
import minDifferenceAI
import copy
import graphics
import pygame

class game:
    features=None

    def __init__(self,players,features, inboard=None,hands=None):
        self.features=features
        self.hands={}
        self.board=None
        self.players=players
        hubs=[]
        for player in self.players:
            self.hands[player[0]]={}
            if(len(player)>2):
                hubs.append(player[2])
        if(inboard==None):
            self.board=board.grid(mapFeatures,len(players),hubs)
        else:
            self.board=inboard
        for key in self.features.cities.keys():
            values=[]
            for i in self.features.cities[key].keys():
                values.append(i)
            cities=random.sample(values,len(self.players))
            for i in range(0,len(self.players)):
                self.hands[players[i][0]][cities[i]]=self.features.cities[key][cities[i]]
        for i in range(0,len(self.players)):
            self.players[i][1]=self.players[i][1].init(copy.deepcopy(self.board),self.features,self.players[i][0],self.hands)
    
    def take_turn(self):
        move=self.players[self.board.turn][1].move(copy.deepcopy(self.board))
        self.board.make_move(move, self.board.turn)
        return self.board.check_winner(self.hands)
        
    def make_move(self, move, player):
        return self.board.make_move(move, player)

    def play_game(self):
        while(self.board.check_winner(self.hands)[0]==None):
            self.take_turn()
        return self.board.check_winner(self.hands)

wins=[0,0,0]
while(sum(wins)<100):
    minDifferenceAI.temp=0
    players=[[0,minDifferenceAI],[1,minDifferenceAI]]
    g=game(players,mapFeatures)

    gBoard=copy.deepcopy(g.board)
    hands2=copy.deepcopy(g.hands)
    winner1, score=g.play_game()

    minDifferenceAI.temp=1
    g2=game([[0,minDifferenceAI],[1,minDifferenceAI]],mapFeatures,gBoard,hands2)
    winner2, score=g2.play_game()
    if(winner1!=winner2):
        print(winner1)
        wins[winner1]+=1
    else:
        print("draw")
        wins[2]+=1
print(wins)
#print(g.play_game())
w = graphics.window(graphics.xres,graphics.yres,mapFeatures)
grid=g.board

#print(get_coords(0,19,extrema,scaling))
running = True
done = False
#print(testgrid.costs)
    # main loop
while running:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not done:
                result=g.take_turn()
                if(result[0]!=None):
                    done=True
                    print(result[0])
            if event.key == pygame.K_q:
                running = False
    w.draw(g.board, g.hands)

#print(g.graph.nodes)
#print(g.players[0][2])
#print(g.board.check_winner(g.players,g.hands))
#print(g.board.computeCosts((0,0)))
#for player in g.players:
#    print(g.board.get_moves(player[2]))
#print(g.board.make_move(0,[((0,0),(1,0))] ))
#print(g.board.check_winner(g.players,g.hands))
#print(g.board.check_winner(board.make_move(g.graph,g.players[0],(1,0))[0],g.players,g.hands))
#g.check_winner(g.graph)
#print(g.hands)
