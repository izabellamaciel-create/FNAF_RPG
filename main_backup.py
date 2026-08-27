from pyscript import document
from pyodide.ffi import create_proxy

# ============================================================
# FNAF RPG — A ÚLTIMA NOITE
# Versão web baseada no RPG.ipynb enviado pelo usuário.
# ============================================================

state = {
    "money": 0,
    "courage": 0,
    "mike": 0,
    "has_key": False,
    "has_tape": False,
    "secret_room": False,
    "trusted_phone": False,
    "saw_fredbear": False,
    "friendly_animatronic": False,
    "survived": True,
}

scene_images = {
    0: "assets/intro.jpg",
    1: "assets/cena1.jpg",
    2: "assets/cena2.jpg",
    3: "assets/cena3.jpg",
    4: "assets/cena4.jpg",
    5: "assets/cena5.jpg",
}

# As artes enviadas cobrem a introdução e as cenas 1–5.
# As cenas seguintes mantêm a arte da Cena 5 até novas imagens serem adicionadas.

def img_for(scene_no):
    return scene_images.get(scene_no, "assets/cena5.jpg")


def update_status():
    document.querySelector("#money").textContent = str(state["money"])
    document.querySelector("#courage").textContent = str(state["courage"])
    document.querySelector("#mike").textContent = str(state["mike"])
    document.querySelector("#key").textContent = "SIM" if state["has_key"] else "NÃO"
    document.querySelector("#tape").textContent = "SIM" if state["has_tape"] else "NÃO"
    items = []
    if state["has_key"]: items.append("Chave de arquivo")
    if state["has_tape"]: items.append("Fita VHS de 1983")
    if state["secret_room"]: items.append("Pista da sala secreta")
    if state["saw_fredbear"]: items.append("Encontro com Fredbear")
    document.querySelector("#archive-text").textContent = ", ".join(items) if items else "Nenhuma pista registrada."


def set_scene_header(number, title, time_label=""):
    document.querySelector("#scene-kicker").textContent = "INTRODUÇÃO" if number == 0 else f"CENA {number}"
    document.querySelector("#scene-title").textContent = title
    document.querySelector("#scene-number").textContent = f"{number:02d}"
    document.querySelector("#progress-fill").style.width = f"{min(100, max(0, number / 16 * 100))}%"
    document.querySelector("#time-label").textContent = time_label
    img = document.querySelector("#scene-image")
    frame = document.querySelector(".art-frame")
    frame.classList.add("changing")
    img.src = img_for(number)
    def remove_change(event):
        frame.classList.remove("changing")
    img.addEventListener("load", create_proxy(remove_change), {"once": True})
    img.alt = title


def clear_choices():
    area = document.querySelector("#choice-area")
    area.innerHTML = ""
    document.querySelector("#continue-btn").classList.add("hidden")


def show_text(text):
    el = document.querySelector("#story-text")
    el.textContent = text.strip()
    el.scrollIntoView({"behavior": "smooth", "block": "nearest"})


def button(label, callback):
    b = document.createElement("button")
    b.className = "choice-btn"
    b.textContent = label
    b.addEventListener("click", create_proxy(callback))
    document.querySelector("#choice-area").appendChild(b)
    return b


def continue_button(callback):
    b = document.querySelector("#continue-btn")
    b.classList.remove("hidden")
    b.addEventListener("click", create_proxy(callback), {"once": True})


def choices(options):
    clear_choices()
    for label, callback in options:
        button(label, callback)


def go(scene):
    scenes[scene]()


def intro():
    set_scene_header(0, "A ÚLTIMA NOITE", "23:00")
    text = """
Você nunca gostou daquela pizzaria.

Desde criança, havia alguma coisa estranha naquele lugar.

As paredes coloridas. As músicas infantis que não pareciam tão simples assim.
Os animatrônicos sorrindo para as crianças, e o desaparecimento de várias delas.

Tudo parecia alegre demais ou só falso demais.
E talvez fosse justamente isso que assustava você.

Durante anos, seu pai trabalhou na Freddy's.
Ele dizia que era apenas um emprego.

"São só robôs", ele falava.
"Você não precisa ter medo deles."

Mas seu pai morreu há três meses.
Um acidente de carro.
Pelo menos era isso que dizia o relatório, mas você nunca teve acesso completo a ele.

Você tentou seguir em frente.
Tentou procurar emprego.
Tentou cuidar da sua mãe.

Mas as coisas ficaram cada vez mais difíceis.
Sua mãe precisava de dinheiro para continuar o tratamento de reabilitação.

E você tinha uma irmã pequena.
Abby.

Ela tinha apenas alguns anos e ainda acreditava que o mundo era um lugar seguro.
Você não podia deixar que ela descobrisse o quanto as coisas estavam ruins.

Naquela noite, você estava sentado na cozinha, contando as poucas notas
que ainda restavam na sua carteira.

Não era suficiente.

Nem de longe.

Foi então que o telefone tocou.

Do outro lado da linha, uma voz masculina falou:

"Boa noite. Estamos procurando alguém para trabalhar no turno da noite."

Você ficou em silêncio.
O homem continuou.

"É na Freddy Fazbear's Pizza."

Seu coração acelerou.
Você conhecia aquele lugar.
Todo mundo conhecia.
Suas memórias da sua infância voltaram com tudo.

A pizzaria estava fechada havia alguns anos, mas uma pequena unidade havia sido reaberta recentemente.
O salário era absurdamente alto para um trabalho noturno.
Alto o bastante para pagar o tratamento da sua mãe.
Alto o bastante para comprar comida.
Alto o bastante para garantir que Abby não precisasse se preocupar com nada.

Você perguntou por que o salário era tão alto.

O homem respondeu apenas:

"Porque quase ninguém aceita."

Você deveria ter desligado.
Mas pensou na sua mãe.

Pensou em Abby.
E aceitou.
"""
    show_text(text)
    choices([("ACEITAR O TURNO — começar a noite", lambda _event: go(1))])


