"""Test per la logica delle Pedine."""


from scacchi.astrazionePezzi.pezzi import Alfiere, Cavallo, Pedone, Re, Regina, Torre


def test_logica_movimento_Pedone():
 """Test logica movimento Pedone."""
 pedone=Pedone("bianco","a2")

 assert pedone.logicaMovimento("a2 a4","a2")
 assert pedone.logicaMovimento("a2 b3","a2")
 assert not pedone.logicaMovimento("e2 e2","e2")
 assert not pedone.logicaMovimento("a1 h8","e3")

def test_logica_movimento_Torre():
 """Test logica movimento Torre."""
 torre=Torre("bianco","h1")

 assert torre.logicaMovimento("a2 a4")
 assert torre.logicaMovimento("e1 e8")
 assert torre.logicaMovimento("a3 h3")
 assert not torre.logicaMovimento("a2 b3")
 assert not torre.logicaMovimento("e2 e2")
 assert not torre.logicaMovimento("a1 h8")


def test_logica_movimento_Cavallo():
  """Test logica movimento Cavallo."""
  cavallo=Cavallo("bianco", "b1")

  assert cavallo.logicaMovimento("g1 h3")
  assert cavallo.logicaMovimento("g8 h6")
  assert not cavallo.logicaMovimento("g1 h4")
  assert not cavallo.logicaMovimento("a2 g3")

def test_logica_movimento_Alfiere():
  """Test logica movimento Alfiere."""
  alfiere=Alfiere("bianco", "c1")

  assert alfiere.logicaMovimento("c1 d2")
  assert alfiere.logicaMovimento("a1 d4")
  assert not alfiere.logicaMovimento("a1 a4")
  assert not alfiere.logicaMovimento("a1 e1")


def test_logica_movimento_Regina():
  """Test logica movimento Regina."""
  regina=Regina("bianco", "d1")

  assert regina.logicaMovimento("c1 c8")
  assert regina.logicaMovimento("a1 h8")
  assert regina.logicaMovimento("c1 d2")
  assert not regina.logicaMovimento("g1 h3")


def test_logica_movimento_Re():
  """Test logica moviemnto Re."""
  re=Re("bianco", "e1")

  assert re.logicaMovimento("a1 b2")
  assert re.logicaMovimento("a1 a2")
  assert re.logicaMovimento("a1 b1")
  assert not re.logicaMovimento("a1 a3")
  assert not re.logicaMovimento("a1 b3")