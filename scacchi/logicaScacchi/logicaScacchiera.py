import re
from enum import Enum
from typing import cast

from scacchi.astrazionePezzi.pezzi import (
    Alfiere,
    Cavallo,
    Pedone,
    Pezzo,
    Re,
    Regina,
    Torre,
)


class TipoControllo(Enum):
    """Enumerativo rappresentante scacco matto e stallo."""

    SCACCOMATTO=0
    STALLO=1

    """Tipo {Entity}.
       
       Astrae il concetto di scacchiera incapsulando il concetto
       di scacchiera . La classe e di tipo {Entity}, infatti questa logica è 
       pronta per poter essere implementata utilizzando un GUI, siccome non 
       sono presenti input necessari da parte dell ' utente e stampe. L' unica funzione 
       che si distacca da questo concetto è la stampaScacchiera(), necessaria
       per rendere la stampa della scacchiera leggibili per l' umano.
    """
class Scacchiera:
    """Questa classe implementa la scacchiera e la sua logica."""

    _patternMossaCorretta=re.compile(r"^[a-h][1-8] [a-h][1-8]$")
    
    _regexParser=re.compile(r"^(R|D|T|A|C)?([a-h][1-8]|[a-h]|[1-8])?(x)?[a-h][1-8](=[RDTAC])?(\+|#)?$")

    _regexArrocco=re.compile(r"^(0-0|0-0-0)$")

    @classmethod
    def inizializzaPedine(cls):
        """Funzione per inizializzare le pedine.

        Returns:
            list: lista di pedine iniziali

        """
        listaPedone=Pedone.listaPedoniIniziali()
        listaCavalli=Cavallo.listaCavalliIniziali()
        listaAlfieri=Alfiere.listaAlfieriIniziali()
        listaTorri=Torre.listaTorriIniziali()
        listaRegine=Regina.listaReginaIniziali()
        listaRe=Re.listaReIniziali()
        listaPedine=listaPedone+listaCavalli+listaAlfieri+listaTorri+listaRegine+listaRe
        return listaPedine
    
    @classmethod
    def isMossaSan(cls,mossa:str)->bool:
        """Controlla se la mossa è sintatticamente corretta.

        Args :
            mossa (str): è una stringa contenente la mossa

        Returns :
             bool:true se la mossa è sintatticamente corretta, false altrimenti
        """
        return bool(cls._regexParser.match(mossa))

    @classmethod
    def isMossaValid(cls,mossa:str)->bool:
        """Controlla se la mossa è corretta per la notazione funzione.

        Args :
            mossa (str): stringa contenente la mossa.

        Returns :
            bool: True se la mossa è sintatticamente corretta, false altrimenti.
        """
        return bool(cls._patternMossaCorretta.match(mossa))
    
    @classmethod
    def isMossaArrocco(cls,mossa:str)->bool:
        """Controlla se la mossa è un arrocco sintatticamente.

        Args :
            mossa (str): stringa contenente la mossa.

        Returns :
            bool: True se la mossa è un arrocco, False altrimenti.
        """
        return bool(cls._regexArrocco.match(mossa))


    def __init__(self):
        self.scacchiera={f"{col}{r}":None for col in "abcdefgh" for r in range (1,9)}
        self.ultimaMossa=None
        self.letteraPromozione=None
        self.storicoMosse=[]
        self.listaMessaggiErrore=[" ",
                        "\n\n[MOSSA NON VALIDA]\n "]
        self.run=True
        self._seiSottoScacco=False
        self.ultimaMossaNotaazione=None

    def fillScacchiera(self, listaPedine: list[Pezzo]):
        """Funzione per riempire la scacchiera .

           I pezzi vengono inseriti mediante il match tra posizione iniziale
           della pedina e chiave del dizionario

        Args :
            listaPedine (list[Pezzo]): lista contenente solo tipi Pezzo
        """
        for pedina in listaPedine:
            posizione=pedina.getPosizioneInizialeScacchiera()
            if self.scacchiera.get(posizione)is None:
                self.scacchiera[posizione]=pedina


    def stampa_scacchiera(self):
        """La funzione stampa sul terminale lo stato della scacchiera."""
        print("\n\t\t\t\t     [SCACCHIERA]\n")
        print("\n\t\t\t    a   b   c   d   e   f   g   h")
        print("\t\t\t  +---+---+---+---+---+---+---+---+")
        for r in range(8, 0, -1):
            row = f"{r} |"
            for col in "abcdefgh":
                pos = f"{col}{r}"
                pezzo =cast(Pezzo | None, self.scacchiera.get(pos)) 
                if pezzo:
                    if pezzo.getNome() == "Pedone":
                        simbolo = "♟ "  if pezzo.getColore() == "nero" else "♙ "
                    elif pezzo.getNome() == "Cavallo":
                        simbolo = "♞ " if pezzo.getColore() == "nero" else "♘ "
                    elif pezzo.getNome() == "Alfiere":
                        simbolo = "♝ " if pezzo.getColore() == "nero" else "♗ "
                    elif pezzo.getNome() == "Torre":
                        simbolo= "♜ "  if pezzo.getColore() == "nero" else "♖ "
                    elif pezzo.getNome() == "Regina":
                        simbolo= "♛ " if pezzo.getColore() == "nero" else "♕ "
                    elif pezzo.getNome() == "Re":
                        simbolo="♚ " if pezzo.getColore() == "nero" else "♔ "
                else:
                    simbolo = "  "
                row += f" {simbolo}|"
            print("\t\t\t"+row + f" {r}")
            print("\t\t\t  +---+---+---+---+---+---+---+---+")
        print("\t\t\t    a   b   c   d   e   f   g   h\n")
    
    def isMossaValidForPedina(self, mossa:str)->bool:
        """Questa funzione controlla la validita' della mossa sulla casella di partenza.

            Nota bene: questa funzione non controlla la traiettoria.

        Args:
            mossa (str): è una stringa contenente la possibile mossa

        Returns:
            bool: restituisce true se valida, altrimenti false

        """
        if not self.isMossaValid(mossa):
            return False
        
        posizionePartenza=mossa.split()[0]
        for posizione in self.scacchiera:
            if posizionePartenza==posizione:
                pedina=cast(Pezzo | None, self.scacchiera.get(posizione))
                if pedina is not None:
                    if pedina.getNome()=="Pedone":
                        return pedina.logicaMovimento(mossa, posizionePartenza)
                    
                    else:
                        return pedina.logicaMovimento(mossa)
                else: 
                    return False
                
    def isTraiettoriaLibera(self, mossa:str,yesArrocco:bool=False)-> bool:
        """Questa funzione controlla se la traiettoria della mossa è libera.

        Args:
            mossa (str): la mossa è una stringa
            yesArrocco(bool): rappresenta il tipo di controllo da fare se 
                              considerare l'arrocco o no.

        Returns:
            bool: restituisce true traiettoria=libera, false altrimenti

        """
        if not self.isMossaValid(mossa):
            return False
        
        posizionePartenza,posizioneArrivo=self.getPosizionePartenzaArrivo(mossa)

        colPartenza, rigaPartenza = posizionePartenza[0], int(posizionePartenza[1])
        colArrivo, rigaArrivo = posizioneArrivo[0], int(posizioneArrivo[1])
        
        pedinaInPartenza = cast(Pezzo | None, self.scacchiera.get(posizionePartenza))

        if not pedinaInPartenza:
            return False
        
        #Controllo pedone
        if pedinaInPartenza.getNome()=="Pedone":
            if colArrivo==colPartenza:
                if self.scacchiera.get(posizioneArrivo) is None:
                    if abs(rigaArrivo - rigaPartenza) == 2:
                        rigaIntermedia =  (rigaPartenza + 
                                          (1 if rigaArrivo>rigaPartenza else -1))
                        
                        posizioneIntermediaPedone = f"{colPartenza}{rigaIntermedia}"
                        if self.scacchiera.get(posizioneIntermediaPedone) is not None:
                            return False
                    return True

                else:
                    return False
            else:
                if self.getPedineInMossaArrivo(mossa) is not None:
                  pedoneInArrivo=cast(Pezzo|None, self.getPedineInMossaArrivo(mossa))
                  return (pedinaInPartenza.getColore() != pedoneInArrivo.getColore())
                else:
                    return False
        
        #Controllo cavallo
        if pedinaInPartenza.getNome()=="Cavallo":
            pedineInArrivo = cast(Pezzo|None, self.getPedineInMossaArrivo(mossa))
            if pedineInArrivo is None:
                return True
            
            return not (pedineInArrivo and
                        pedineInArrivo.getColore() == pedinaInPartenza.getColore())

        
        deltaCol = ord(colArrivo) - ord(colPartenza)
        deltaRiga = rigaArrivo - rigaPartenza

        passoCol = 0 if deltaCol==0 else int(deltaCol / abs(deltaCol))
        passoRiga = 0 if deltaRiga==0 else int(deltaRiga / abs(deltaRiga))

        colCorrente = ord(colPartenza) + passoCol
        rigaCorrente = rigaPartenza + passoRiga

        while colCorrente != ord(colArrivo) or rigaCorrente != rigaArrivo:
            posizioneIntermedia = f"{chr(colCorrente)}{rigaCorrente}"
            if self.scacchiera.get(posizioneIntermedia) is not None:
                return False
            colCorrente += passoCol
            rigaCorrente += passoRiga

        pedineInArrivo = cast(Pezzo|None, self.getPedineInMossaArrivo(mossa))

        if not yesArrocco:
            return not (pedineInArrivo and
                     pedineInArrivo.getColore() == pedinaInPartenza.getColore())
        else:
            return True


    def muoviPedine(self,mossa:str):
        """Questa funzione sposta le pedine.

        Args:
            mossa (str): la mossa è una stringa

        """      
        if not self.isMossaValid(mossa):
            return False

        pedinaInPartenza=cast(Pezzo|None, self.getPedineInMossaPartenza(mossa))

        if pedinaInPartenza is None:
            return False
        
        posizionePartenza ,posizioneArrivo =self.getPosizionePartenzaArrivo(mossa)

        self.salvaMossaSanPRE(mossa,pedinaInPartenza)
        
        self.scacchiera[posizioneArrivo]=pedinaInPartenza
        self.scacchiera[posizionePartenza]=None

        self.salvaMossaSanPOST(mossa,pedinaInPartenza)

        if pedinaInPartenza.getNome() == "Torre" or pedinaInPartenza.getNome() == "Re":
            pedinaInPartenza.setMovedOnce(True)
        
        self._seiSottoScacco=False

        self.ultimaMossaNotaazione=mossa


        return True
    
    def salvaMossaSanPRE(self,mossa:str, pedinaInPartenza:Pezzo):
        """Salva la mossa nel modo corretto nello storico delle mosse SAN.

        Args :
            mossa (str): stringa contenente la mossa parsata,
                         nel formato "casellaPartenza casellaArrivo".
            pedinaInPartenza (Pedina): pedina presente nella casella di
                                       partenza della mossa. 
        """
        if self.ultimaMossa is not None:
            pedinaInarrivo=self.getPedineInMossaArrivo(mossa)
            if pedinaInarrivo is None:
                self.ultimaMossa=self.ultimaMossa.replace("x","")
        
     
    def salvaMossaSanPOST(self,mossa:str,pedinaInPartenza:Pezzo):
        """Questa funzione segue lo stesso concetto della funzione salvaMossaSanPRE.
        
           Salva alcune mosse che posso essere modificate solo dopo aver effetutato 
           la mossa.

        Args :
            mossa (str): stringa contenente la mossa parsata, 
                         nel formato "casellaPartenza casellaArrivo".

            pedinaInPartenza (Pedina): pedina presente nella casella di
                                       partenza della mossa.

        """
        oppostoTurnoColore ="bianco" if pedinaInPartenza.getColore()=="nero" else "nero"
        
        if self.ultimaMossa is not None:
             self.ultimaMossa=self.ultimaMossa.replace("#","")
             simbolo="="
             posizioneSimbolo=self.ultimaMossa.find(simbolo)
             if posizioneSimbolo != -1 :
                 self.ultimaMossa=self.ultimaMossa[:posizioneSimbolo]
             if not self.isReSottoScacco(oppostoTurnoColore):
                  self.ultimaMossa=self.ultimaMossa.replace("+","")
               
        self.storicoMosse.append(self.ultimaMossa)
        self.ultimaMossaNotaazione =mossa
        
    
    def isReSottoScacco(self,colore:str)->bool:
        """Questa funzione controlla se il re del turno passato è sotto scacco.
           
           - Estrae il re del colore corrispondente alla stringa passata come argomento 
           - Ne salva la posizione in posizioneRe 
           - Compone tutte le mosse iterando sulle chiavi del dizionario ,
             passando alle funzioni di controllo
             logico le mosse composte  "casellaPartenza posizioneRe".
           
           Se trova una composizione valida, siamo sotto scacco,
           setto la variabile scacco a True 
           ed esco restituendo True , False altrimenti

        Args : 
            colore (str): colore del turno attuale ("bianco" o "nero")

        Returns :
            bool: True se sotto scacco, False altrimenti
        """
        for posizione,pedina in self.scacchiera.items():
            pedina=cast(Pezzo|None,pedina)
            if pedina and pedina.getNome() == "Re" and pedina.getColore() == colore:
                posizioneRe=posizione
                
        for posizione, _ in self.scacchiera.items():
              mossa=f"{posizione} {posizioneRe}"
              if self.isMossaValidForPedina(mossa) and self.isTraiettoriaLibera(mossa):
                  self._seiSottoScacco=True
                  return True
              
        return False

    def promozione(self, mossa:str, turno:str)->bool:
        """Funzione che si occupa della promozione di un pedone.

           Args :
            mossa (str): stringa contenente la mossa
            turno (str): stringa contenente il colore del turno

        Returns :
            bool: True se la promozione è stata effettuata, False altrimenti.
        """
        posizioneArrivo= mossa.split()[1]

        pedinaInPartenza=cast(Pezzo|None,self.getPedineInMossaArrivo(mossa))

        rigaArrivo=int(posizioneArrivo[1])

        if ((pedinaInPartenza.getColore()=="bianco" and rigaArrivo==8) or 
            (pedinaInPartenza.getColore()=="nero" and rigaArrivo==1)):

            if not self.letteraPromozione:

                return True
            else:
                if self.letteraPromozione == "D":
                 self.scacchiera[posizioneArrivo]=Regina(pedinaInPartenza.getColore(), 
                                                         posizioneArrivo)
                 self.storicoMosse.pop()
                 self.storicoMosse.append(self.ultimaMossa+"=D")
                elif self.letteraPromozione == "T":
                 self.scacchiera[posizioneArrivo]=Torre(pedinaInPartenza.getColore(), 
                                                         posizioneArrivo)
                 self.storicoMosse.pop()
                 self.storicoMosse.append(self.ultimaMossa+"=T")
                elif self.letteraPromozione == "A":
                 self.scacchiera[posizioneArrivo]=Alfiere(pedinaInPartenza.getColore(), 
                                                          posizioneArrivo)
                 self.storicoMosse.pop()
                 self.storicoMosse.append(self.ultimaMossa+"=A")
                elif self.letteraPromozione == "C":
                 self.scacchiera[posizioneArrivo]=Cavallo(pedinaInPartenza.getColore(), 
                                                           posizioneArrivo)
                 self.storicoMosse.pop()
                 self.storicoMosse.append(self.ultimaMossa+"=C")
                
                return False

            
    
    def isStalloOrMate(self, colore:str, controllo:TipoControllo) -> bool:
        """Funzione che controlla lo scacco matto e lo stallo.

        Args :
            colore (str): stringa contenente il colore del turno.
            controllo (TipoControllo): enumerativo per tipo di controllo.
                                       0 per scacco matto, 1 per stallo.

        Returns :
            bool: restituisce true se si è sotto scacco/stallo, false altrimenti.
        """
        if controllo == TipoControllo.STALLO:
            if self.isReSottoScacco(colore):
                return False
            
        else:
            if not self.isReSottoScacco(colore):
                return False
        
        for posizione, pedina in self.scacchiera.items():
            pedina = cast(Pezzo|None, pedina)
            if pedina and pedina.getColore()==colore:
                for colonna in "abcdefgh":
                    for riga in range (1,9):
                        posizioneArrivo = f"{colonna}{riga}"
                        mossa = f"{posizione} {posizioneArrivo}"
                        if ((self.isMossaValidForPedina(mossa)) and 
                            (self.isTraiettoriaLibera(mossa))):

                            pedinaOriginale=self.simulaMossa(mossa)

                            sottoScacco=self.isReSottoScacco(colore)

                            self.ripristinaScacchiera(mossa,pedinaOriginale)

                            if not sottoScacco:
                                return False
                            
        return True

    def traduciArrocco(self,arrocco:str,turno:str)->str:
        """Questa funzione traduce la notazione SAN dell'arrocco.

        Args :
            arrocco (str): stringa contenente la notazione SAN dell'arrocco
            turno (str): stringa contenente il colore del turno

        Returns :
            str: restituisce la notazione tradotta dell'arrocco
                  se non è un arrocco restituisce una stringa vuota.
        """
        if arrocco=="0-0":
            nuovoArrocco="e1 h1" if turno=="bianco" else "e8 h8"
            return nuovoArrocco
        
        elif arrocco=="0-0-0":
            nuovoArrocco="e1 a1" if turno=="bianco" else "e8 a8"

            return nuovoArrocco
        else:
            return " "
    
    def tryArrocco(self,mossa:str,turno:str)->bool:
        """Controlla la logica delle condizioni in cui si puo' arroccare.

        Args :
            mossa (str): stringa contenente la mossa tradotta 
            turno (str): colore del turno

        Returns :
            bool: True se si puo' arroccare, False altrimenti.
        """
        pedinaRe=self.getPedineInMossaPartenza(mossa)  
        pedinaTorre=self.getPedineInMossaArrivo(mossa)
        posizionePartenza,posizioneArrivo=self.getPosizionePartenzaArrivo(mossa)

        if pedinaRe is None or pedinaTorre is None:
            return False

        pedinaRe=cast(Pezzo|None,pedinaRe)
        pedinaTorre=cast(Pezzo|None,pedinaTorre) 

        if ((pedinaRe.getColore()!=pedinaTorre.getColore()) or
            (pedinaRe.getNome()!="Re") or pedinaTorre.getNome()!="Torre"):
            return False

        if not self.isTraiettoriaLibera(mossa,yesArrocco=True):
            return False
        
        pedinaRe=cast(Pezzo|None,pedinaRe)
        pedinaTorre=cast(Pezzo|None,pedinaTorre)

        if pedinaRe.getMovedOnce() or pedinaTorre.getMovedOnce():

            return False
        
        posizioneTransitorie=self.getPosizioniTransitorieArrocco(posizionePartenza,posizioneArrivo)
        posizioneTransitoria=posizionePartenza
        for posizione in posizioneTransitorie:
            mossaIntermedia=posizioneTransitoria+" "+posizione
            pedinaOriginale=self.simulaMossa(mossaIntermedia)
            if self.isReSottoScacco(turno):

                self.ripristinaScacchiera(mossaIntermedia,pedinaOriginale)
                return False
            posizioneTransitoria=posizione
            self.ripristinaScacchiera(mossaIntermedia,pedinaOriginale)
        
        self.doArrocco(posizionePartenza,posizioneArrivo)
        return True

    def doArrocco(self,posizioneRe:str,posizioneTorre:str):
        """Funzione che esegue l'arrocco.

        Args :
            posizioneRe (str): posizione del re
            posizioneTorre (str): posizione della torre
        """
        colonnaRe=posizioneRe[0]
        rigaRe=int(posizioneRe[1])
        colonnaTorre=posizioneTorre[0]
        if colonnaTorre>colonnaRe:
            nuovaPosizioneRe=f"{chr(ord(colonnaRe)+2)}{rigaRe}"
            nuovaPosizioneTorre=f"{chr(ord(colonnaRe)+1)}{rigaRe}"
        else:
            nuovaPosizioneRe=f"{chr(ord(colonnaRe)-2)}{rigaRe}"
            nuovaPosizioneTorre=f"{chr(ord(colonnaRe)-1)}{rigaRe}"
        
        self.scacchiera[nuovaPosizioneRe]=self.scacchiera[posizioneRe]
        self.scacchiera[posizioneRe]=None

        self.scacchiera[nuovaPosizioneTorre]=self.scacchiera[posizioneTorre]
        self.scacchiera[posizioneTorre]=None

        re=cast(Pezzo|None,self.scacchiera.get(nuovaPosizioneRe))
        re.setMovedOnce(True)

        torre=cast(Pezzo|None,self.scacchiera.get(nuovaPosizioneTorre))
        torre.setMovedOnce(True)

        self.ultimaMossa="0-0"

        self.ultimaMossaNotaazione="Arrocco eseguito"

    
    def possibleEnpassant(self)->bool:
        """Funzione che accerta la possibilità di un Enpassant.

        Returns :
            bool: True se è possibile, False altrimenti_
        """
        if not self.ultimaMossaNotaazione:
            return False
        
        if not self.isMossaValid(self.ultimaMossaNotaazione):
            return False
        
        ultimaPartenza,ultimoArrivo=self.getPosizionePartenzaArrivo(self.ultimaMossaNotaazione)
        pedinaUltima=cast(Pezzo|None,self.getPedineInMossaArrivo(self.ultimaMossaNotaazione))

        if not pedinaUltima:
            return False
        
        if pedinaUltima.getNome()!="Pedone":
            return False
        
        if ultimaPartenza[0]!=ultimoArrivo[0]:
            return False
        
        rigArrivo=int(ultimoArrivo[1])
        rigaPartenza= int(ultimaPartenza[1])


        return (abs(rigArrivo-rigaPartenza)==2)
    
    def intentionToEnpassant(self,mossa:str,turno:str)->bool:
        """Funzione che controlla l'intensione dell'utente.

        Args :
            mossa (str): stringa contenente la mossa
            turno (str): stringa contenente il colore del turno

        Returns :
            bool: True se l'utente vuole fare l'Enpassant, False altrimenti.
        """
        if not self.possibleEnpassant():
            return False
        
        posizionePartenza,posizioneArrivo=self.getPosizionePartenzaArrivo(mossa)

        if posizionePartenza[0]==posizioneArrivo[0]:
            return False
        
        posizioneArrivoMossaPrec=self.ultimaMossaNotaazione.split()[1]
        rigaArrivoMossaPrec=int(posizioneArrivoMossaPrec[1])
        rigaPartenza=int(posizionePartenza[1])
        rigaArrivo=int(posizioneArrivo[1])

        if rigaPartenza!=rigaArrivoMossaPrec:
            return False
        
        colonnaArrivoMossaPrec=posizioneArrivoMossaPrec[0]
        colonnaArrivo=posizioneArrivo[0]

        if colonnaArrivoMossaPrec!=colonnaArrivo:
            return False   

        if turno=="bianco" and rigaArrivo-rigaPartenza==1:
            return True

        if turno=="nero" and rigaArrivo-rigaPartenza==-1:
            return True 
    
    def doEnpassant(self,mossa:str):
        """_Funzione che termina logica di Enpassant.

        Args :
            mossa (str): stringa contenente la mossa.
        """
        posizioneArrivo=self.ultimaMossaNotaazione.split()[1]
        self.scacchiera[posizioneArrivo]=None 
        self.muoviPedine(mossa)
   
    #funzioni rigurdanti il parsing della mossa
    def myParser(self,mossa:str,turno:str)->str:
        """Questa funzione si occupa di pare il pasring delle mosse.

           Utilizzando diverse regex, il programma analizza il tipo di mossa in 
           notazione SAN ricevuta e la traduce nel formato "casella iniziale" "spazio" 
           "casella finale"
           
        Args :
            mossa (str): stringa contenente la mossa SAN
            turno (str): stringa contenente il colore del turno attuale

        Returns :
            mossaValida(str): stringa contente la mossa tradotta per le nostre funzioni
                              se non venisse trovata una mossa valida restituisce "#"
                              in modo che la funzione isMossaValidForPedina poi rifiuta 
                              questa mossa

        """
        allDisambiguate=re.compile(r"^(R|D|T|A|C)?([a-h][1-8])[a-h][1-8]$")
        noDisambiguate=re.compile(r"^(R|D|T|A|C)?[a-h][1-8]$")
        disambiguoColonna=re.compile(r"^(R|D|T|A|C)?[a-h][a-h][1-8]$")
        disambiguoRiga=re.compile(r"^(R|D|T|A|C)?[1-8][a-h][1-8]$")

        self.ultimaMossa=mossa

        mossa=mossa.replace("x","")
        mossa=mossa.replace("+","")
        mossa=mossa.replace("#","")

        posizioneUguale=mossa.find("=")

        if posizioneUguale != -1:
            #per il momento non ci serve ma sarà utile quando si implementerà 
            #la promozione del pedone
            self.letteraPromozione=mossa[posizioneUguale+1]
            mossa=mossa[:posizioneUguale+1]
            mossa=re.sub(r"[^a-zA-Z0-9]", "", mossa)  
                                                      

        if allDisambiguate.match(mossa):
              

             if mossa[0].isupper():
                 return mossa[1]+mossa[2]+" "+mossa[3]+mossa[4]
             else:
                 return mossa[0]+mossa[1]+" "+mossa[2]+mossa[3]
             
        elif noDisambiguate.match(mossa):

             if mossa[0].islower():
                 mossa="P"+mossa  


                           
             if mossa[0] == "P":
                mossa=self.exractFromParser(mossa,"Pedone",turno)
             elif mossa[0] == "C":
                mossa=self.exractFromParser(mossa,"Cavallo",turno)
             elif mossa[0] == "D":
                mossa=self.exractFromParser(mossa,"Regina",turno)
             elif mossa[0] == "R":
                mossa=self.exractFromParser(mossa, "Re", turno)
             elif mossa[0] == "T":
                mossa=self.exractFromParser(mossa,"Torre",turno)
             elif mossa[0] == "A":
                mossa=self.exractFromParser(mossa,"Alfiere",turno)
            
             return mossa

        
        elif disambiguoColonna.match(mossa):
        
             if mossa[0].islower():
                 mossa="P"+mossa 
             
             colonnaDisambiguata=mossa[1]
             
             listaMosseEstratte=[]
             mossaValida="#"

             for posizione,pedina in self.scacchiera.items():
                 pedina=cast(Pezzo | None,pedina)
                 if ((pedina) and (pedina.getNome()[0] == mossa[0]) and 
                     (pedina.getColore() == turno) and 
                     (posizione[0] == colonnaDisambiguata)):
                      posizionePedina=posizione
                      mossaComposta=posizionePedina+" "+mossa[2]+mossa[3] 

                      if ((self.possibleEnpassant()) and 
                         (self.intentionToEnpassant(mossaComposta,turno))):
                             mossaValida=mossaComposta

                      elif ((self.isMossaValidForPedina(mossaComposta)) and 
                           (self.isTraiettoriaLibera(mossaComposta))):
                            listaMosseEstratte.append(mossaComposta)
                            mossaValida=mossaComposta
                            if(len(listaMosseEstratte)==2):
                                
                              mossaValida="#"
                              
             return mossaValida
        

        elif disambiguoRiga.match(mossa):

             if mossa[0].islower():
                 mossa="P"+mossa 
             
             rigaDiasambiguata=mossa[1]

             listaMosseEstratte=[]
             mossaValida="#"

             for posizione,pedina in self.scacchiera.items():
                 pedina=cast(Pezzo | None,pedina)
                 if ((pedina) and (pedina.getNome()[0] == mossa[0]) and 
                  (pedina.getColore() == turno) and 
                  (posizione[1] == rigaDiasambiguata)):
                      posizionePedina=posizione
                      mossaComposta=posizionePedina+" "+mossa[2]+mossa[3]

                      if ((self.possibleEnpassant()) and 
                         (self.intentionToEnpassant(mossaComposta,turno))):
                             mossaValida=mossaComposta 
                     
                      elif ((self.isMossaValidForPedina(mossaComposta)) and 
                            (self.isTraiettoriaLibera(mossaComposta))):
                            listaMosseEstratte.append(mossaComposta)
                            mossaValida=mossaComposta
                            if(len(listaMosseEstratte)==2):
                                
                             mossaValida="#"
                 
             return mossaValida


        else:
            return "#"       
    
    def exractFromParser(self,mossa:str,daCercare:str,colore:str)->str:
         """Questa funzione compone le possibili mosse per poi estrarle.
            
            In base a quale pezzo bisogna cercare compone le possibili mosse e ne 
            controlla la validità quando ne trova solamente una la passa all' engine
            se invece ne trovasse piu' di una capirebbe che la SAN inserita era ambigua
            e quindi restituirebbe una stringa non valida che poi verrà rifiutata 
            dalle altre funzioni.Vi sono due pezzi di funzione presenti nella funzione 
            myPaser molto simili a questo, poichè questo si occupa delle mosse che 
            vengono passate senza avere disambiguazioni es. (Cf3,Ta3,Da5,ecc..)

         Args :
            mossa (str): stringa rappresentante la mossa in SAN
            daCercare (str): nome del pezzo da dover cercare es. "Pedone"
            colore (str): colore del pezzo da dover cercare es. "bianco"

         Returns :
            mossaValida: stringa contenente "#" se la ricerca è andata male
                         altrimenti contiene la mossa tradotta correttamente
         """
         mossaValida="#"
         listaMosseEstratte=[]
         for posizione,pedina in self.scacchiera.items():
          pedina=cast(Pezzo | None,pedina)
          if pedina and pedina.getNome() == daCercare and pedina.getColore() == colore:
             posizionePedina=posizione
             mossaComposta=posizionePedina+" "+mossa[1]+mossa[2]

             if ((self.possibleEnpassant()) and 
                         (self.intentionToEnpassant(mossaComposta,colore))):
                             mossaValida=mossaComposta

             elif ((self.isMossaValidForPedina(mossaComposta)) and 
                    (self.isTraiettoriaLibera(mossaComposta))):
                listaMosseEstratte.append(mossaComposta)
                mossaValida=mossaComposta
                if(len(listaMosseEstratte)==2):
                        
                 
                 mossaValida="#"
    
         
         return mossaValida
            

    #funzioni ausiliari
    def getPosizionePartenzaArrivo(self,mossa:str):
        """Questa funzione estrae dalla mossa posizione di partenza e arrivo.

        Args:
            mossa (str): è una stringa

        Returns:
            str: restituisce due stringhe contenenti posizione partenza e arrivo

        """
        posizionePartenza=mossa.split()[0]
        posizioneArrivo=mossa.split()[1]
        return posizionePartenza,posizioneArrivo
    

    def getPedineInMossaArrivo(self, mossa:str)->(Pezzo|None):
        """Questa funzione estrae la pedina in posizione di arrvo della mossa.

        Args :
            mossa(str): è una stringa

        Returns :
            pedina (Pezzo|None): se la pedina esiste la restituisce, altrimenti None
        """
        posizioneArrivo=mossa.split()[1]
        pedina=self.scacchiera.get(posizioneArrivo)
        return pedina
    
    def getPedineInMossaPartenza(self, mossa:str)->(Pezzo|None):
        """Questa funzione estrae la pedina in posizione di partenza della mossa.

        Args :
            mossa(str): è una stringa

        Returns :
            pedina (Pezzo|None): se la pedina esiste la restituisce, altrimenti None
        """
        posizionePartenza=mossa.split()[0]
        pedina=self.scacchiera.get(posizionePartenza)
        return pedina
    

    def simulaMossa(self, mossa:str)->(Pezzo|None):
        """La funzione simulla una mossa sulla scacchiera.
           
           La simulazione della mossa viene fatta senza alcun tipo di controllo.
           Tiene traccia della pedina che eventualmente era presente
           nella casella di arrivo in modo da poter ripristinare
           la scacchiera allo stato precedente alla simulazione

           Utilizzata per assicurarsi che le proprie mosse 
           non ci mettano sotto scacco da sole.
        Args :
            mossa (str): stringa contenente la mossa parsata, 
            nel formato "casellaPartenza casellaArrivo".

        Returns :
            pedinaOriginale(None|Pedina): oggetto di tipo pedina se presente 
                                          nella casella di arrivo, None altrimenti
        """
        posizionePartenza ,posizioneArrivo =self.getPosizionePartenzaArrivo(mossa)

        pedinaOriginale = self.getPedineInMossaArrivo(mossa)
        self.scacchiera[posizioneArrivo] = self.scacchiera[posizionePartenza]
        self.scacchiera[posizionePartenza] = None
        return pedinaOriginale
    
    def ripristinaScacchiera(self, mossa:str, pedinaOriginale):
        """La funzione ripristina la scacchiera.
           
           Il ripristino della scacchiera avviene 
           attraverso il passaggio della mossa di cui fare il rollback 
           e la eventuale pedina  salvata dalla funzione simulaMossa.


        Args :
            mossa (str): stringa contenente la mossa parsata, 
                                 nel formato "casellaPartenza casellaArrivo".
            
            pedinaOriginale(None|Pedina) : pedina che verrà rimessa nella 
                                           vecchia posizione di arrivo, se esiste.
        """
        posizionePartenza ,posizioneArrivo =self.getPosizionePartenzaArrivo(mossa)


        self.scacchiera[posizionePartenza] = self.scacchiera[posizioneArrivo]
        self.scacchiera[posizioneArrivo] = pedinaOriginale
    

    def getPosizioniTransitorieArrocco(self,posizioneRe:str,posizioneTorre:str)->tuple:
        """Funzione che ricava le posizioni transitorie dell 'arrocco.

        Args :
            posizioneRe (str): posizione partenza del Re
            posizioneTorre (str): posizione partenza della Torre

        Returns :
            tuple: primaposizione,secondaposizione . Stringhe contententi le caselle
        """
        colonnaRe=posizioneRe[0]
        rigaRe=int(posizioneRe[1])
        colonnaTorre=posizioneTorre[0]

        if colonnaTorre>colonnaRe:
            primaPosizione = f"{chr(ord(colonnaRe)+1)}{rigaRe}"
            secondaPosizione = f"{chr(ord(colonnaRe)+2)}{rigaRe}"
            return [primaPosizione,secondaPosizione]
        else:
            primaPosizione = f"{chr(ord(colonnaRe)-1)}{rigaRe}"
            secondaPosizione = f"{chr(ord(colonnaRe)-2)}{rigaRe}"
            return [primaPosizione,secondaPosizione]