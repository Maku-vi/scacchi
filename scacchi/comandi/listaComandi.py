import time


def help():
    """Visualizza i comandi di gioco con una breve descrizione.

    - /gioca: Inizia la partita se non c'è una in corso.
    - /scacchiera: Mostra i pezzi sulla scacchiera se il gioco è iniziato.
    - /abbandona: Chiede conferma per abbandonare; segnala vittoria se confermato.
    - /patta: Chiede conferma per pareggio; termina la partita se accettato.
    - /esci: Chiede conferma per uscire; chiude l'app se confermato.
    - /help: Mostra questa pagina di aiuto.


    """
    print("\n\n[COMANDI UTILIZZATI NEL GIOCO:]")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/gioca: \n")
    print("[-Se non c'è una partita in corso, attende la prima mossa]")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/scacchiera \n")
    print("[-Se il gioco è iniziato, mostra i pezzi sulla scacchiera]")
    print("[-Se il gioco non e' iniziato l'app suggerisce il comando /gioca]\n")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/abbandona")
    print("\n[L' applicazione chiede conferma ]")
    print("[-Se confermato, l'app segnala vittoria per abbandono]")
    print("[-Se negato, l'app attende nuovi comandi]")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/patta")
    print("\n[L' applicazione chiede conferma all' avversario]")
    print("[-Se l'avversario accetta, la partita termina con il pareggio ]")
    print("[-Se rifiutato, l'app attende nuovi comandi]")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/esci")
    print("\n[L'applicazione chiede conferma]")
    print("[-Se confermato, l'app si chiude]")
    print("[-Se negato, l’app resta in attesa di nuovi comandi]")
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("/help")
    print("\n[-Se chiamato, richiama questa pagina di help]")
    print("--------------------------------------------------------------------------------------------------------------------------")


def patta(turno:str, oppostoTurno:str)->int:
    """Questa funzione propone la patta.

    Args:
        turno (str): è una stringa
        oppostoTurno (str): è una stringa

    Returns:
        int: restituisce un intero

    """
    print(f"\n Il giocatore {turno} ha proposto la patta ")
    print(f"\n Giocatore {oppostoTurno} accetti? ")
    scelta=input("[SI o NO]-->")
    scelta=scelta.lower()
    if scelta=="si":
        print("\n La partita è terminata in pareggio ")
        time.sleep(1)   
        return 1
    elif scelta=="no":
        print("\n Patta rifiutata! ")
        time.sleep(1)
        return 2
    else:
        print("\n Hai inserito una risposta non valida! La patta è rifiutata ")
        time.sleep(1)
        return 2
    
def esci():
    """Questa funzione gestisce l'uscita dal gioco.

    Returns : 
        int: restituisce un intero in base alla scelta
    """
    print("\n Sei sicuro di voler uscire? Si o No")
    scelta=input("scelta->")
    scelta=scelta.lower()
    if scelta=="si":
        return 3
    elif scelta=="no":
        print("\nOperazione annullata")
        time.sleep(1)
        return 4
    else:
        print("Hai inserito una risposta sbagliata, operazione annullata")
        time.sleep(1)
        return 4 
       
def abbandona(turno:str, oppostoTurno:str)->int:
    """Questa funzione permette di abbandonare la partita.

    Args:
        turno (str): è una stringa
        oppostoTurno (str): è una stringa

    Returns:
        int: restituisce un intero

    """
    print(f"\n Gicatore {turno} vuoi abbandonare la partita? ")
    scelta=input("[SI o NO]-->")
    scelta=scelta.lower()
    if scelta=="si":
        print(f"\n Giocatore {oppostoTurno} hai vinto la partita ")
        time.sleep(1)
        return 1
    elif scelta=="no":
        print("\n Operazione annullata")
        time.sleep(1)
        return 2
    else:
        print("\n Hai inserito una risposta non valida! Operazione annullata ")
        time.sleep(1)
        return 2