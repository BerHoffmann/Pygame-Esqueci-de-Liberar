# 3030: Esqueci de Liberar

> Jogo em Python

Projeto CES-22, ITA 2022

### Alunos:

<!--ts-->

-   Bernardo Hoffmann da Silva
-   Marcos Vinicius Pereira Veloso
-   Victor Maciel
<!--te-->

## Como rodar a aplicação:

No terminal, clone o projeto:

```
git clone https://github.com/macieeel/jogoCES22.git
```

_A versão final do jogo está na branch main._

Baixe os módulos:
```
pip install pygame
pip install pytmx
pip install sys
```

Por fim, execute o arquivo main.py:

```
python main.py
```


## INSTRUÇÕES:

O jogo se trata de um entregador que precisa entregar pizzas enquanto está fugindo da polícia.

Ande pelo mapa com WASD ou Setas (direita e esquerda rotacionam sua moto).
Andar na grama diminui sua velocidade e blocos amarelos e verdes escuro são prédios e árvores, e são intransponíveis.
Para entregar as pizzas, siga a seta vermelha do canto superior esquerdo, e quando chegar no marcador, segure a barra de espaço até realizar a entrega.
Cuidado, cada entrega possui um tempo limite indicado na barra.
Não dirija na água e não deixe a polícia encostar em você!




## PASTAS:

### img

Pasta que contém sprites, imagem background, fontes e tiles do mapa.

### maps

Pasta que contém o arquivo TMX do mapa, arquivos utilizados no TILED para gerenciar os tiles do mapa. Existem três versões do mapa diferentes, e a mais atualizada é a mapav2.

### sounds

Pasta com tudo que é relacionado ao som do jogo. Contém as músicas e efeitos sonoros.

### textos

Pasta com todos os arquivos de imagem utilizados para rotular os prédios do mapa.

## DESCRIÇÃO DOS ARQUIVOS .py

### main.py

Execute para jogar o jogo. Possui a classe jogo e a declaração dos objetos com as classes declaradas em outros arquivos. Gerencia as telas iniciais, de game over, de jogo e de pause. Possui as funções principais de update e draw. Realiza o controle dos sons e música.

### sprites.py

Possui as classes do jogador, polícia, obstáculos, pizza, flecha e água. São basicamente as diferentes classes de todas as sprites utilizadas e as funções relacionadas às interações entre elas. Nesse arquivo estão as funções de colisão entre jogador e polícia contra o cenário, do jogador contra a polícia e de ambos com a água. Além disso, há as funções de entrega da pizza e da flecha que deve apontar para a pizza.

### settings.py

Definições de cores e configurações da tela, como tamanho e framerate do jogo. Definição de constantes utilizadas pelo jogador e polícia, como velocidade e caixa de colisão. Definição do tempo total de entrega.

### tilemap.py

Possui a classe camera e a classe tilemap. Realiza a movimentação dos demais objetos com a movimentação do jogador. Função update da camera. Carregamento do tiled map para o jogo. Renderização do mapa dentro do pygame.