def cena1():
    set_scene_header(1, "A CHEGADA", "23:47")
    show_text("""
Depois de uma longa tarde se preparando mentalmente pro seu novo trabalho,
você estaciona o carro em frente à Freddy Fazbear's Pizza.

A placa está parcialmente quebrada.
Algumas letras ainda piscam — "FREDDY FAZBEAR'S PIZZA".

O estacionamento está vazio.
Completamente vazio.

Você pega sua mochila e caminha até a entrada.
A porta está destrancada.
Isso deveria ser estranho.

Mas você entra mesmo assim.
O cheiro de poeira é a primeira coisa que percebe.

Depois vem o som.
Uma música infantil toca ao longe.
Uma música antiga.

Você olha para o palco.
Freddy está lá, o animatrônico marrom, com seu famoso chapéu preto.
Bonnie está ao lado dele, mais desgastado.
Chica está do outro lado, segurando o famoso Mr. Cupcake.

Eles estão exatamente da forma como você lembrava quando era criança,
apenas mais desgastados e sujos.

Foxy está escondido atrás da cortina.
Todos estão desligados.
Pelo menos aparentemente.
""")
    choices([
        ("Ir imediatamente para a sala de segurança.", lambda _event: scene1_a(1)),
        ("Examinar os animatrônicos.", lambda _event: scene1_a(2)),
        ("Procurar o escritório do gerente.", lambda _event: scene1_a(3)),
    ])


def scene1_a(op):
    if op == 1:
        state["courage"] += 1
        text = """
Você decide não perder tempo.
Quanto mais cedo começar, mais cedo poderá ir embora.

No caminho para a sala de segurança, você passa pelo palco.
Por um segundo, tem a impressão de que Freddy está olhando para você.

Você olha novamente.
Ele está parado.
Imóvel.

Você respira fundo.
"É só paranoia.", você diz, tentando acreditar em si mesmo.
"""
    elif op == 2:
        state["money"] += 20
        text = """
Você se aproxima do palco.
Freddy parece velho.
Muito mais velho do que nas fotografias do seu passado.

Você percebe algo estranho.
Há marcas profundas no chão em frente ao palco.
Como se algo pesado tivesse sido arrastado.

Você se agacha.
Encontra uma pequena peça metálica.
Parece fazer parte de um animatrônico.

Você guarda no bolso.
Talvez possa vender depois.
Talvez possa ajudar a entender o lugar.
"""
    else:
        state["has_key"] = True
        text = """
Você procura o escritório do gerente.
Depois de alguns minutos, encontra uma porta com uma placa:

GERÊNCIA.

A porta está trancada.
Ao lado dela existe uma pequena caixa de metal.

Dentro, você encontra uma chave.
A etiqueta diz:

"ARQUIVO."

Você guarda a chave.
Não sabe para que serve.

Ainda.
"""
    show_text(text); update_status(); choices([("Continuar para a sala de segurança →", lambda _event: go(2))])


def cena2():
    set_scene_header(2, "O ESCRITÓRIO", "00:15")
    show_text("""
Você finalmente chega à sala de segurança.
Há dois monitores, um telefone e duas portas blindadas de ferro.

E uma quantidade assustadora de câmeras.
Você começa a testar os equipamentos.

Então o telefone toca.
Você atende.

"Olá?"

Silêncio.

Depois:

"Você é o novo guarda?"

A voz parece masculina.

Você responde que sim.

"Meu nome é Mike."

Ele diz que trabalhou ali antes.

"Eu preciso te avisar de algumas coisas."

Você pergunta o quê.

Mike demora alguns segundos para responder.

"Não confie nos animatrônicos."

Você olha para as câmeras.

Freddy está no palco.
Bonnie também.
Chica também.

Mike continua:

"E principalmente..."

A ligação começa a falhar.

"...não deixe..."

Chiado.

"...ele..."

A chamada cai.
Você congela.
""")
    choices([
        ("Confiar no aviso de Mike.", lambda _event: scene2_a(1)),
        ("Ignorar Mike e seguir as regras da empresa.", lambda _event: scene2_a(2)),
        ("Tentar ligar novamente para Mike.", lambda _event: scene2_a(3)),
    ])


