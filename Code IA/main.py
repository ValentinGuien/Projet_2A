
from Plateau import *
import time

##MODE JOUEUR VS IA

def main():
    """Fonction principale du script"""
    dames = Plateau()
    print("Vous jouez les blancs")
    
    
    while not(dames.get_finpartie()):
        
        d = dames.dict_mouvements()
        if len(d)==0:
            dames.set_finpartie(True)
            dames.afficher()
            print("Victoire de l'ordinateur !")
        
        else:
            cond=False
            
            while not(cond):
                dames.afficher()
                piece = input("Quelle piece voulez vous jouez ? Saisir i,j : ")
                coord = input("Ou voulez vous la jouez ? Saisir i,j : ")
                try:
                    i,j=int(piece[0]),int(piece[2])
                    nouv_i,nouv_j=int(coord[0]),int(coord[2])
                    if (i,j) not in d or (nouv_i,nouv_j) not in d[(i,j)]:
                        print("Deplacement impossible")
                        print("Liste des deplacements disponibles : ",d)
                    else:
                        dames.deplacer(i,j,nouv_i,nouv_j)
                        cond=True
                except IndexError:
                    print("Erreur, coordonnees mal saisies")
                except ValueError:
                    print("Erreur, coordonnees mal saisies")
                    
                
                
                if cond:
                    dames.afficher()
                    if len(dames.dict_mouvements())==0:
                        print("Vous avez gagne !")
                        dames.set_finpartie(True)
                    else:
                        print("L'ordinateur reflechit...")
                        t1 = time.time()
                        i,j,nouv_i,nouv_j = dames.predire(1,3,10,"noir")
                        t2 = time.time()
                        dames.deplacer(i,j,nouv_i,nouv_j)
                        print("Temps ecoule : ",t2-t1)
                        print("L'ordinateur deplace la piece ",i,",",j," a la case ",nouv_i,",",nouv_j)
        
    fichier = open("histo_partie.txt","a")
    fichier.write(str(dames.get_historique())+"\n")
    fichier.close()
    
if __name__=="__main__":
    main()
    
## MODE IA VS IA

# def main():
    """Fonction principale du script"""
    dames = Plateau()
    print("IA VS IA")
    
    
    while not(dames.get_finpartie()):
        if len(dames.dict_mouvements())==0:
            dames.set_finpartie(True)
            print("Victoire des noirs !")
        else:
            i,j,nouv_i,nouv_j = dames.predire(1,3,"blanc")
            dames.deplacer(i,j,nouv_i,nouv_j)
            if len(dames.dict_mouvements())==0:
                dames.set_finpartie(True)
                print("Victoire des blancs !")
            else:
                i,j,nouv_i,nouv_j = dames.predire(1,-1,"noir")
                dames.deplacer(i,j,nouv_i,nouv_j)
                #print("Noir deplace la piece ",i,",",j," a la case ",nouv_i,",",nouv_j)
        if dames.match_nul():
            print("Match nul")
            dames.set_finpartie(True)
        
    fichier = open("histo_partie.txt","a")
    fichier.write(str(dames.get_historique())+"\n")
    fichier.close()
    
# if __name__=="__main__":
#     main()

##
x = [['pion', 'blanc', 2, 4, 3, 5, None, None], ['pion', 'noir', 5, 1, 4, 2, None, None], ['pion', 'blanc', 1, 5, 2, 4, None, None], ['pion', 'noir', 5, 3, 4, 4, None, None], ['pion', 'blanc', 3, 5, 5, 3, 'pion', 'noir'], ['pion', 'noir', 6, 2, 4, 4, 'pion', 'blanc'], ['pion', 'blanc', 0, 6, 1, 5, None, None], ['pion', 'noir', 4, 4, 3, 5, None, None], ['pion', 'blanc', 2, 6, 4, 4, 'pion', 'noir'], ['pion', 'noir', 5, 5, 3, 3, 'pion', 'blanc'], ['pion', 'blanc', 2, 2, 4, 4, 'pion', 'noir'], ['pion', 'noir', 4, 2, 3, 1, None, None], ['pion', 'blanc', 2, 0, 4, 2, 'pion', 'noir'], ['pion', 'noir', 6, 4, 5, 5, None, None], ['pion', 'blanc', 1, 1, 2, 0, None, None], ['pion', 'noir', 5, 5, 3, 3, 'pion', 'blanc'], ['pion', 'blanc', 0, 2, 1, 1, None, None], ['pion', 'noir', 5, 7, 4, 6, None, None], ['pion', 'blanc', 1, 3, 2, 2, None, None], ['pion', 'noir', 6, 6, 5, 5, None, None], ['pion', 'blanc', 2, 2, 4, 4, 'pion', 'noir'], ['pion', 'noir', 5, 5, 3, 3, 'pion', 'blanc'], ['pion', 'blanc', 1, 7, 2, 6, None, None], ['pion', 'noir', 6, 0, 5, 1, None, None], ['pion', 'blanc', 4, 2, 6, 0, 'pion', 'noir'], ['pion', 'noir', 4, 6, 3, 5, None, None], ['pion', 'blanc', 2, 4, 4, 2, 'pion', 'noir'], ['pion', 'noir', 3, 5, 1, 7, 'pion', 'blanc'], ['pion', 'blanc', 1, 5, 2, 4, None, None], ['pion', 'noir', 1, 7, 0, 6, None, None], ['pion', 'blanc', 4, 2, 5, 3, None, None], ['pion', 'noir', 7, 3, 6, 2, None, None], ['pion', 'blanc', 2, 4, 3, 5, None, None], ['pion', 'noir', 6, 2, 4, 4, 'pion', 'blanc'], ['pion', 'blanc', 3, 5, 5, 3, 'pion', 'noir'], ['dame', 'noir', 0, 6, 1, 7, None, None], ['pion', 'blanc', 1, 1, 2, 2, None, None], ['dame', 'noir', 1, 7, 2, 6, None, None], ['pion', 'blanc', 2, 0, 3, 1, None, None], ['dame', 'noir', 2, 6, 1, 7, None, None], ['pion', 'blanc', 3, 1, 4, 0, None, None], ['dame', 'noir', 1, 7, 2, 6, None, None]]
dames = Plateau()