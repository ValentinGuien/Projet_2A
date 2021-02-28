class Piece:
    
    def __init__(self, coul="vide", etat="vide"):
        """Creation d'une piece
        - coul : couleur de la piece, vide ou blanc ou noir
        - etat : etat de la piece, vide, pion ou dame"""
        self.coul=coul
        self.etat=etat
    
    def to_str(self):
        """affichage de la piece en 2 lettres : 
        etat (p, d) + couleur (b, n) ou .. si case vide """
        if self.coul=="vide":
            str='..'
        else:
            str= self.etat[0] + self.coul[0]
        return str

    def est_vide(self):
        """Booleen disant si la case est vide"""
        return self.coul=="vide" and self.etat=="vide"

    def get_coul(self):
        """Returne la couleur de la piece"""
        return self.coul
    
    def set_coul(self,coul):
        """Modifie la couleur de la piece"""
        self.coul = coul

    def est_ennemie(self,coul):
        """Returne True si la piece est ennemie de la couleur coul"""
        return not(self.est_vide()) and self.coul!=coul
        
        
    def liberer_case(self):
        """Liberation de la case"""
        self.set_coul("vide")
        self.set_etat("vide")
    
    def get_etat(self):
        """Returne l'etat de la piece"""
        return self.etat
    
    def set_etat(self,etat):
        """Modifie l'etat de la piece"""
        self.etat = etat
        
    def promotion(self):
        """Promotion d'une piece : elle passe de pion a dame"""
        self.set_etat("dame")