def scene2_a(op):
    if op == 1:
        state["mike"] += 2
        text = """
Você anota mentalmente o aviso.
Não sabe quem Mike é, mas o nome é familiar.

Alguma coisa na voz dele parecia verdadeira.
Você decide observar as câmeras com atenção.
"""
    elif op == 2:
        text = """
Você balança a cabeça.

"Provavelmente só está tentando me assustar."

Você segue as instruções do manual.
Economizar energia.
Monitorar as câmeras.
Manter as portas fechadas apenas quando necessário.

Parece simples.
"""
    else:
        state["mike"] += 1
        text = """
Você liga novamente.
Dessa vez, Mike atende.

"Eu sabia que você ligaria."

Você pergunta o que aconteceu com os outros guardas.

Mike responde:

"Alguns foram embora."

Silêncio.

"E alguns não tiveram essa opção."

A ligação termina.
"""
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(3))])


def cena3():
    set_scene_header(3, "AS SOMBRAS", "01:03")
    show_text("""
Você observa as câmeras.
Nada.

01:17.
Nada.

01:29.
Nada.

Então...
Um ruído.

Você olha para a câmera do palco.

Bonnie desapareceu.
Seu coração dispara.

Você troca para outra câmera.
Corredor esquerdo.
Nada.

Outra.
Banheiro.
Nada.

Outra.
Cozinha.
Nada.

Você volta para o palco.

Freddy continua parado.
Chica também.

Bonnie não está mais lá.

Então você ouve:

TOC.
TOC.
TOC.

Alguma coisa bate na porta esquerda.

Você olha para o corredor.
Não há ninguém.

TOC.

Mais forte.

Você precisa decidir rápido.
""")
    choices([
        ("Fechar a porta imediatamente.", lambda _event: scene3_a(1)),
        ("Olhar pelas câmeras primeiro.", lambda _event: scene3_a(2)),
        ("Sair da sala para verificar.", lambda _event: scene3_a(3)),
    ])


def scene3_a(op):
    if op == 1:
        state["courage"] += 1
        text = """
Você fecha a porta.

TOC.
TOC.
TOC.

A coisa do outro lado para.

Você espera.
Cinco segundos.
Dez.
Vinte.

Então a câmera do corredor mostra Bonnie parado diante da porta.
Ele está olhando diretamente para a câmera.

Você sente um arrepio.
Como essas coisas estão ligadas?

Depois de alguns segundos, Bonnie vai embora.
"""
    elif op == 2:
        text = """
Você troca rapidamente pelas câmeras.

Corredor esquerdo.

Bonnie.
Ele está parado a poucos metros da sua sala.

Você fecha a porta.

Bonnie fica olhando para ela.

Depois desaparece.

Você não sabe para onde foi.
"""
    else:
        state["courage"] -= 1
        text = """
Você abre a porta.

O corredor está vazio.

Você dá alguns passos.
Nada.

Então escuta um som atrás de você.

Você vira.

Bonnie está no fim do corredor.

Parado.
Imóvel.

Você corre de volta para o escritório e fecha a porta.

Por pouco.
Muito pouco.
"""
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(4))])


def cena4():
    set_scene_header(4, "ESCOLHAS", "02:00")
    show_text("""
A energia está em 72%.

Você começa a procurar alguma coisa para ocupar a mente depois do susto de Bonnie.
Abre uma gaveta.
Nada.

Outra.
Papéis antigos.

Na terceira gaveta, encontra uma fita VHS.

Existe uma etiqueta:

"1983 — TREINAMENTO."

Você encontra um aparelho antigo.
Depois de alguns minutos, consegue fazê-lo funcionar.

A gravação começa.

Uma voz infantil aparece.

"Bem-vindos à Freddy Fazbear's Pizza!"

Crianças riem.

A câmera mostra o restaurante antigo.
Muito mais colorido.
Muito mais cheio.
Exatamente como ele era na sua época de menino.

Então a gravação muda.

Um homem aparece.

Seu pai.

Você reconhece imediatamente.
Seu coração para.

Ele está conversando com outro funcionário sem saber que estão sendo gravados.
Você aumenta o volume.

Seu pai diz:

"Eu disse que essa coisa não deveria ser usada."

O outro homem responde:

"É tarde demais."

A fita termina.

Você fica imóvel.

Seu pai sabia de alguma coisa.
E nunca contou.
""")
    choices([
        ("Guardar a fita.", lambda _event: scene4_a(1)),
        ("Deixar a fita no aparelho.", lambda _event: scene4_a(2)),
        ("Destruir a fita.", lambda _event: scene4_a(3)),
    ])


