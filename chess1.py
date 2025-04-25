import pygame
import sys
import chess
import chess.engine
import time

# Colors
LIGHT_BROWN = (245, 222, 179)
DARK_BROWN = (139, 69, 19)
TIMER_FONT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
POPUP_COLOR = (220, 220, 220)
POPUP_TRANSPARENCY = (220, 220, 220, 220)  # Semi-transparent popup

# Chess piece images
PIECE_IMAGES = {
    'P': 'images/white_pawn.png', 'R': 'images/white_rook.png', 'N': 'images/white_knight.png',
    'B': 'images/white_bishop.png', 'Q': 'images/white_queen.png', 'K': 'images/white_king.png',
    'p': 'images/black_pawn.png', 'r': 'images/black_rook.png', 'n': 'images/black_knight.png',
    'b': 'images/black_bishop.png', 'q': 'images/black_queen.png', 'k': 'images/black_king.png',
}

# Path to Stockfish executable
STOCKFISH_PATH = "C:\\stockfish\\stockfish-windows-x86-64-avx2.exe"

class ChessGame:
    def __init__(self):
        pygame.init()
        self.window_size = (1000, 800)
        self.board_size = 700
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = chess.Board()
        self.piece_images = self.load_images()
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_offset = (0, 0)
        self.game_started = False
        self.time_control = 5 * 60  # Default time control is 5 minutes for each player
        self.white_time = self.time_control
        self.black_time = self.time_control
        self.start_time = None
        self.timer_font = pygame.font.Font(None, 30)
        self.game_mode = "Human vs Human"  # Start in Human vs Human mode
        self.ai_engine = None
        self.setup_menu()
        self.time_dropdown_open = False  # Control dropdown state
        self.time_options = [("30+10", 30*60 + 10), ("10+2", 10*60 + 2), ("5+2", 5*60 + 2),
                             ("3+2", 3*60 + 2), ("1+2", 1*60 + 2)]  # Time control options
        self.popup_message = None  # Message to display in popup
        self.popup_start_time = None  # When the popup was shown

    def load_images(self):
        """Load and scale piece images."""
        images = {}
        for piece, path in PIECE_IMAGES.items():
            try:
                image = pygame.image.load(path)
                images[piece] = pygame.transform.scale(image, (self.grid_size, self.grid_size))
            except Exception as e:
                print(f"Error loading image for {piece}: {e}")
        return images

    @property
    def grid_size(self):
        return int(self.board_size // 8)

    def setup_menu(self):
        self.menu_width = self.window_size[0] - self.board_size
        self.menu_area = pygame.Surface((self.menu_width, self.window_size[1]))
        self.menu_area.fill((220, 220, 220))

        # Define button areas
        self.start_button = pygame.Rect(self.board_size + 20, 20, 160, 40)
        self.resign_button = pygame.Rect(self.board_size + 20, 80, 160, 40)
        self.draw_offer_button = pygame.Rect(self.board_size + 20, 140, 160, 40)
        self.new_game_button = pygame.Rect(self.board_size + 20, 200, 160, 40)
        self.game_mode_button = pygame.Rect(self.board_size + 20, 300, 160, 40)
        self.time_control_button = pygame.Rect(self.board_size + 20, 360, 160, 40)  # Time control button

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(self.screen, color, (col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = self.piece_images.get(piece.symbol())
                    if piece_image:
                        self.screen.blit(piece_image, (col * self.grid_size, row * self.grid_size))

        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.dragging_piece, (mouse_x - self.dragging_offset[0], mouse_y - self.dragging_offset[1]))

    def draw_menu(self):
        self.screen.blit(self.menu_area, (self.board_size, 0))
        self.render_button(self.start_button, "Start Game", not self.game_started)
        self.render_button(self.resign_button, "Resign", self.game_started)
        self.render_button(self.draw_offer_button, "Offer Draw", self.game_started)
        self.render_button(self.new_game_button, "New Game", True)
        self.render_button(self.game_mode_button, self.game_mode, True)  # Display current game mode
        self.render_button(self.time_control_button, f"Time: {self.time_control // 60}", True)  # Display time control

        # Draw dropdown if it's open
        if self.time_dropdown_open:
            self.draw_time_dropdown()

        # Display timer for each player
        if self.start_time and self.game_started:
            elapsed_time = time.time() - self.start_time
            if self.board.turn:  # White's turn
                self.white_time -= elapsed_time
            else:  # Black's turn
                self.black_time -= elapsed_time
            self.start_time = time.time()  # Reset start time for next tick

            # Draw the timers for white and black players
            white_timer_text = self.timer_font.render(f"White Time: {int(self.white_time // 60)}:{int(self.white_time % 60):02}", True, TIMER_FONT_COLOR)
            black_timer_text = self.timer_font.render(f"Black Time: {int(self.black_time // 60)}:{int(self.black_time % 60):02}", True, TIMER_FONT_COLOR)
            self.screen.blit(white_timer_text, (self.board_size + 20, 400))
            self.screen.blit(black_timer_text, (self.board_size + 20, 440))

        # Draw popup if there's a message
        if self.popup_message:
            self.draw_popup()

    def draw_time_dropdown(self):
        dropdown_width = self.time_control_button.width
        dropdown_height = len(self.time_options) * 30
        dropdown_x = self.time_control_button.x
        dropdown_y = self.time_control_button.y + self.time_control_button.height

        # Draw dropdown background
        pygame.draw.rect(self.screen, BUTTON_COLOR, (dropdown_x, dropdown_y, dropdown_width, dropdown_height))

        # Draw dropdown options
        font = pygame.font.Font(None, 24)
        for i, (label, _) in enumerate(self.time_options):
            option_rect = pygame.Rect(dropdown_x, dropdown_y + i * 30, dropdown_width, 30)
            pygame.draw.rect(self.screen, BUTTON_COLOR, option_rect)
            option_text = font.render(label, True, TIMER_FONT_COLOR)
            self.screen.blit(option_text, (dropdown_x + 10, dropdown_y + i * 30 + 5))

    def render_button(self, button_rect, text, enabled):
        color = BUTTON_COLOR if enabled else BUTTON_HOVER_COLOR
        pygame.draw.rect(self.screen, color, button_rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, TIMER_FONT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_popup(self):
        popup_width = 300
        popup_height = 100
        popup_rect = pygame.Rect((self.window_size[0] - popup_width) // 2, (self.window_size[1] - popup_height) // 2,
                                  popup_width, popup_height)
        
        # Draw popup background
        pygame.draw.rect(self.screen, POPUP_COLOR, popup_rect)

        # Draw message text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.popup_message, True, TIMER_FONT_COLOR)
        text_rect = text_surface.get_rect(center=popup_rect.center)
        self.screen.blit(text_surface, text_rect)

        # Check if the popup should disappear after a certain time
        if time.time() - self.popup_start_time > 3:  # Show for 3 seconds
            self.popup_message = None  # Hide the popup after 3 seconds

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.board_size:
                        self.handle_dragging(pos)
                    else:
                        self.handle_menu_click(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.board_size:
                        self.handle_drop(pos)
                self.dragging_piece = None
                self.dragging_offset = (0, 0)

    def handle_dragging(self, pos):
        row = pos[1] // self.grid_size
        col = pos[0] // self.grid_size
        self.selected_square = chess.square(col, 7 - row)
        piece = self.board.piece_at(self.selected_square)
        if piece:
            self.dragging_piece = self.piece_images[piece.symbol()]
            self.dragging_offset = (pos[0] - col * self.grid_size, pos[1] - row * self.grid_size)

    def handle_drop(self, pos):
        if self.selected_square is not None:
            target_square = chess.square(pos[0] // self.grid_size, 7 - pos[1] // self.grid_size)
            if self.board.is_legal(chess.Move(self.selected_square, target_square)):
                self.board.push(chess.Move(self.selected_square, target_square))
                self.update_timer()
                if self.game_mode == "Human vs AI" and self.board.turn == chess.BLACK:  # AI's turn
                    self.make_ai_move()
            self.selected_square = None

    def update_timer(self):
        if not self.start_time:
            self.start_time = time.time()

    def make_ai_move(self):
        if self.ai_engine is None:
            self.ai_engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        # Analyze the position and get the best move
        result = self.ai_engine.play(self.board, chess.engine.Limit(time=2.0))  # Give AI 2 seconds to decide
        self.board.push(result.move)
        self.update_timer()

    def toggle_game_mode(self):
        # Toggle between Human vs Human and Human vs AI
        if self.game_mode == "Human vs Human":
            self.game_mode = "Human vs AI"
        else:
            self.game_mode = "Human vs Human"
        print(f"Game mode changed to: {self.game_mode}")  # Debug output

    def handle_menu_click(self, pos):
        if self.start_button.collidepoint(pos):
            self.start_game()
        elif self.resign_button.collidepoint(pos):
            self.resign_game()
        elif self.draw_offer_button.collidepoint(pos):
            self.offer_draw()
        elif self.new_game_button.collidepoint(pos):
            self.new_game()
        elif self.game_mode_button.collidepoint(pos):
            self.toggle_game_mode()  # Call toggle_game_mode when the button is clicked
        elif self.time_control_button.collidepoint(pos):
            self.time_dropdown_open = not self.time_dropdown_open  # Toggle dropdown
        elif self.time_dropdown_open:
            for i, (label, seconds) in enumerate(self.time_options):
                option_rect = pygame.Rect(self.time_control_button.x, self.time_control_button.y + self.time_control_button.height + i * 30,
                                           self.time_control_button.width, 30)
                if option_rect.collidepoint(pos):
                    self.time_control = seconds
                    self.white_time = seconds
                    self.black_time = seconds
                    self.time_dropdown_open = False  # Close dropdown after selection
                    break

    def start_game(self):
        self.game_started = True
        self.board.reset()
        self.white_time = self.time_control
        self.black_time = self.time_control
        self.start_time = None

    def resign_game(self):
        print("Player resigned!")
        self.popup_message = "Player Resigned! Game Over."
        self.popup_start_time = time.time()  # Set the time when the popup is shown
        self.game_started = False

    def offer_draw(self):
        print("Draw offered!")
        self.popup_message = "Draw Offered! Game Over."
        self.popup_start_time = time.time()  # Set the time when the popup is shown
        self.game_started = False

    def new_game(self):
        self.__init__()  # Re-initialize the game

    def run(self):
        while True:
            self.screen.fill((255, 255, 255))
            self.handle_events()
            self.draw_board()
            self.draw_pieces()
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)  # Frame rate

if __name__ == "__main__":
    game = ChessGame()
    game.run()

