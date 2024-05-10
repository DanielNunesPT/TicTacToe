class TicTacToe:
    def __init__(self):
        # Inicializar o tabuleiro do jogo com vazios
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.opponent_player = 'O'
        self.available_moves = [(i, j) for i in range(3) for j in range(3)]

    def print_board(self):
        # Exibir o tabuleiro do jogo
        print('\n'.join([' | '.join([cell if cell else ' ' for cell in row]) for row in self.board]))
        print('-' * 9)

    def is_winner(self, player):
        # Verificar se o jogador venceu o jogo
        # Verificar linhas, colunas e diagonais
        return (
            any(all(cell == player for cell in row) for row in self.board) or
            any(all(self.board[i][j] == player for i in range(3)) for j in range(3)) or
            all(self.board[i][i] == player for i in range(3)) or
            all(self.board[i][2 - i] == player for i in range(3))
        )

    def is_draw(self):
        # Verificar se o jogo terminou em empate
        return all(cell != '' for row in self.board for cell in row)

    def make_move(self, row, col, player):
        # Fazer uma jogada
        if (row, col) in self.available_moves:
            self.board[row][col] = player
            self.available_moves.remove((row, col))
            return True
        return False

    def minmax(self, board, depth, is_maximizing):
        # Implementação do algoritmo MinMax
        if self.is_winner(self.opponent_player):
            return -10 + depth
        if self.is_winner(self.current_player):
            return 10 - depth
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row, col in self.available_moves:
                board[row][col] = self.current_player
                score = self.minmax(board, depth + 1, False)
                board[row][col] = ''
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.available_moves:
                board[row][col] = self.opponent_player
                score = self.minmax(board, depth + 1, True)
                board[row][col] = ''
                best_score = min(best_score, score)
            return best_score

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        # Implementação do algoritmo Alpha-Beta
        if self.is_winner(self.opponent_player):
            return -10 + depth
        if self.is_winner(self.current_player):
            return 10 - depth
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row, col in self.available_moves:
                board[row][col] = self.current_player
                score = self.alpha_beta(board, depth + 1, alpha, beta, False)
                board[row][col] = ''
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.available_moves:
                board[row][col] = self.opponent_player
                score = self.alpha_beta(board, depth + 1, alpha, beta, True)
                board[row][col] = ''
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def find_best_move(self, algorithm):
        # Encontre o melhor movimento com base no algoritmo fornecido
        best_score = float('-inf')
        best_move = None
        for row, col in self.available_moves:
            self.board[row][col] = self.current_player
            if algorithm == 'minmax':
                score = self.minmax(self.board, 0, False)
            elif algorithm == 'alpha_beta':
                score = self.alpha_beta(self.board, 0, float('-inf'), float('inf'), False)
            self.board[row][col] = ''
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def play_game(self):
        print("Bem-vindo ao jogo do galo!")
        print("Você é o jogador X e o computador é o jogador O.")
        while True:
            self.print_board()
            if self.is_draw():
                print("O jogo terminou em empate.")
                break
            if self.is_winner(self.current_player):
                print(f"{self.current_player} venceu!")
                break

            if self.current_player == 'X':
                # Turno do jogador humano
                row, col = map(int, input("Digite a linha e a coluna (0-2) separados por espaço: ").split())
                if not self.make_move(row, col, self.current_player):
                    print("Movimento inválido. Tente novamente.")
                    continue
            else:
                # Turno do computador
                print("O computador está jogando...")
                move = self.find_best_move('alpha_beta')  # Use 'minmax' ou 'alpha_beta'
                self.make_move(move[0], move[1], self.current_player)

            # Alternar entre jogadores
            self.current_player, self.opponent_player = self.opponent_player, self.current_player

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