def scene4_a(op):
    if op == 1:
        state["has_tape"] = True
        text = "Você guarda a fita dentro da mochila. Se seu pai aparece naquela gravação, existe uma chance de descobrir o que realmente aconteceu com ele."
    elif op == 2:
        text = "Você decide deixar a fita ali. Talvez alguém possa perceber que você assistiu. Mas talvez isso seja exatamente o que você quer."
    else:
        text = "Você quebra a fita. O som plástico da fita se partindo ecoa pela sala. Você não quer saber. Não quer descobrir. Mas algumas coisas não desaparecem quando destruímos as provas."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(5))])


def cena5():
    set_scene_header(5, "A PORTA NO PORÃO", "02:47")
    show_text("""
Uma luz vermelha aparece em uma das câmeras.

Você verifica.
É o corredor que leva ao porão.
O local deveria estar bloqueado.

Mas a porta está aberta.

Você decide investigar.

Desce as escadas.

O ar fica mais frio.

No final do corredor existe uma porta metálica.

Há uma palavra escrita nela:

"ARQUIVO."

Se você encontrou a chave anteriormente, ela serve naquela porta.
Caso contrário, a porta está apenas encostada.

Você entra.

Existem caixas antigas.
Fotos.
Documentos.

E uma parede inteira coberta por desenhos infantis.

Todos mostram Freddy.
Bonnie.
Chica.
Foxy.

E uma quinta figura.

Uma fantasia amarela.

Você reconhece o personagem.

Fredbear.

Ao lado de um dos desenhos existe uma frase escrita por uma criança:

"Ele levou meu irmão."

Você sente o estômago embrulhar.

Então encontra uma fotografia.

Seu pai aparece nela.
Ao lado de vários funcionários.

Um deles está usando uma fantasia amarela.
""")
    choices([
        ("Procurar documentos.", lambda _event: scene5_a(1)),
        ("Voltar imediatamente.", lambda _event: scene5_a(2)),
        ("Procurar uma passagem escondida.", lambda _event: scene5_a(3)),
    ])


def scene5_a(op):
    if op == 1:
        state["secret_room"] = True; state["courage"] += 1
        text = "Você começa a procurar documentos. Encontra registros de desaparecimentos, todos antigos e relacionados à pizzaria. Então encontra um relatório com a assinatura do seu pai: 'Se alguma coisa acontecer comigo, procure a sala que não aparece nas plantas.'"
    elif op == 2:
        text = "Você decide que já viu demais. Volta pelas escadas. Mas quando chega ao corredor... a porta do porão está fechada. Você tem certeza de que a deixou aberta. Você não sabe como."
    else:
        state["secret_room"] = True
        text = "Você examina as paredes. Uma delas parece diferente. Você empurra. Nada. Empurra novamente. CLIQUE. Uma parte da parede se move. Atrás dela existe um corredor estreito. Você não entra. Ainda não. Mas agora sabe que existe algo escondido dentro daquela pizzaria."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(6))])


def cena6():
    set_scene_header(6, "A SEGUNDA LIGAÇÃO", "03:20")
    show_text("""
O telefone toca novamente.

É Mike.

"Você encontrou a fita?"

Você fica em silêncio.
Como ele sabe?

Mike suspira.

"Seu pai esteve aqui antes de mim."

Você pergunta se ele conhecia seu pai.

"Conhecia."

Mike conta que seu pai tentou denunciar o antigo gerente.
Mas ninguém acreditou nele.

"Seu pai descobriu que os animatrônicos não eram simplesmente máquinas com defeito."

Você pergunta:

"Então o que eles são?"

Mike responde:

"Eu não sei."

Pausa.

"Mas eles lembram."

A ligação cai.

Você olha para Freddy na câmera.

Por um instante...

Freddy parece estar sorrindo de maneira diferente.
""")
    choices([
        ("Sim, acreditar em Mike.", lambda _event: scene6_a(1)),
        ("Não acreditar em Mike.", lambda _event: scene6_a(2)),
        ("Perguntar sobre seu pai antes de desligar.", lambda _event: scene6_a(3)),
    ])


def scene6_a(op):
    if op == 1: state["mike"] += 2; text = "Você decide acreditar nele. Mike é a única pessoa que parece saber o que está acontecendo."
    elif op == 2: text = "Você começa a desconfiar de Mike. Talvez ele esteja manipulando você. Talvez tenha alguma relação com o desaparecimento do seu pai."
    else: state["mike"] += 3; text = "Você pergunta: 'Meu pai morreu em um acidente?' Mike fica em silêncio. 'Foi isso que disseram.' Você pergunta se ele sabe que não foi. Mike responde: 'Eu estava lá naquela noite.' A ligação termina."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(7))])


