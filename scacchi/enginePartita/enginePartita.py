import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import cast

from astrazionePezzi.pezzi import Alfiere, Cavallo, Pezzo, Regina, Torre
from comandi.listaComandi import abbandona, esci, help, patta
from logicaScacchi.logicaScacchiera import Scacchiera, TipoControllo


def clear_terminal():
    """Questa funzione pulisce il terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

"""Tipo {Control}

       Nonostante questa non sia una classe, poichè il concetto di partita
       è solo un assemblaggio personale e può essere modificato dall' utente,
       possiamo indentificare il ruolo in {Control}, poichè unisce input dell' utente
       con la logica delle nostre classi.

"""
def EnginePartita():
    """Questa funzione gestisce il flusso del gioco degli scacchi.

    Inizializza la scacchiera, gestisce i turni dei giocatori e le mosse.
    """
    scacchiera=Scacchiera()
    scacchiera.fillScacchiera(scacchiera.inizializzaPedine())
    turno="bianco"
    mossa=" "
    IndexErrore=0
    clear_terminal()
  

    print("Il gioco inizierà tra...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)  
    clear_terminal()
    

    while scacchiera.run:
        scacchiera.letteraPromozione=None
        

        if scacchiera.isStalloOrMate(turno,TipoControllo.SCACCOMATTO) :
                clear_terminal()           
                scacchiera.stampa_scacchiera()
                print(f"\n[HAI PERSO GIOCARORE {turno.upper()} ,SCACCO MATTO!]\n")
                scacchiera.run=False
                

        elif scacchiera.isStalloOrMate(turno,TipoControllo.STALLO):
                clear_terminal()           
                scacchiera.stampa_scacchiera()
                print(f"\n[IL GIOCATORRE {turno.upper()} E' IN STALLO , PAREGGIO]")
                scacchiera.run=False
                
        else:
            oppostoturno="bianco" if turno=="nero" else "nero"
            clear_terminal()
            scacchiera.stampa_scacchiera()
            print(scacchiera.listaMessaggiErrore[IndexErrore])
            IndexErrore=0
            if scacchiera._seiSottoScacco:
             print("Sei sotto scacco,fai solo mosse che ti liberano dallo scacco")
            print(f"Turno del giocatore -> {turno}")
            mossa=input("Inserisci la mossa in notazione algebrica (es. e2 Cc6)-->")

            #qua ci androanno il capire i comandi
            if mossa=="/patta":
                codiceUscita=patta(turno,oppostoturno)
                if codiceUscita==1:
                    return 1
            
            if mossa=="/esci":
                codiceUscita=esci()
                if codiceUscita==3:
                    return 3
            if mossa=="/mosse":
                if scacchiera.storicoMosse:
                    clear_terminal()
                    print("Storico delle mosse:")
                    for mossa in scacchiera.storicoMosse:
                        print("\n"+mossa)
                    input("\nPremi invio per continuare...")
                    scacchiera.stampa_scacchiera()
                else:
                        print("Nessuna mossa effettuata finora.")
                        input("\nPremi invio per continuare...")

            if mossa=="/scacchiera":
                clear_terminal()
                scacchiera.stampa_scacchiera()
                input("\nPremi invio per continuare...")
            
            if mossa=="/help":
                clear_terminal()
                help()
                input("\nPremi invio per continuare...")

            if mossa=="/abbandona":
                codiceUscita=abbandona(turno,oppostoturno)
                if codiceUscita==1:
                    return 1

            
            if Scacchiera.isMossaArrocco(mossa) and  not scacchiera._seiSottoScacco:
                
                mossa=scacchiera.traduciArrocco(mossa,turno)
                if scacchiera.tryArrocco(mossa,turno):
                
                 turno = "nero" if turno == "bianco" else "bianco"
            
            elif Scacchiera.isMossaValid(mossa):
                mossa="#"
            
            else:
            
                if Scacchiera.isMossaSan(mossa):
                    mossa=scacchiera.myParser(mossa,turno)

                if scacchiera.isMossaValidForPedina(mossa):
                   pedinaInpartenza=scacchiera.getPedineInMossaPartenza(mossa)
                   pedinaInpartenza=cast(Pezzo|None, pedinaInpartenza)
                   if pedinaInpartenza.getColore() == turno:

                    if scacchiera.intentionToEnpassant(mossa,turno):
                        scacchiera.doEnpassant(mossa)
                        turno = "nero" if turno == "bianco" else "bianco"
                        
                    else:

                        if scacchiera.isTraiettoriaLibera(mossa):
                            pedinaoriginale=scacchiera.simulaMossa(mossa)

                            if scacchiera.isReSottoScacco(turno):
                                scacchiera.ripristinaScacchiera(mossa,pedinaoriginale)
                                            
                            else:
                                scacchiera.ripristinaScacchiera(mossa,pedinaoriginale)
                                if((scacchiera.muoviPedine(mossa)) and
                                  (pedinaInpartenza.getNome()=="Pedone") and 
                                    (scacchiera.promozione(mossa,turno))):
                                     
                                    promotion_interattiva(mossa,scacchiera)
                                     


                                turno = "nero" if turno == "bianco" else "bianco"
                        

                else:
                     IndexErrore=1 if mossa not in ["/mosse","/esci","/patta",
                                                    "/scacchiera","/help",
                                                "/abbandona"] else 0




def promotion_interattiva(mossa:str, scacchiera : Scacchiera):
    """Funzione che gestisce una promozione interrativa.

    Args:
        mossa (str): stinga contentente la mossa
        scacchiera (Scacchiera): oggetto di tipo scacchiera.

    """
    posizioneArrivo= mossa.split()[1]

    pedinaInPartenza=cast(Pezzo|None, scacchiera.getPedineInMossaArrivo(mossa))

    
    print("\n\n")
    print("Il pedone è arrivato all'ultima riga! Scegli un pezzo per la promozione:")
    print("1. Regina")
    print("2. Torre")
    print("3. Alfiere")
    print("4. Cavallo")
    scelta = input("\nInserisci il numero del pezzo desiderato: ")

    if scelta == "1":
        scacchiera.scacchiera[posizioneArrivo] = Regina(pedinaInPartenza.getColore(),
                                                            posizioneArrivo)
        scacchiera.storicoMosse.pop()
        scacchiera.storicoMosse.append(scacchiera.ultimaMossa+"=D")
    elif scelta == "2":
        scacchiera.scacchiera[posizioneArrivo] = Torre(pedinaInPartenza.getColore(), 
                                                        posizioneArrivo)
        scacchiera.storicoMosse.pop()
        scacchiera.storicoMosse.append(scacchiera.ultimaMossa+"=T")
    elif scelta == "3":
        scacchiera.scacchiera[posizioneArrivo] = Alfiere(pedinaInPartenza.getColore(), 
                                                            posizioneArrivo)
        scacchiera.storicoMosse.pop()
        scacchiera.storicoMosse.append(scacchiera.ultimaMossa+"=A")
    elif scelta == "4":
        scacchiera.scacchiera[posizioneArrivo] = Cavallo(pedinaInPartenza.getColore(),
                                                            posizioneArrivo)
        scacchiera.storicoMosse.pop()
        scacchiera.storicoMosse.append(scacchiera.ultimaMossa+"=C")
    else:
        print("\nScelta non valida. Il pedone sarà promosso a regina di default.")

        scacchiera.scacchiera[posizioneArrivo] = Regina(pedinaInPartenza.getColore(), 
                                                        posizioneArrivo)
        scacchiera.storicoMosse.pop()
        scacchiera.storicoMosse.append(scacchiera.ultimaMossa+"=D")

        time.sleep(1)
