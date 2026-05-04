import sys
import time

#from rich import print
from scacchi.comandi.listaComandi import help
from scacchi.enginePartita.enginePartita import EnginePartita, clear_terminal


def main():
    """Questa funzione gestisce il menu iniziale del gioco.

    Tipo {Boundary}
    
    Mostra il menu iniziale e gestisce le scelte dell'utente.
    """
    clear_terminal()
    if len(sys.argv)>1:
        arg1=sys.argv[1]
        if arg1=="--help" or arg1=="-h":
            help()
        
        print("\nPer avviare il gioco digitare SI")
        print("altrimenti premi un tasto per uscire")
        scelta=input("\n Scelta-->")
        scelta=scelta.lower()
        if scelta=="si":
            codiceUscita=EnginePartita()
            if codiceUscita==1:
                print("\n La partita è finita ")
                sys.argv.clear()
                time.sleep(3)
                main()
            elif codiceUscita==3:
                print("Sei uscito dal gioco")
    else:
        print("\n\n[BENVENUTI NEL GIOCO DEGLI SCACCHI DEL TEAM GOLDWASSER...]")
        print("    [BUONA FORTUNA E CHE VINCA IL MIGLIORE GIOCATORE]\n\n")
        print("[Per viusalizzare i comandi di gioco inserire il comando /help]\n\n")
        comando=input("\n >>> ")
        if comando=="/gioca":
            codiceUscita=EnginePartita()
            if codiceUscita==1:
                print("\n La partita è finita")
                sys.argv.clear()
                time.sleep(3)
                main()
            elif codiceUscita==3:
                print("Sei uscito dal gioco")
                
        else:
        
            while comando not in ["/gioca","/esci"]:
                    if comando in ["/scacchiera","/abbandona","/patta","/mosse"]:
                        print("\n Partita non ancora avviata, usa il comando /gioca")

                    elif comando=="/help":
                        help()
                    else:
                        print("\n Hai inserito un comando non valido!")
                    
                    comando=input("\n >>> ")

            if comando == "/gioca":
                codiceUscita=EnginePartita()
                if codiceUscita==1:
                    print("\n La partita è finita")
                    sys.argv.clear()
                    time.sleep(3)
                    main()
                elif codiceUscita==3:
                    print("Sei uscito dal gioco")
                
            


if __name__=="__main__":
    main()
    print("\n[GRAZIE PER AVER GIOCATO CON NOI ;) ]")