def cena7():
    set_scene_header(7, "ABBY", "04:00")
    show_text("""
Seu celular vibra.

É uma mensagem de Abby.

"Você vai voltar hoje?"

Você olha para o relógio.
Ainda faltam duas horas.

Você responde que sim.

Outra mensagem chega.

"Eu tive um sonho estranho."

Você pergunta sobre o sonho.

Abby responde:

"Um urso amarelo falou comigo."

Seu sangue gela.

Você pergunta o que ele disse.

Ela responde:

"Ele disse que você está procurando seu pai."

Você fica olhando para a tela.

Então chega outra mensagem.

"Ele disse que conhece você."

Nesse momento, todas as luzes do restaurante apagam.

Você fica no escuro.
Apenas a tela do celular ilumina seu rosto.
""")
    choices([
        ("Ligar para Abby.", lambda _event: scene7_a(1)),
        ("Verificar o gerador.", lambda _event: scene7_a(2)),
        ("Ficar na sala de segurança.", lambda _event: scene7_a(3)),
    ])


def scene7_a(op):
    if op == 1: text = "Você liga para Abby. Ela atende. 'Você está aí?' 'Estou.' 'Não deixa ele chegar perto de você.' Você pergunta quem. Abby responde: 'O urso.' A ligação cai."
    elif op == 2: text = "Você pega uma lanterna e vai até o gerador. No caminho, vê uma silhueta. Alta. Amarela. Ela desaparece quando você aponta a luz."
    else: text = "Você permanece na sala. A câmera mostra todos os animatrônicos. Todos desapareceram. Você percebe que nenhum deles está mais no palco."
    show_text(text); choices([("Continuar →", lambda _event: go(8))])


def cena8():
    state["saw_fredbear"] = True
    set_scene_header(8, "FREDBEAR", "04:19")
    show_text("""
Você precisa encontrar uma forma de religar a energia.

Enquanto caminha pelo corredor, escuta uma música.
Uma caixa de música.

Você segue o som.
Entra em uma sala antiga.

No centro existe uma cadeira.

Sentado nela está um animatrônico amarelo.

Fredbear.

Você congela.

Ele não se mexe.

Então seus olhos acendem.

"Você é filho dele."

A voz é baixa.
Quase humana.

Você não consegue responder.

Fredbear continua:

"Seu pai tentou me libertar."

Você pergunta:

"Libertar quem?"

Ele inclina a cabeça.

"Todos nós."

Então a sala muda.

Por alguns segundos, você vê uma memória.

Crianças correndo.
Funcionários gritando.
Uma fantasia amarela.
Seu pai tentando impedir alguma coisa.

Depois tudo desaparece.

Fredbear volta a ficar imóvel.
""")
    update_status()
    choices([
        ("Perguntar onde está seu pai.", lambda _event: scene8_a(1)),
        ("Perguntar quem está dentro dos animatrônicos.", lambda _event: scene8_a(2)),
        ("Correr da sala.", lambda _event: scene8_a(3)),
    ])


def scene8_a(op):
    if op == 1: text = "Fredbear responde: 'Ele tentou voltar.' Você pergunta quando. 'Na última noite.' Você percebe que a morte do seu pai pode ter acontecido dentro da pizzaria."
    elif op == 2: text = "Fredbear olha para você. 'Crianças que nunca foram embora.' Você percebe o significado. Os animatrônicos podem estar possuídos."
    else: text = "Você corre. Não olha para trás. Mas enquanto corre, escuta Fredbear dizer: 'Você vai voltar.' E você sabe que ele está certo."
    show_text(text); choices([("Continuar →", lambda _event: go(9))])


def cena9():
    set_scene_header(9, "O HOMEM DA FANTASIA", "04:37")
    show_text("""
Você retorna para a sala de segurança.

As câmeras voltam.
Por alguns segundos, tudo parece normal.

Então uma câmera mostra uma pessoa.

Um homem.

Ele está usando uma fantasia amarela.

Você aproxima a imagem.

A pessoa olha diretamente para a câmera.
Depois levanta a mão.
Acena.

Você sente o sangue gelar.

O telefone toca.

Você atende.

É Mike.

"Saia daí."

Você pergunta por quê.

"Ele voltou."

Você pergunta quem.

Mike responde:

"O homem que começou tudo."

A ligação termina.

A câmera fica preta.
""")
    choices([
        ("Fugir imediatamente.", lambda _event: scene9_a(1)),
        ("Procurar o homem.", lambda _event: scene9_a(2)),
        ("Continuar na sala e esperar.", lambda _event: scene9_a(3)),
    ])


def scene9_a(op):
    if op == 1: text = "Você corre para a saída. Mas a porta principal está trancada. Você tenta abrir. Nada. A única saída é continuar procurando uma forma de escapar."
    elif op == 2: text = "Você decide procurar o homem. Talvez ele saiba o que aconteceu com seu pai. Talvez seja a única chance de descobrir a verdade."
    else: text = "Você fica. A sala fica silenciosa. Então alguém bate na porta. Uma vez. Duas. Três. Você não abre. Depois de alguns segundos, a batida para."
    show_text(text); choices([("Continuar →", lambda _event: go(10))])


