from abc import ABC, abstractmethod

"""Tipo {Entity}.

   Il file contiene tutte classi di tipo {Entity}.

   Astraggono il concetto di pezzo della scacchiera e la logica
   generele di movimento, non situazionale. 
"""
class Pezzo(ABC):
    """Classe astratta che rappresenta un pezzo degli scacchi.

    Args :
        nome(str): il nome del pezzo (es, "pedone", "cavallo", ...)
        colore (str): Il colore del pezzo ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte la pedina.
        movedOnce (bool): Indica se il pezzo si è già mosso almeno una volta.

    Metodi astratti:
        logicaMovimento(mossa: str) -> bool:
            Determina se una mossa è valida secondo le regole del pezzo specifico.
    """
 
    def __init__(self, nome:str,colore:str, posizioneInizialeScacchiera :str):
            self.nome = nome
            self.colore = colore.lower()
            self.posizioneInizialeScacchiera = posizioneInizialeScacchiera
            self.movedOnce=False

    def __str__(self)->str:
        """Restituisce una rappresentazione testuale del pezzo."""
        return f"{self.nome} {self.colore} in {self.posizioneInizialeScacchiera}"
    
    def __repr__(self)->str:
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return self.__str__()
    
    def getNome(self)->str:
        """Restituisce il nome del pezzo."""
        return self.nome
    
    def getColore(self)->str:
        """Restituisce il colore del pezzo."""
        return self.colore
    
    def getPosizioneInizialeScacchiera(self)->str:
        """Restituisce la posizione iniziale del pezzo sulla scacchiera."""
        return self.posizioneInizialeScacchiera
    
    def getMovedOnce(self)->bool:
        """Restituisce True se il pezzo si è mosso almeno una volta,False altrimenti."""
        return self.movedOnce
    
    def setMovedOnce(self, movedOnce:bool)->None:
        """Imposta lo stato di mosso almeno una volta.

        Args :
            movedOnce (bool):se True, il pezzo si è mosso almeno una volta, sennò False.
        """
        self.movedOnce = movedOnce

    def calcolaDifferenze(self,mossa:str)->tuple:
        """Funzione che calcola differenza di righe e colonne.

        Args :
            mossa (str): stringa contenente la mossa.

        Returns :
            tuple: restituisce una tupla (differenzaColonne,differenzaRiga).
        """
        mossadiPartenza,mossadiArrivo=mossa.split()
        differenzaColonne = abs(ord(mossadiArrivo[0])- ord(mossadiPartenza[0]))
        differenzaRighe = abs(int(mossadiArrivo[1])-int(mossadiPartenza[1]))
        return differenzaColonne,differenzaRighe

    @abstractmethod
    def logicaMovimento(self, mossa:str)->bool:
        """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
        Args :
            mossa (str): La mossa da verificare, rappresentata come stringa.

        Returns :
            bool: True se la mossa è valida, False altrimenti.
        """
       
    pass


class Pedone(Pezzo):
    """Classe che rappresenta il pedone e la sua logica di movimento.

    Args :
        colore (str): Il colore del pedone ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte il pedone.
    """

    @classmethod
    def listaPedoniIniziali(cls)->list:
        """Prepara una lista di pedoni sia neri che bianchi, nelle posizioni iniziali.

        Returns :
            list:Una lista di oggetti Pedone con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        listaAllPedoni=[]
        for i in range(16):
            if i < 8:
                posizioneBianchi=str(chr(97+i))+"2"
                listaAllPedoni.append(Pedone("bianco", posizioneBianchi))

            else:
                posizioneNeri=str(chr(97+(i-8)))+"7"
                listaAllPedoni.append(Pedone("nero", posizioneNeri))

        return listaAllPedoni

    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Pedone", colore,posizioneInizialeScacchiera)

    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str,posizioneAttuale:str)->bool:
        """Controlla se la mossa del pedone è valida Sfruttando la differenza tra righe.

        Args :
            mossa (str): La mossa da verificare, rappresentata come stringa.
            posizioneAttuale (str): La posizione attuale del pedone sulla scacchiera.
                                    Verrà usata per validare uno spostamento di 2 case.

        Returns :
            bool: True se la mossa è valida, False altrimenti.
        """
        mossadiPartenza, mossaDiArrivo = mossa.split(" ")
        differenzaRighe = (int(mossaDiArrivo[1]) - int(mossadiPartenza[1]))
        differenzaColonne = (ord(mossaDiArrivo[0]) - ord(mossadiPartenza[0]))

        #CONTROLLO VERTICALE 
        if mossadiPartenza[0] == mossaDiArrivo[0]:
            return(
                (self.colore == "bianco" and differenzaRighe in [1, 2] and
                 posizioneAttuale == self.posizioneInizialeScacchiera) or

                (self.colore == "bianco" and differenzaRighe == 1) or

                (self.colore == "nero" and differenzaRighe in [-1, -2] and 
                 posizioneAttuale == self.posizioneInizialeScacchiera) or

                (self.colore == "nero" and differenzaRighe == -1)
            )
        
        #CONTROLLO DIAGONALE
        return (
        differenzaColonne in (1, -1) and (
        (self.colore == "bianco" and differenzaRighe == 1) or
        (self.colore == "nero" and differenzaRighe == -1)
        )
         )
        

    
class Cavallo(Pezzo):
    """Classe che rappresenta il cavallo.

    Args : 
         colore (str): Il colore del cavallo ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte il cavallo.
    """

    @classmethod
    def listaCavalliIniziali(cls)->list:
        """Prepara una lista di cavalli sia neri che bianchi, nelle posizioni iniziali.

        Returns :
        list:Una lista di oggetti Cavallo con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        posizioni=[("bianco", "b1"), ("bianco", "g1"), ("nero", "b8"), ("nero", "g8")]
        return [Cavallo(colore, posizione) for colore, posizione in posizioni]
    
    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Cavallo", colore, posizioneInizialeScacchiera)
    
    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str)->bool:
       """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
       Args :
           mossa (str): La mossa da verificare, rappresentata come stringa.

       Returns :
           bool: True se la mossa è valida, False altrimenti.
       """
       differenzaColonne, differenzaRighe = self.calcolaDifferenze(mossa)
       return(
           (differenzaColonne == 2 and differenzaRighe ==1) or
           (differenzaColonne == 1 and differenzaRighe == 2)
          )
          
       
       
       
    
