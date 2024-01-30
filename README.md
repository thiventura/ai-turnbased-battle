# AI turn-based battle
Jogo criado para a disciplina de Inteligência Artificial do Instituto de Computação da UFMT. O propósito é que os alunos criem os scripts que decidirão quais ações os personagens devem fazer para alcançar a vitória.

<div align="center">
<img src="https://github.com/thiventura/ai-turnbased-battle/assets/26909742/c05ac327-f9a3-4913-b3ab-f1cf8f0e22ca" alt="Printscreen do jogo" style="height: 300px"/>
</div>


## Sobre o jogo
O jogo é uma batalha por turno, no qual 2 personagens lutam entre si. Em cada turno 1 personagem deve avaliar a situação e determinar sua ação. Em seguida, o outro personagem realiza as mesmas etapas. Esse ciclo continua até que um dos personagens esteja sem vida.

Os personagens começam com 9 vidas e as ações permitidas são: se mover (cima, baixo, direita, esquerda), atacar ou se defender.

No cenário, além dos personagens, há 1 coração e 1 arma. O personagem que pegar primeiro o coração tem sua vida completa novamente. E o personagem que pegar primeiro a arma tem os próximos 5 ataques com dano aumentado. Todos esses componentes estarão em um tabuleiro 5x5.

Algumas regras:
- O personagem se move apenas 1 quadrado por ação de movimento
- Os personagens não podem ocupar o mesmo espaço
- O ataque comum tem dano 1
- O ataque com arma tem dano 2
- Os ataques tem alcance de 1 quadrado em todas as direções, inclusive na diagonal
- Se houver um ataque enquanto o adversário está defendendo, o dano é diminuído em 1


## Inteligência Artificial
O foco deste projeto é permitir que conceitos de agentes inteligentes possam ser programados no jogo, fazendo com que cada aluno possa definir o comportamento dos personagens por meio de Inteligência Artificial.

Para tanto, os alunos devem criar programas que recebem o estado do jogo e devem retornar a ação a ser realizada. Como processar os estados e escolher a melhor ação depende da implementação do agente. A utilização de Minimax, por exemplo, encaixa perfeitamente.

Os programas dos agentes inteligentes serão chamados por linha de comando. Assim, eles podem ser programados em qualquer linguagem. O estado será passado por argumentos e a ação deverá ser retornada por meio da saída principal (impressão na tela).

Um estado tem os seguintes atributos:
- id do seu personagem (1 ou 2)
- configuração do tabuleiro contendo 25 números (5x5), no qual: 0 é espaço vazio, 1 é o jogador 1, 2 é o jogador 2, 3 é a arma, 4 é o coração
- vida do jogador 1 (0 a 9)
- vida do jogador 2 (0 a 9)
- munição do jogador 1 (0 a 5)
- munição do jogador 2 (0 a 5)

Um exemplo de estado é: 2 0000401000000000002030000 9 9 0 0. Isso significa que:
- É a vez do jogador 2
- O coração está na posição [0,4], o jogador 1 na [1,1], o jogador 2 na [3,3] e a arma na [4,0]
- Ambos jogadores estão com 9 vidas
- Ambos jogadores estão com 0 munições


## Exemplos de IA
Os programas "ia-dummy.py" e "ia-random.py" são exemplos de agentes deste jogo. O primeiro tenta sempre avançar para perto do adversário e ataca sempre que tiver ao alcance. O segundo apenas sorteia uma ação a ser realizada. Apesar de não serem tão inteligentes, são bons exemplos para verificar como ler o estado atual do jogo e os possíveis comandos.


## Personalização
As imagens de exemplo são do Palword®. Mas facilmente é possível trocar as imagens da pasta "images" para deixar o tema da batalha como desejar.


## Como rodar
Necessário ter Python e a biblioteca pygame:
```console
pip3 install pygame
```

Depois rode o programa `board`
```console
python board.py
```