def cena10():
    set_scene_header(10, "BONNIE", "05:01")
    show_text("""
Você ouve passos.

Bonnie aparece no corredor.
Ele entra na sala.

Você pensa que vai morrer.

Mas ele para.

Não ataca.

A cabeça dele se vira lentamente.

Então ele aponta para uma porta lateral.

Você percebe que ele está tentando mostrar alguma coisa.
Talvez uma armadilha.
Talvez não.

Bonnie espera.
""")
    choices([
        ("Seguir Bonnie.", lambda _event: scene10_a(1)),
        ("Ficar parado.", lambda _event: scene10_a(2)),
        ("Tentar conversar com ele.", lambda _event: scene10_a(3)),
    ])


def scene10_a(op):
    if op == 1: state["friendly_animatronic"] = True; text = "Você segue Bonnie. Ele leva você até uma sala antiga. Na parede existe uma mensagem: 'ELE NÃO É O INIMIGO.' Bonnie então volta para o corredor. Você entende que os animatrônicos talvez não sejam todos seus inimigos."
    elif op == 2: text = "Você não confia nele. Bonnie fica parado por alguns segundos. Depois vai embora. Você talvez tenha perdido uma oportunidade importante."
    else: state["friendly_animatronic"] = True; text = "Você pergunta: 'Você consegue me entender?' Bonnie não responde. Mas aponta para uma fotografia. É uma foto do seu pai. Depois aponta para você e para a porta. Você entende. Ele conhecia seu pai."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(11))])


def cena11():
    set_scene_header(11, "O ESCRITÓRIO DO GERENTE", "05:15")
    show_text("""
Você encontra finalmente o escritório do gerente.
A porta está aberta.

Dentro existe uma mesa.
Um computador.
E uma pasta.

Você abre.

Dentro existem contratos.
Relatórios.
E pagamentos.

Você encontra algo inesperado.

Um documento relacionado ao salário dos guardas.
O valor era alto porque ninguém permanecia no emprego por muito tempo.

Você também encontra uma conta bancária antiga.
Há dinheiro suficiente para pagar vários meses do tratamento da sua mãe.

Mas o dinheiro pertence à empresa.
Você poderia simplesmente pegá-lo.

Ninguém perceberia.
Talvez.
""")
    choices([
        ("Pegar o dinheiro.", lambda _event: scene11_a(1)),
        ("Não pegar.", lambda _event: scene11_a(2)),
        ("Pegar apenas o suficiente para ajudar sua mãe.", lambda _event: scene11_a(3)),
    ])


def scene11_a(op):
    if op == 1: state["money"] += 500; text = "Você pega o dinheiro. A necessidade venceu a consciência. Mas percebe uma coisa: a câmera no canto da sala está ligada. Alguém pode ter visto."
    elif op == 2: text = "Você fecha a pasta. Não vai transformar a situação da sua família em outra mentira."
    else: state["money"] += 200; text = "Você pega apenas uma pequena quantia. O suficiente para ajudar. Você sabe que ainda está errado. Mas não consegue deixar sua mãe sem tratamento."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(12))])


def cena12():
    state["secret_room"] = True
    set_scene_header(12, "A SALA QUE NÃO EXISTE", "05:32")
    show_text("""
Você finalmente encontra a passagem mencionada pelo seu pai.

O corredor termina em uma parede falsa.
Você atravessa.

Existe uma sala pequena.
Sem câmeras.
Sem janelas.

No centro está uma cadeira.
E nela...
um gravador.

Você aperta PLAY.

A voz do seu pai começa.

"Se você está ouvindo isso, significa que eu falhei."

Você começa a chorar.

Ele continua:

"Eu tentei destruir os registros."
"Não consegui."
"A verdade é que as crianças estão presas."
"Os animatrônicos são apenas as prisões."

Então ele fala uma última coisa:

"Mas existe alguém controlando tudo."

Você prende a respiração.

Seu pai diz o nome.

"William Afton."

A gravação termina.

Você percebe que seu pai sabia quem era o responsável.
E talvez tenha morrido tentando impedir que ele continuasse.
""")
    update_status(); choices([("Continuar →", lambda _event: go(13))])


def cena13():
    set_scene_header(13, "A ARMADILHA", "05:45")
    show_text("""
A porta fecha atrás de você.

Você tenta abrir.
Nada.

O homem da fantasia aparece na outra extremidade da sala.

Ele tira a máscara.

É um homem velho.

Ele olha para você.

"Seu pai era persistente."

Você pergunta:

"Você matou ele?"

Ele sorri.

"Seu pai escolheu o próprio destino."

Você sente raiva.

Ele continua:

"Você não deveria ter vindo."

Você pergunta por que ele ainda está ali.

Ele responde:

"Porque algumas coisas nunca morrem."

As luzes começam a piscar.

Atrás dele, Freddy aparece.
Depois Bonnie.
Depois Chica.
E Foxy.

O homem olha para eles.

"Façam o que sempre fizeram."

Você percebe que não tem muito tempo.
""")
    choices([
        ("Enfrentar o homem.", lambda _event: scene13_a(1)),
        ("Fugir.", lambda _event: scene13_a(2)),
        ("Tentar fazer os animatrônicos se voltarem contra ele.", lambda _event: scene13_a(3)),
    ])


