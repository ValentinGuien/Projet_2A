import random
from Piece import *

class Plateau:
    
    
    
    def __init__(self):
        """Creation d'un plateau de jeu 8x8"""
        
        self.cases=[[Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece()],[Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion")],[Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece(),Piece("blanc","pion"),Piece()],[Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece()],[Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece(),Piece()],[Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion")],[Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece()],[Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion"),Piece(),Piece("noir","pion")]]
    
        #Tour du joueur, les blancs commencent
        self.tour = "blanc"
        
        #Historique des coups joues
        self.historique = []
        
        #Valeur pour designer "l'infini"
        self.infinity = 1000000
        
        #Prochain coup que l'ordinateur doit jouer
        self.nextmove = ()
        
        #Indique si la partie est terminee ou non
        self.finpartie = False
        
    
    def changer_tour(self):
        """Changer de tour"""
        if self.tour=="blanc":
            self.tour="noir"
        else:
            self.tour="blanc"
    
    def afficher(self):
        """Visualisation du plateau de jeu"""
        ligne=""
        for i in range(7,-1,-1):
            for j in range(8):
                ligne+=self.cases[i][j].to_str()+" "
                
            ligne+="\n"
        print(ligne)
        
    def deplacer(self,i,j,nouv_i,nouv_j):
        """deplacer la piece en case [i,j] a la case [nouv_i,nouv_j]"""
        coul_piece = self.cases[i][j].get_coul()
        etat_piece = self.cases[i][j].get_etat()
        self.cases[nouv_i][nouv_j].set_coul(coul_piece)
        self.cases[nouv_i][nouv_j].set_etat(etat_piece)
        self.cases[i][j].liberer_case()

        coul_piece_prise = None
        etat_piece_prise = None
        
        #Promotion
        if (coul_piece =="blanc" and nouv_i==7) or (coul_piece=="noir" and nouv_i==0):
            self.cases[nouv_i][nouv_j].promotion()
        
        #Prise d'une piece
        if abs(nouv_i-i)==2:
            """une piece a ete attrapee"""
            coul_piece_prise = self.cases[(nouv_i+i)//2][(nouv_j+j)//2].get_coul()
            etat_piece_prise = self.cases[(nouv_i+i)//2][(nouv_j+j)//2].get_etat()
            self.cases[(nouv_i+i)//2][(nouv_j+j)//2].liberer_case()
        
        #On ajoute a l'historique les changements du plateau
        self.historique.append([etat_piece,coul_piece,i,j,nouv_i,nouv_j,etat_piece_prise,coul_piece_prise])
        
        self.changer_tour()
        
    def annuler(self):
        """annuler un déplacement"""
        
        #Recuperation du dernier coup joue
        etat_piece,coul_piece,ancien_i,ancien_j,i,j,etat_piece_prise,coul_piece_prise=self.historique[-1]
        
        #Rembobinage
        self.cases[i][j].liberer_case()
        self.cases[ancien_i][ancien_j].set_coul(coul_piece)
        self.cases[ancien_i][ancien_j].set_etat(etat_piece)
        
        if abs(ancien_i-i)==2:
            self.cases[(ancien_i+i)//2][(ancien_j+j)//2].set_coul(coul_piece_prise)
            self.cases[(ancien_i+i)//2][(ancien_j+j)//2].set_etat(etat_piece_prise)
            
        self.changer_tour()
        
        del self.historique[-1]
    
    
            
    def mouvements_simple_piece(self,i,j):
        """donne les mouvements simples possibles pour une piece situee en [i,j]"""
        
        simples = []
        etat_piece = self.cases[i][j].get_etat()
        coul_piece = self.cases[i][j].get_coul()
        
        if coul_piece=="blanc":
            #deplacer en avant
            if i!=7:
                #deplacer a gauche
                if j!=0:
                    if self.cases[i+1][j-1].est_vide():
                        simples.append((i+1,j-1))
                #deplacer a droite
                if j!=7:
                    if self.cases[i+1][j+1].est_vide():
                        simples.append((i+1,j+1))
            #deplacer en arriere (dames seulement)         
            if i!=0 and etat_piece=="dame":
                #deplacer a gauche
                if j!=0:
                    if self.cases[i-1][j-1].est_vide():
                        simples.append((i-1,j-1))
                #deplacer a droite
                if j!=7:
                    if self.cases[i-1][j+1].est_vide():
                        simples.append((i-1,j+1))
                        
                        
        elif coul_piece=="noir":
            #deplacer en avant
            if i!=0:
                #deplacer a gauche
                if j!=0:
                    if self.cases[i-1][j-1].est_vide():
                        simples.append((i-1,j-1))
                #deplacer a droite
                if j!=7:
                    if self.cases[i-1][j+1].est_vide():
                        simples.append((i-1,j+1))
            #deplacer en arriere (dames seulement)
            if i!=7 and etat_piece=="dame":
                #deplacer a gauche
                if j!=0:
                    if self.cases[i+1][j-1].est_vide():
                        simples.append((i+1,j-1))
                #deplacer a droite
                if j!=7:
                    if self.cases[i+1][j+1].est_vide():
                        simples.append((i+1,j+1))
        return simples
    
    def mouvements_prise_piece(self,i,j):
    
        etat_piece = self.cases[i][j].get_etat()
        coul_piece = self.cases[i][j].get_coul()
        
        mouvements=[]
        
        
        if coul_piece=="blanc":
            #prise en avant
            if i<6:
                #prise a gauche
                if j>1 and self.cases[i+1][j-1].est_ennemie(coul_piece) and self.cases[i+2][j-2].est_vide():
                    mouvements.append((i+2,j-2))
                #prise a droite
                if j<6 and self.cases[i+1][j+1].est_ennemie(coul_piece) and self.cases[i+2][j+2].est_vide():
                    mouvements.append((i+2,j+2))
            #prise en arriere (dames seulement)
            if i>1 and etat_piece=="dame":
                #prise a gauche
                if j>1 and self.cases[i-1][j-1].est_ennemie(coul_piece) and self.cases[i-2][j-2].est_vide():
                    mouvements.append((i-2,j-2))
                #prise a droite
                if j<6 and self.cases[i-1][j+1].est_ennemie(coul_piece) and self.cases[i-2][j+2].est_vide():
                    mouvements.append((i-2,j+2))
                    
                    
        elif coul_piece=="noir":
            #prise en avant
            if i>1:
                #prise a gauche
                if j>1 and self.cases[i-1][j-1].est_ennemie(coul_piece) and self.cases[i-2][j-2].est_vide():
                    mouvements.append((i-2,j-2))
                #prise a droite
                if j<6 and self.cases[i-1][j+1].est_ennemie(coul_piece) and self.cases[i-2][j+2].est_vide():
                    mouvements.append((i-2,j+2))
            #prise en arriere (dames seulement)
            if i<6 and etat_piece=="dame":
                #prise a gauche
                if j>1 and self.cases[i+1][j-1].est_ennemie(coul_piece) and self.cases[i+2][j-2].est_vide():
                    mouvements.append((i+2,j-2))
                #prise a droite
                if j<6 and self.cases[i+1][j+1].est_ennemie(coul_piece) and self.cases[i+2][j+2].est_vide():
                    mouvements.append((i+2,j+2))
                    
        return mouvements
        
        
    def dict_mouvements(self):
        """Donne tous les mouvements possibles sous la forme d'un dictionnaire ou l'index (i,j) donne la liste des deplacements possibles de la piece situee en (i,j)"""
        d=dict()
        #On regarde d'abord si une prise est possible
        for i in range(8):
            for j in range(8):
                if self.cases[i][j].get_coul()==self.tour:
                    l = self.mouvements_prise_piece(i,j)
                    if len(l)>0:
                        d[(i,j)]=l
            
        #Pas de prise possible, on regarde les mouvements simples
        if len(d)==0:
            for i in range(8):
                for j in range(8):
                    if self.cases[i][j].get_coul()==self.tour:
                        l = self.mouvements_simple_piece(i,j)
                        if len(l)>0:
                            d[(i,j)]=l
        return d
    
    def get_historique(self):
        """Returne l'historique de la partie"""
        return self.historique
        
    def jouer_aleatoirement(self):
        """Le joueur qui doit jouer joue aleatoirement"""
        d = self.dict_mouvements()
        if len(d)==0:
            print("Fin de la partie !")
        else:
            i1,j1 = random.choice(list(d.keys()))
            i2,j2 = random.choice(d[i1,j1])
            print("deplacement de la piece ",i1,",",j1," a la position ",i2,",",j2)
            self.deplacer(i1,j1,i2,j2)
            
    def rejouer_partie(self, histo):
        for move in histo:
            self.deplacer(move[2],move[3],move[4],move[5])
    
        
            
    def evaluer(self,score_pion,score_dame,coul):
        score_blanc=0
        score_noir=0
        for i in range(8):
            for j in range(8):
                piece = self.cases[i][j]
                if piece.get_coul()=="blanc":
                    if piece.get_etat()=="dame":
                        score_blanc+=score_dame
                    else:
                        score_blanc+=score_pion
                elif piece.get_coul()=="noir":
                    if piece.get_etat()=="dame":
                        score_noir+=score_dame
                    else:
                        score_noir+=score_pion
                   
        if coul=="blanc":
            return score_blanc-score_noir
        else:
            return score_noir-score_blanc
    
    def alphabeta(self,alpha,beta,score_pion,score_dame,coul,prof):
        
        if prof==0:
            return self.evaluer(score_pion,score_dame,coul)
        else:
            d = self.dict_mouvements()
            if len(d)==0:
                return self.evaluer(score_pion,score_dame,coul)
            else:
                piece_a_jouer=random.choice(list(d.keys()))
                coord_a_placer=random.choice(d[piece_a_jouer])
                if self.tour!=coul: #noeud de type min = à l'ennemi de jouer
                    score = self.infinity
                    for piece in d:
                        i,j = piece
                        for coord in d[piece]:
                            nouv_i,nouv_j = coord
                            self.deplacer(i,j,nouv_i,nouv_j)
                            v=self.alphabeta(alpha,beta,score_pion,score_dame,coul,prof-1)
                            if v<score:
                                score = v
                                piece_a_jouer=piece
                                coord_a_placer=coord
                                
                            self.annuler()
                            if alpha>=score:
                                return score
                            beta = min(beta,score)
                else: #noeud de type max = au joueur de joueur
                    score = -self.infinity
                    for piece in d:
                        i,j = piece
                        for coord in d[piece]:
                            nouv_i,nouv_j = coord
                            self.deplacer(i,j,nouv_i,nouv_j)
                            v=self.alphabeta(alpha,beta,score_pion,score_dame,coul, prof-1)
                            if v>score:
                                score = v
                                piece_a_jouer=piece
                                coord_a_placer=coord
                            
                            self.annuler()
                            if score>=beta:
                                return score
                            alpha = max(beta,score)
                self.nextmove=piece_a_jouer+coord_a_placer
                return score
    
    def predire(self,score_pion,score_dame,prof,coul):
        self.alphabeta(-self.infinity,self.infinity,score_pion,score_dame,coul,prof)
        return self.nextmove
        
    def get_finpartie(self):
        return self.finpartie
    
    def set_finpartie(self,bool):
        self.finpartie = bool
        
    def match_nul(self):
        """Regarde si un match est "nul" :
        Les 4 memes derniers coups ont ete effectues 3 fois de suite"""
        return len(self.get_historique())==300