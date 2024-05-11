class Jogador:
    def __init__(self, nome):
        self.nome = nome

    def jogar(self, tabuleiro):
        raise NotImplementedError("Método 'jogar' não implementado.")

class JogadorHumano(Jogador):
    def jogar(self, tabuleiro):
        while True:
            try:
                row, col = map(int, input(f"{self.nome}, escolha a linha e a coluna (0-2) separadas por espaço: ").split())
                if tabuleiro.valid_move(row, col):
                    return row, col
                else:
                    print("Jogada inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite dois números separados por espaço.")

class JogadorComputador(Jogador):
    def jogar(self, tabuleiro):
        row, col = tabuleiro.find_best_move()
        return row, col

class Tabuleiro:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = None
        self.opponent_player = None

    def print_board(self):
        print('\n'.join([' | '.join([cell if cell else ' ' for cell in row]) for row in self.board]))
        print('-' * 9)

    def valid_move(self, row, col):
        return 0 <= row <= 2 and 0 <= col <= 2 and self.board[row][col] == ''

    def make_move(self, row, col, player):
        if self.valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def is_winner(self, player):
        # Verificar se o jogador venceu o jogo
        return (
            any(all(cell == player for cell in row) for row in self.board) or
            any(all(self.board[i][j] == player for i in range(3)) for j in range(3)) or
            all(self.board[i][i] == player for i in range(3)) or
            all(self.board[i][2 - i] == player for i in range(3))
        )

    def is_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def play_game(self, jogador1, jogador2):
        print("Bem-vindo ao jogo do galo!")
        self.current_player = jogador1
        self.opponent_player = jogador2

        while True:
            self.print_board()

            if self.is_draw():
                print("O jogo terminou em empate.")
                break

            if self.is_winner(self.current_player.nome):
                self.print_board()
                print(f"{self.current_player.nome} venceu!")
                break

            row, col = self.current_player.jogar(self)
            self.make_move(row, col, self.current_player.nome)

            if self.is_winner(self.current_player.nome):
                self.print_board()
                print(f"{self.current_player.nome} venceu!")
                break

            if self.is_draw():
                print("O jogo terminou em empate.")
                break

            self.current_player, self.opponent_player = self.opponent_player, self.current_player


    def minmax(self, depth, is_maximizing):
        if self.is_winner(self.opponent_player.nome):
            return -10 + depth
        if self.is_winner(self.current_player.nome):
            return 10 - depth
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = self.current_player.nome
                        score = self.minmax(depth + 1, False)
                        self.board[row][col] = ''
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = self.opponent_player.nome
                        score = self.minmax(depth + 1, True)
                        self.board[row][col] = ''
                        best_score = min(best_score, score)
            return best_score

    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        if self.is_winner(self.opponent_player.nome):
            return -10 + depth
        if self.is_winner(self.current_player.nome):
            return 10 - depth
        if self.is_draw():
            return 0

        if is_maximizing:
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = self.current_player.nome
                        alpha = max(alpha, self.alpha_beta(depth + 1, alpha, beta, False))
                        self.board[row][col] = ''
                        if beta <= alpha:
                            break
            return alpha
        else:
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = self.opponent_player.nome
                        beta = min(beta, self.alpha_beta(depth + 1, alpha, beta, True))
                        self.board[row][col] = ''
                        if beta <= alpha:
                            break
            return beta

    def find_best_move(self):
        best_score = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = self.current_player.nome
                    score = self.alpha_beta(0, float('-inf'), float('inf'), False)
                    self.board[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move

if __name__ == "__main__":
    print("Escolha o modo de jogo:")
    print("1. Jogador contra Jogador")
    print("2. Jogador contra Computador")
    print("3. Computador contra Computador")

    modo = input("Escolha o modo (1/2/3): ")

    if modo == '1':
        jogador1 = JogadorHumano("Jogador 1")
        jogador2 = JogadorHumano("Jogador 2")
    elif modo == '2':
        jogador1 = JogadorHumano("Jogador Humano")
        jogador2 = JogadorComputador("Computador")
    elif modo == '3':
        jogador1 = JogadorComputador("Computador 1")
        jogador2 = JogadorComputador("Computador 2")
    else:
        print("Modo inválido. Por favor, escolha 1, 2 ou 3.")
        exit()

    tabuleiro = Tabuleiro()
    tabuleiro.play_game(jogador1, jogador2)
