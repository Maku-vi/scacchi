"""Test per logica di scacchiera principale."""
from scacchi.astrazionePezzi.pezzi import Re, Regina, Torre
from scacchi.logicaScacchi.logicaScacchiera import Pedone, Scacchiera, TipoControllo

scacchiera=Scacchiera()
scacchiera.fillScacchiera(Scacchiera.inizializzaPedine())

#setup per una scacchiera per lo scacco
board=Scacchiera()
board.scacchiera["a1"]=Re("bianco","a1")
board.scacchiera["h1"]=Re("nero","h1")
board.scacchiera["b1"]=Regina("bianco","b1")
#setup per  una scacchiera per lo scacco Matto

boardMate=Scacchiera()
boardMate.scacchiera["a1"]=Re("bianco","a1")
boardMate.scacchiera["h1"]=Re("nero","h1")
boardMate.scacchiera["b1"]=Regina("bianco","b1")
boardMate.scacchiera["b2"]=Regina("bianco","b2")

#setup per una scacchiera per lo Stallo

boardStallo=Scacchiera()
boardStallo.scacchiera["h8"]=Re("nero","h8")
boardStallo.scacchiera["f7"]=Re("bianco","f7")
boardStallo.scacchiera["g6"]=Regina("bianco","g6")

#setup per una scachiera per l' arrocco

boardArrocco=Scacchiera()
boardArrocco.scacchiera["e1"]=Re("bianco","e1")
boardArrocco.scacchiera["h1"]=Torre("bianco", "h1")

#setup per una scaccheira per l' enPassant

boardEnpassant=Scacchiera()
boardEnpassant.scacchiera["e5"]=Pedone("bianco","e2")
boardEnpassant.scacchiera["d5"]=Pedone("nero","d7")
boardEnpassant.ultimaMossaNotaazione="d7 d5"


def test_isMossaValidForPedina():
    """Test per la funzione di mossa valida nella posizione attuale."""
    assert not scacchiera.isMossaValidForPedina("stringanonvalida")
    assert scacchiera.isMossaValidForPedina("a2 a3")
    assert scacchiera.isMossaValidForPedina("g1 f3")
    assert not scacchiera.isMossaValidForPedina("h1 a8")

def test_isTraiettoiraLibera():
    """Test per la funzione di traiettoria valida nella posizione attuale."""
    assert not scacchiera.isTraiettoriaLibera("strinanonvalida")
    assert scacchiera.isTraiettoriaLibera("g1 a3")
    assert scacchiera.isTraiettoriaLibera("e2 e4")


def test_isReSottoScacco():
    """Test per la funzione di scacco."""
    assert not scacchiera.isReSottoScacco("bianco")
    assert not scacchiera.isReSottoScacco("nero")
    assert board.isReSottoScacco("nero")
    assert not board.isReSottoScacco("bianco")

def test_isStalloOrMate():
    """Test per la funzione dello ScaccoMatto."""
    assert boardMate.isStalloOrMate("nero",TipoControllo.SCACCOMATTO)
    assert not boardMate.isStalloOrMate("bianco",TipoControllo.SCACCOMATTO)
    assert boardStallo.isStalloOrMate("nero",TipoControllo.STALLO)
    assert not boardStallo.isStalloOrMate("bianco",TipoControllo.STALLO)


def test_tryArrocco():
    """Test per la funzione di logica arrocco principale."""
    assert boardArrocco.tryArrocco("e1 h1","bianco")

    #aggiungo una torre nella traiettoria per vedere il 
    #risultato sulla traiettoria
    boardArrocco.scacchiera["f1"]=Regina("bianco","f1")

    assert not boardArrocco.tryArrocco("e1 h1", "bianco")

def test_enPassant():
    """Test per la funzione di logica enPassatn."""
    assert boardEnpassant.possibleEnpassant()
    assert boardEnpassant.intentionToEnpassant("e5 d6","bianco")