class Torre(Pezzo):
    """Classe che rappresenta la torre.

    Args : 
         colore (str): Il colore della torre ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte la torre.
    """

    @classmethod
    def listaTorriIniziali(cls)->list:
        """Prepara una lista di torri sia neri che bianchi, nelle posizioni iniziali.

        Returns :
        list:Una lista di oggetti Torre con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        posizioni=[("bianco", "a1"), ("bianco", "h1"), ("nero", "a8"), ("nero", "h8")]
        return [Torre(colore, posizione) for colore, posizione in posizioni]
    
    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Torre", colore, posizioneInizialeScacchiera)
    
    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str)->bool:
       """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
       Args :
           mossa (str): La mossa da verificare, rappresentata come stringa.

       Returns :
           bool: True se la mossa è valida, False altrimenti.
       """
       differenzaColonne, differenzaRighe = self.calcolaDifferenze(mossa)
       return(
           (differenzaColonne == 0 and differenzaRighe>0 )or
           (differenzaRighe == 0 and differenzaColonne>0 )
       )
    
class Alfiere(Pezzo):
    """Classe che rappresenta l'alfiere.

    Args : 
         colore (str): Il colore dell'alfiere ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte l'alfiere.
    """

    @classmethod
    def listaAlfieriIniziali(cls)->list:
        """Prepara una lista di alfieri sia neri che bianchi, nelle posizioni iniziali.

        Returns :
        list:Una lista di oggetti Alfiere con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        posizioni=[("bianco", "c1"), ("bianco", "f1"), ("nero", "c8"), ("nero", "f8")]
        return [Alfiere(colore, posizione) for colore, posizione in posizioni]
    
    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Alfiere", colore, posizioneInizialeScacchiera)
    
    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str)->bool:
       """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
       Args :
           mossa (str): La mossa da verificare, rappresentata come stringa.

       Returns :
           bool: True se la mossa è valida, False altrimenti.
       """
       differenzaColonne,differenzaRighe=self.calcolaDifferenze(mossa)
       return (differenzaColonne==differenzaRighe and differenzaColonne>0)
    
    
    
class Regina(Pezzo):
    """Classe che rappresenta la regina.

    Args : 
         colore (str): Il colore della regina ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte la regina.
    """

    @classmethod
    def listaReginaIniziali(cls)->list:
        """Prepara una lista di Regina sia neri che bianchi, nelle posizioni iniziali.

        Returns :
        list:Una lista di oggetti Regina con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        posizioni=[("bianco", "d1"), ("nero", "d8")]
        return [Regina(colore, posizione) for colore, posizione in posizioni]
    
    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Regina", colore, posizioneInizialeScacchiera)
    
    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str)->bool:
       """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
       Args :
           mossa (str): La mossa da verificare, rappresentata come stringa.

       Returns :
           bool: True se la mossa è valida, False altrimenti.
       """
       differenzaColonne, differenzaRighe = self.calcolaDifferenze(mossa)
       return(
           (differenzaColonne == 0 and differenzaRighe>0 )or
           (differenzaRighe == 0 and differenzaColonne>0 )or
           (differenzaColonne == differenzaRighe and differenzaColonne>0 )

       )    
class Re(Pezzo):
    """Classe che rappresenta il re.

    Args : 
         colore (str): Il colore del re ('bianco' o 'nero').
        posizioneInizialeScacchiera (str): La casella iniziale da cui parte il re.
    """

    @classmethod
    def listaReIniziali(cls)->list:
        """Prepara una lista di Re sia neri che bianchi, nelle posizioni iniziali.

        Returns :
        list:Una lista di oggetti Re con l'attributo posizioneInizialeScacchiera
                 impostato in base alla posizione iniziale sulla scacchiera.
        """
        posizioni=[("bianco", "e1"), ("nero", "e8")]
        return [Re(colore, posizione) for colore, posizione in posizioni]
    
    def __init__(self,colore:str, posizioneInizialeScacchiera:str):
        super().__init__("Re", colore, posizioneInizialeScacchiera)
    
    def __str__(self):
        """Restituisce una rappresentazione testuale del pezzo."""
        return super().__str__()
    
    def __repr__(self):
        """Restituisce una rappresentazione del pezzo nelle struttre dati."""
        return super().__repr__()
    
    def logicaMovimento(self, mossa:str)->bool:
       """Determina se una mossa è valida secondo le regole del pezzo specifico.
        
       Args :
           mossa (str): La mossa da verificare, rappresentata come stringa.

       Returns :
           bool: True se la mossa è valida, False altrimenti.
       """
       differenzaColonne, differenzaRighe = self.calcolaDifferenze(mossa)
        
       return((differenzaColonne <= 1 and differenzaRighe <= 1) and
               (differenzaColonne > 0 or differenzaRighe > 0))
    
    