def scene13_a(op):
    if op == 1: state["courage"] += 3; text = "Você pega um pedaço de metal no chão. Não é uma arma. Mas é tudo que você tem. Você avança. O homem recua. Os animatrônicos observam. Por alguns segundos, ninguém se mexe."
    elif op == 2: text = "Você corre para a saída lateral. O homem tenta impedir você. Mas Bonnie aparece entre vocês. Você consegue escapar."
    else: state["courage"] += 2; text = "Você grita: 'Vocês não precisam obedecer a ele!' Os animatrônicos param. O homem perde o sorriso. Pela primeira vez, ele parece assustado."
    show_text(text); update_status(); choices([("Continuar →", lambda _event: go(14))])


def cena14():
    set_scene_header(14, "AS CRIANÇAS", "05:53")
    show_text("""
Os animatrônicos começam a se mover.

Mas não contra você.

Freddy olha para o homem.
Chica olha.
Bonnie também.

O homem dá um passo para trás.

"Não."

As luzes piscam.

Você começa a ouvir vozes infantis.

Uma.
Duas.
Cinco.
Muitas.

As vozes repetem:

"Ele mentiu."
"Ele mentiu."
"Ele mentiu."

O homem corre.
Os animatrônicos vão atrás.

Você fica parado.

Então uma pequena figura aparece no corredor.

Uma criança.

Ela olha para você.

"Seu pai tentou ajudar."

Você pergunta:

"Ele está aqui?"

A criança sorri.

"Não mais."

Ela desaparece.

Você entende.

Seu pai não está preso ali.
Ele conseguiu libertar pelo menos uma parte deles.

Mas a história ainda não acabou.
""")
    choices([("Continuar →", lambda _event: go(15))])


def cena15():
    set_scene_header(15, "06:00", "06:00")
    show_text("""
O relógio marca 06:00.

A energia retorna.
As portas se abrem.

O homem desapareceu.
Os animatrônicos voltaram ao palco.

Tudo parece normal.
Quase.

Você pega sua mochila.

Dentro dela estão:
- A fita.
- Os documentos.
- As provas.
- E a verdade sobre seu pai.

Você sai da pizzaria.
O sol começa a nascer.

Você olha para trás.

Freddy está na janela.
Observando você.

Você entra no carro.

Seu celular vibra.

É Abby.

"Você voltou?"

Você responde:

"Sim."

Ela manda outra mensagem.

"Ele está aí?"

Você olha para o banco traseiro.
Não há ninguém.

Você responde:

"Quem?"

Abby responde:

"O urso amarelo."

Você congela.

Então escuta uma voz atrás de você:

"Olá."

Você vira.

A tela fica preta.
""")
    choices([("Ver o desfecho →", lambda _event: go(16))])


def final_scene():
    set_scene_header(16, "O FINAL", "06:01")
    clear_choices()
    if state["courage"] >= 3 and state["mike"] >= 3 and state["saw_fredbear"]:
        title = "FINAL — VERDADEIRA LIBERTAÇÃO"
        text = """
Você sobreviveu.

Mas não esqueceu.

Nas semanas seguintes, você entrega as provas às autoridades.
Os documentos do seu pai são analisados.
A história da pizzaria é reaberta.

Famílias que perderam crianças recebem respostas.
Sua mãe consegue continuar o tratamento.
Abby volta a sorrir.

Você nunca mais trabalha na Freddy's.

Mas uma noite, enquanto organiza as coisas do seu pai,
encontra uma última fotografia.

Atrás dela existe uma frase:

"Obrigado por terminar o que comecei."

Você sorri.
Pela primeira vez desde a morte dele.

Talvez seu pai finalmente esteja em paz.
"""
    elif state["courage"] <= 0:
        title = "FINAL — PRESO"
        text = """
Você sobreviveu àquela noite.
Mas não conseguiu descobrir toda a verdade.

Dias depois, começa a receber ligações.
Sempre às 03:00.
Ninguém fala.
Apenas uma música infantil toca.

Você tenta ignorar.
Até que uma noite encontra uma pequena caixa na porta de casa.

Dentro existe uma fotografia.
Você.
Abby.
Sua mãe.

E atrás de vocês...
Freddy.

No verso está escrito:

"Uma noite ainda não terminou."

Você percebe tarde demais.
A pizzaria não ficou para trás.
Ela veio com você.
"""
    elif state["money"] >= 200 and not state["has_tape"]:
        title = "FINAL — O DINHEIRO"
        text = """
Você não descobriu toda a verdade.
Mas conseguiu dinheiro suficiente para ajudar sua família.

Sua mãe continua o tratamento.
Abby continua estudando.
Você consegue outro emprego.
A vida melhora.

Mas você nunca conta a ninguém sobre aquela noite.

Anos depois, a Freddy Fazbear's Pizza fecha novamente.
Você pensa que acabou.

Até receber uma carta.

Dentro dela existe uma fotografia antiga.
Seu pai aparece nela.

E atrás dele...
uma criança.

Você nunca descobriu quem era.
"""
    elif state["friendly_animatronic"] and state["secret_room"]:
        title = "FINAL — OS AMIGOS"
        text = """
Você descobriu a verdade.

Os animatrônicos não eram simplesmente monstros.
Eles eram vítimas.

Com a ajuda de Bonnie, você encontrou provas suficientes
para expor o passado da pizzaria.

A unidade é demolida.
As crianças finalmente são libertadas.

Durante a última noite antes da demolição,
você volta uma última vez.

Bonnie está sentado no palco.

Você diz:

"Obrigado."

Ele move lentamente a cabeça.
Depois fecha os olhos.

Você vai embora.

Quando a construção começa no dia seguinte,
não há nenhum corpo dentro dos animatrônicos.

Eles simplesmente desapareceram.
Como se finalmente tivessem ido para casa.
"""
    elif state["has_tape"] and state["saw_fredbear"] and state["mike"] >= 2:
        title = "FINAL ESPECIAL — O LEGADO"
        text = """
Você entrega a fita para Mike.

Ele escuta.
Quando termina, fica em silêncio.

Depois diz:

"Seu pai conseguiu."

Você pergunta:
"Conseguiu o quê?"

Mike responde:
"Ele deixou uma saída."

Juntos, vocês investigam os documentos.
A verdade começa a aparecer.

Mas existe uma última coisa que vocês descobrem.

William Afton não desapareceu.

Ele está em algum lugar.
Esperando.

E agora ele sabe que você está procurando por ele.

A história não terminou.

Ela apenas começou.
"""
    else:
        title = "FINAL — SOBREVIVENTE"
        text = """
Você sobreviveu à primeira noite.
Isso já é alguma coisa.

Você recebe o pagamento.
Volta para casa.
Compra os medicamentos da sua mãe.
Compra comida.

E promete a Abby que nunca mais vai voltar para aquela pizzaria.

Por alguns meses, tudo fica bem.

Até que uma manhã você recebe uma carta.
Sem remetente.

Dentro existe apenas uma frase:

"Obrigado por jogar."

Você olha pela janela.

Do outro lado da rua...
há um homem usando uma fantasia amarela.

Quando você pisca...
ele desaparece.
"""
    show_text(f"{title}\n\n{text}")
    update_status()
    document.querySelector("#choice-area").innerHTML = ""
    b = document.createElement("button")
    b.className = "continue-btn"
    b.textContent = "↻ JOGAR NOVAMENTE"
    b.addEventListener("click", create_proxy(restart))
    document.querySelector("#choice-area").appendChild(b)


scenes = {0: intro, 1: cena1, 2: cena2, 3: cena3, 4: cena4, 5: cena5, 6: cena6, 7: cena7, 8: cena8, 9: cena9, 10: cena10, 11: cena11, 12: cena12, 13: cena13, 14: cena14, 15: cena15, 16: final_scene}


def start_music():
    audio = document.querySelector("#music")
    try:
        audio.volume = 0.28
        audio.play()
        document.querySelector("#music-btn").textContent = "🔊 Música"
    except Exception:
        document.querySelector("#music-btn").textContent = "▶ Música"


def toggle_music(event=None):
    audio = document.querySelector("#music")
    if audio.paused:
        start_music()
    else:
        audio.pause()
        document.querySelector("#music-btn").textContent = "🔇 Música"


def restart(event=None):
    state.update({"money":0,"courage":0,"mike":0,"has_key":False,"has_tape":False,"secret_room":False,"trusted_phone":False,"saw_fredbear":False,"friendly_animatronic":False,"survived":True})
    document.querySelector("#start-screen").classList.remove("hidden")
    document.querySelector("#game-screen").classList.add("hidden")
    document.querySelector("#music").pause()
    document.querySelector("#music-btn").textContent = "🔇 Música"
    update_status()


def start_game(event=None):
    document.querySelector("#start-screen").classList.add("hidden")
    document.querySelector("#game-screen").classList.remove("hidden")
    update_status()
    start_music()
    go(0)


document.querySelector("#start-btn").addEventListener("click", create_proxy(start_game))
document.querySelector("#restart-btn").addEventListener("click", create_proxy(restart))
document.querySelector("#music-btn").addEventListener("click", create_proxy(toggle_music))
