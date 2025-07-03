import pygame
import random
import time

# 게임 초기 설정
pygame.init()
pygame.font.init()  # 폰트 시스템 초기화

# 게임 화면 크기 설정
GAME_WIDTH = 450  # 게임 영역 너비 (10칸)
INFO_WIDTH = 150  # 정보 영역 너비 (5칸)
SCREEN_WIDTH = GAME_WIDTH + INFO_WIDTH
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GAME_COLUMNS = GAME_WIDTH // GRID_SIZE
GAME_ROWS = SCREEN_HEIGHT // GRID_SIZE

# 폰트 설정
FONT_SIZE = 20
INFO_FONT_SIZE = 16
MIDDLE_FONT_SIZE = 30
LARGE_FONT_SIZE = 50
game_font = pygame.font.SysFont('arial', FONT_SIZE)
info_font = pygame.font.SysFont('arial', INFO_FONT_SIZE)
middle_font = pygame.font.SysFont('arial', MIDDLE_FONT_SIZE, bold=True)
large_font = pygame.font.SysFont('arial', LARGE_FONT_SIZE, bold=True)

# 게임에서 사용할 색상 정의
SCREEN_BACKGROUND = (50, 44, 187)   # 화면 배경색
EMPTY_CELL = (0, 0, 0)              # 빈 셀 색상
GAME_BACKGROUND_TOP = (50, 44, 187)   # 게임 배경색 상단
GAME_BACKGROUND_BOTTOM = (46, 95, 216)   # 게임 배경색 하단
GAME_BORDER = (50, 44, 187)         # 테두리색
INFO_BACKGROUND = (36, 44, 84)      # 정보 영역 배경색
INFO_BORDER = (36, 44, 84)         # 정보 영역 테두리색
PREVIEW_BACKGROUND = (0, 0, 0)   # 미리보기 배경색
PREVIEW_BORDER = (0, 0, 0)   # 미리보기 테두리색
WHITE = (255, 255, 255)             # 텍스트 색상
GUIDE_COLOR = (255, 255, 255, 40)  # 가이드 블록 색상 (반투명 흰색)
YELLOW = (255, 187, 2)              # 보너스 텍스트 색상
RED = (222, 76, 69)                 # 패널티 텍스트 색상

# 테트리스 블록 정의 (모양과 색상을 함께 정의)
TETROMINOES = {
    'I': {
        'shape': [[1, 1, 1, 1]],  # I 블록: 파란색 긴 막대
        'color': (77, 113, 255)    # Blue
    },
    'T': {
        'shape': [[1, 1, 1],      # T 블록: 하늘색 T자
                 [0, 1, 0]],
        'color': (70, 207, 255)    # Sky Blue
    },
    'Z': {
        'shape': [[1, 1, 0],      # Z 블록: 주황색 Z자
                 [0, 1, 1]],
        'color': (255, 130, 7)      # Orange
    },
    'S': {
        'shape': [[0, 1, 1],      # S 블록: 보라색 S자
                 [1, 1, 0]],
        'color': (149, 87, 230)      # Violet
    },
    'O': {
        'shape': [[1, 1],         # O 블록: 녹색 정사각형
                 [1, 1]],
        'color': (63, 215, 48)    # Green
    },
    'L': {
        'shape': [[1, 1, 1],      # L 블록: 빨간색 L자
                 [1, 0, 0]],
        'color': (226, 45, 43)    # Red
    },
    'J': {
        'shape': [[1, 1, 1],      # J 블록: 노란색 J자
                 [0, 0, 1]],
        'color': (255, 209, 48)      # Yellow
    },
    'U': {
        'shape': [[1, 0, 1],      # U 블록: 시안색 U자
                 [1, 1, 1]],
        'color': (77, 254, 169)      # Cyan
    },
    'V': {
        'shape': [[1, 1],      # V 블록: 분홍색 V자
                 [0, 1]],
        'color': (255, 125, 244)      # Pink
    }
}

# 게임 상태 상수
GAME_STATE_PLAYING = 'playing'
GAME_STATE_PAUSED = 'paused'
GAME_STATE_GAME_OVER = 'game_over'
GAME_STATE_LEVEL_TRANSITION = 'level_transition'
GAME_STATE_COUNTDOWN = 'countdown'
GAME_STATE_COMPLETED = 'completed'

# 레벨 관련 상수
LINES_PER_LEVEL = 10      # 레벨업에 필요한 줄 수
MAX_LEVEL = 10            # 최대 레벨
BONUS_MESSAGE_TIME = 2    # 보너스 메시지 표시 시간 (초)
CLEAR_MESSAGE_TIME = 5    # 클리어 메시지 표시 시간 (초)
SCORE_PER_LINE = 100      # 기본 줄당 점수
SPEED_BONUS_MULTIPLIER = 10  # 시간 보너스 배율 (초당)
PENALTY_MULTIPLIER = 2   # 시간 패널티 배율 (초당)

# 레벨별 설정
LEVEL_SETTINGS = {
    1: {"drop_time": 1000, "target_time": 120},   # 1레벨: 기본 속도, 목표 120초
    2: {"drop_time": 900, "target_time": 110},   # 2레벨: 110초
    3: {"drop_time": 800, "target_time": 100},   # 3레벨: 100초
    4: {"drop_time": 700, "target_time": 90},    # 4레벨: 90초
    5: {"drop_time": 600, "target_time": 80},    # 5레벨: 80초
    6: {"drop_time": 500, "target_time": 70},    # 6레벨: 70초
    7: {"drop_time": 400, "target_time": 60},    # 7레벨: 60초
    8: {"drop_time": 300, "target_time": 50},    # 8레벨: 50초
    9: {"drop_time": 200, "target_time": 45},    # 9레벨: 45초
    10: {"drop_time": 100, "target_time": 40}     # 10레벨: 최고 속도, 목표 40초
}

class Tetris:
    def __init__(self):
        """게임 초기화"""
        pygame.init()
        pygame.display.set_caption('테트리스')

        # 화면 설정
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # 게임 상태
        self.reset_game()

    def reset_game(self):
        """게임 상태를 초기화합니다."""
        # 게임 상태
        self.grid = [[EMPTY_CELL for _ in range(GAME_COLUMNS)] for _ in range(GAME_ROWS)]
        self.state = GAME_STATE_COUNTDOWN
        self.running = True

        # 블록 가방 초기화
        self.piece_bag = []
        self.init_piece_bag()

        # 현재 블록과 다음 블록
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

        # 게임 점수와 레벨
        self.score = 0
        self.level = 1
        self.lines_cleared = 0

        # 게임 타이밍 관련
        self.level_start_time = time.time()
        self.show_bonus_until = 0
        self.countdown_start = time.time()
        self.transition_start = 0
        self.last_fall_time = pygame.time.get_ticks()

        # 보너스/패널티 표시
        self.bonus_text = ""
        self.bonus_color = WHITE

        # 키 입력 처리
        self.init_key_controls()

    def init_key_controls(self):
        """키 입력 관련 변수를 초기화합니다."""
        self.das_delay = 170  # DAS (Delayed Auto Shift) 시작 대기 시간
        self.das_speed = 50   # DAS 반복 속도
        self.key_repeat_delay = 170
        self.key_repeat_interval = 50
        self.key_times = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }
        self.key_pressed = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_DOWN: False
        }

    def init_piece_bag(self):
        """7-bag 시스템용 블록 가방을 초기화합니다."""
        pieces = list(TETROMINOES.keys())
        random.shuffle(pieces)
        self.piece_bag.extend(pieces)

    def get_next_piece(self):
        """다음 블록을 가져옵니다. 7-bag 시스템 적용."""
        # 가방이 비었으면 새로 채우기
        if not self.piece_bag:
            self.init_piece_bag()

        # 가방에서 블록 하나 꺼내기
        piece_name = self.piece_bag.pop()
        piece = TETROMINOES[piece_name]

        # 블록을 화면 상단 중앙에 위치시킴
        return {
            'shape': piece['shape'].copy(),
            'color': piece['color'],
            'x': GAME_COLUMNS // 2 - len(piece['shape'][0]) // 2,
            'y': 0
        }

    def new_piece(self):
        """새로운 테트리스 블록을 생성합니다."""
        if not self.piece_bag:
            self.init_piece_bag()

        piece_name = self.piece_bag.pop()
        piece = TETROMINOES[piece_name]

        return {
            'shape': piece['shape'].copy(),
            'color': piece['color'],
            'x': GAME_COLUMNS // 2 - len(piece['shape'][0]) // 2,
            'y': 0
        }

    def draw_block(self, x, y, color):
        """블록을 그립니다."""
        if color == EMPTY_CELL:  # 빈 공간은 그리지 않음
            return

        # 블록 내부
        pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))

        # 3D 효과를 위한 블록 테두리
        light_color = tuple(min(c + 50, 255) for c in color)  # 밝은 면
        dark_color = tuple(max(c - 50, 0) for c in color)     # 어두운 면

        # 테두리 그리기 (시계 방향)
        pygame.draw.line(self.screen, light_color, (x, y), (x + GRID_SIZE - 1, y), 2)  # 상단
        pygame.draw.line(self.screen, light_color, (x, y), (x, y + GRID_SIZE - 1), 2)  # 좌측
        pygame.draw.line(self.screen, dark_color, (x, y + GRID_SIZE - 1), (x + GRID_SIZE - 1, y + GRID_SIZE - 1), 2)  # 하단
        pygame.draw.line(self.screen, dark_color, (x + GRID_SIZE - 1, y + 1), (x + GRID_SIZE - 1, y + GRID_SIZE - 1), 2)  # 우측

    def create_gradient_surface(self, width, height, start_color, end_color):
        """수직 그라데이션 효과를 가진 surface를 생성합니다."""
        surface = pygame.Surface((width, height))
        for y in range(height):
            # 현재 높이에 따른 그라데이션 비율 계산
            ratio = y / height
            # 시작색과 끝색을 보간하여 현재 줄의 색상 계산
            current_color = (
                int(start_color[0] + (end_color[0] - start_color[0]) * ratio),
                int(start_color[1] + (end_color[1] - start_color[1]) * ratio),
                int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            )
            # 현재 줄에 색상 적용
            pygame.draw.line(surface, current_color, (0, y), (width, y))
        return surface

    def draw_game_area(self):
        """게임 영역을 그립니다."""
        # 게임 영역 그라데이션 배경
        gradient_surface = self.create_gradient_surface(GAME_WIDTH, SCREEN_HEIGHT, GAME_BACKGROUND_TOP, GAME_BACKGROUND_BOTTOM)
        self.screen.blit(gradient_surface, (0, 0))

        # 게임 그리드 그리기
        for y in range(GAME_ROWS):
            for x in range(GAME_COLUMNS):
                if self.grid[y][x] != EMPTY_CELL:
                    self.draw_block(x * GRID_SIZE, y * GRID_SIZE, self.grid[y][x])

        # 가이드 라인 그리기 (현재 블록 그리기 전에)
        ghost_piece = self.get_ghost_position()
        self.draw_ghost_piece(ghost_piece)

        # 게임 영역 테두리
        pygame.draw.rect(self.screen, GAME_BORDER, (0, 0, GAME_WIDTH, SCREEN_HEIGHT), 1)

    def draw_info_area(self):
        """정보 영역을 그립니다."""
        # 정보 영역 배경
        pygame.draw.rect(self.screen, INFO_BACKGROUND, (GAME_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))

        # 정보 영역 좌표 설정
        info_left = GAME_WIDTH + 20  # 레이블 시작 x좌표
        info_right = GAME_WIDTH + INFO_WIDTH - 20  # 값 끝 x좌표

        # 레벨 표시
        level_label = info_font.render('LEVEL :', True, WHITE)
        level_value = info_font.render(str(self.level).rjust(7), True, WHITE)
        self.screen.blit(level_label, (info_left, 30))
        # 값 우측 정렬을 위한 위치 계산
        level_value_rect = level_value.get_rect(right=info_right, top=30)
        self.screen.blit(level_value, level_value_rect)

        # 점수 표시
        score_label = info_font.render('SCORE :', True, WHITE)
        score_value = info_font.render(str(self.score).rjust(7), True, WHITE)
        self.screen.blit(score_label, (info_left, 60))
        # 값 우측 정렬을 위한 위치 계산
        score_value_rect = score_value.get_rect(right=info_right, top=60)
        self.screen.blit(score_value, score_value_rect)

        # 다음 블록 미리보기 영역
        preview_box_size = 130  # 기존 120에서 10픽셀 증가
        preview_box_x = GAME_WIDTH + (INFO_WIDTH - preview_box_size) // 2
        preview_box_y = SCREEN_HEIGHT - 160  # 기존 150에서 10픽셀 위로 이동

        # 미리보기 박스 배경
        pygame.draw.rect(self.screen, PREVIEW_BACKGROUND, 
                        (preview_box_x, preview_box_y, 
                         preview_box_size, preview_box_size))
        # 미리보기 박스 테두리
        pygame.draw.rect(self.screen, PREVIEW_BORDER, 
                        (preview_box_x, preview_box_y, 
                         preview_box_size, preview_box_size), 1)

        # 다음 블록 그리기 (중앙 정렬을 위해 위치 조정)
        if self.next_piece:
            # 블록의 크기 계산
            block_width = len(self.next_piece['shape'][0]) * GRID_SIZE
            block_height = len(self.next_piece['shape']) * GRID_SIZE

            # 미리보기 박스 중앙에 위치하도록 좌표 계산
            preview_center_x = preview_box_x + preview_box_size // 2
            preview_center_y = preview_box_y + preview_box_size // 2

            start_x = preview_center_x - block_width // 2
            start_y = preview_center_y - block_height // 2

            # 블록 그리기
            for i, row in enumerate(self.next_piece['shape']):
                for j, cell in enumerate(row):
                    if cell:
                        x = start_x + j * GRID_SIZE
                        y = start_y + i * GRID_SIZE
                        self.draw_block(x, y, self.next_piece['color'])

        # 정보 영역 테두리
        pygame.draw.rect(self.screen, INFO_BORDER, (GAME_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT), 1)

    def draw_piece(self, piece):
        """현재 이동 중인 블록을 화면에 그립니다."""
        for i, row in enumerate(piece['shape']):
            for j, value in enumerate(row):
                if value:  # 블록의 각 부분을 그림
                    self.draw_block(
                        (piece['x'] + j) * GRID_SIZE,
                        (piece['y'] + i) * GRID_SIZE,
                        piece['color']
                    )

    def is_valid(self, piece, dx, dy):
        """블록이 이동 가능한 위치인지 확인합니다.

        Args:
            piece: 검사할 블록
            dx: x축 이동량
            dy: y축 이동량

        Returns:
            bool: 이동 가능하면 True, 불가능하면 False
        """
        for i, row in enumerate(piece['shape']):
            for j, value in enumerate(row):
                if value:
                    nx, ny = piece['x'] + j + dx, piece['y'] + i + dy
                    if (nx < 0 or                # 왼쪽 벽 충돌
                        nx >= GAME_COLUMNS or         # 오른쪽 벽 충돌
                        ny >= GAME_ROWS or           # 바닥 충돌
                        (ny >= 0 and self.grid[ny][nx] != EMPTY_CELL)):  # 다른 블록과 충돌
                        return False
        return True

    def lock_piece(self, piece):
        """블록을 현재 위치에 고정시킵니다."""
        for i, row in enumerate(piece['shape']):
            for j, value in enumerate(row):
                if value:
                    self.grid[piece['y'] + i][piece['x'] + j] = piece['color']
        self.clear_lines()  # 완성된 줄이 있는지 확인하고 제거

    def show_countdown(self):
        """레벨 시작 전 카운트다운을 표시합니다."""
        if self.state != GAME_STATE_COUNTDOWN:
            return False

        current_time = time.time()
        if self.countdown_start == 0:
            self.countdown_start = current_time

        countdown_time = current_time - self.countdown_start
        if countdown_time >= 3:
            self.state = GAME_STATE_PLAYING
            self.level_start_time = current_time  # 카운트다운 후 레벨 시작 시간 설정
            return False

        # 카운트다운 숫자 계산 (3,2,1)
        count = 3 - int(countdown_time)

        # 화면 중앙에 큰 숫자 표시
        count_text = large_font.render(str(count), True, WHITE)
        text_rect = count_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(count_text, text_rect)

        # 레벨 표시
        level_text = large_font.render(f"Level {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70))
        self.screen.blit(level_text, level_rect)

        return True

    def draw_status(self):
        """레벨과 점수 정보를 화면에 표시합니다."""
        # 레벨 표시
        level_text = game_font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

        # 점수 표시
        score_text = game_font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 100, 30))

        # 보너스/패널티 메시지 표시
        current_time = time.time()
        if current_time < self.show_bonus_until:
            # 화면 중앙에 크게 표시
            bonus_surface = middle_font.render(self.bonus_text, True, self.bonus_color)
            bonus_rect = bonus_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(bonus_surface, bonus_rect)

    def calculate_time_bonus(self):
        """레벨 클리어 시간에 따른 보너스/패널티 점수를 계산합니다."""
        level_time = time.time() - self.level_start_time
        target_time = LEVEL_SETTINGS[self.level]["target_time"]

        time_diff = level_time - target_time

        if time_diff <= -5:  # 목표 시간보다 5초 이상 빨리 클리어
            self.score += 1000
            self.bonus_text = "Speed Bonus: +1000!"
            self.bonus_color = YELLOW
        elif time_diff >= 10:  # 목표 시간보다 10초 이상 느리게 클리어
            self.score = max(0, self.score - 200)  # 점수가 음수가 되지 않도록
            self.bonus_text = "Time Penalty: -200"
            self.bonus_color = RED
        else:  # 기본 (보너스/패널티 없음)
            self.bonus_text = "Level Clear!"
            self.bonus_color = WHITE

        self.show_bonus_until = time.time() + BONUS_MESSAGE_TIME  # 2초간 보너스/패널티 메시지 표시

    def show_level_transition(self):
        """레벨 전환 화면을 표시합니다."""
        if self.state != GAME_STATE_LEVEL_TRANSITION:
            return False

        current_time = time.time()
        transition_time = current_time - self.transition_start

        # 2초 동안 레벨 클리어 메시지 표시
        if transition_time < 2:
            clear_text = large_font.render(f"Level {self.level-1} Clear!", True, YELLOW)
            clear_rect = clear_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(clear_text, clear_rect)

            # 보너스/패널티 메시지가 있다면 함께 표시
            if current_time < self.show_bonus_until:
                bonus_surface = game_font.render(self.bonus_text, True, self.bonus_color)
                bonus_rect = bonus_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
                self.screen.blit(bonus_surface, bonus_rect)

            return True

        # 전환 화면 종료, 다음 레벨 준비
        self.prepare_next_level()  # 여기서 다음 레벨 준비
        self.state = GAME_STATE_COUNTDOWN
        self.countdown_start = current_time
        return False

    def check_level_up(self):
        """레벨 업 조건을 확인하고 처리합니다."""
        if self.lines_cleared >= LINES_PER_LEVEL:  # 설정된 줄 수 달성 시 레벨 업
            self.calculate_time_bonus()
            self.level += 1

            if self.level > MAX_LEVEL:  # 최대 레벨 클리어
                self.state = GAME_STATE_COMPLETED
                self.show_bonus_until = time.time() + CLEAR_MESSAGE_TIME
                self.bonus_text = "Congratulations!"
                self.bonus_color = YELLOW
            else:  # 다음 레벨 시작
                self.state = GAME_STATE_LEVEL_TRANSITION
                self.transition_start = time.time()
                self.show_bonus_until = time.time() + BONUS_MESSAGE_TIME

                # 보너스 메시지를 표시하기 위해 prepare_next_level은 나중에 호출
                self.lines_cleared = 0

    def prepare_next_level(self):
        """다음 레벨을 준비합니다."""
        # 게임 그리드 초기화
        self.grid = [[EMPTY_CELL for _ in range(GAME_COLUMNS)] for _ in range(GAME_ROWS)]

        # 블록 초기화
        self.piece_bag = []  # 새로운 블록 가방으로 시작
        self.init_piece_bag()
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

        # 레벨 관련 변수 초기화
        self.level_start_time = time.time()  # 레벨 시작 시간 초기화
        self.last_fall_time = pygame.time.get_ticks()  # 블록 낙하 시간 초기화

        # 키 입력 상태 초기화
        self.key_pressed = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_DOWN: False
        }
        self.key_times = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }

        # 보너스/패널티 메시지는 초기화하지 않음 - 레벨 전환 화면에서 표시되어야 함

    def clear_lines(self):
        """완성된 줄을 찾아 제거하고 점수를 증가시킵니다."""
        # 완성되지 않은 줄(빈 셀이 있는 줄)만 유지
        new_grid = [row for row in self.grid if not all(cell != EMPTY_CELL for cell in row)]
        removed_lines = GAME_ROWS - len(new_grid)

        # 제거된 줄 수만큼 새로운 빈 줄 추가
        self.grid = [[EMPTY_CELL for _ in range(GAME_COLUMNS)] for _ in range(removed_lines)] + new_grid

        # 제거된 줄 수에 따른 점수 계산
        if removed_lines > 0:
            self.score += removed_lines * SCORE_PER_LINE * self.level  # 레벨이 높을수록 더 높은 점수
            self.lines_cleared += removed_lines
            self.check_level_up()

    def update(self):
        """게임 상태를 업데이트합니다."""
        if self.state != GAME_STATE_PLAYING:
            return

        if not self.is_valid(self.current_piece, 0, 1):  # 아래로 이동할 수 없으면
            self.lock_piece(self.current_piece)          # 현재 블록을 고정
            self.current_piece = self.next_piece         # 다음 블록을 현재 블록으로
            self.next_piece = self.new_piece()          # 새로운 다음 블록 생성

            if not self.is_valid(self.current_piece, 0, 0):  # 새 블록이 생성될 공간이 없으면
                self.state = GAME_STATE_GAME_OVER       # 게임 오버
                self.running = False
        else:
            self.current_piece['y'] += 1  # 블록을 한 칸 아래로 이동

    def run(self):
        """게임의 메인 루프를 실행합니다."""
        while self.running:
            current_time = pygame.time.get_ticks()
            self.screen.fill(SCREEN_BACKGROUND)

            # 게임 상태에 따른 화면 업데이트
            if self.state == GAME_STATE_LEVEL_TRANSITION:
                if not self.show_level_transition():
                    self.state = GAME_STATE_COUNTDOWN
                    self.countdown_start = time.time()
            elif self.state == GAME_STATE_COUNTDOWN:
                if not self.show_countdown():
                    self.state = GAME_STATE_PLAYING
            elif self.state == GAME_STATE_PLAYING:
                self.draw_game_area()
                self.draw_info_area()
                self.draw_piece(self.current_piece)

                # 현재 레벨에 따른 블록 낙하 속도 적용
                drop_time = LEVEL_SETTINGS[self.level]["drop_time"]
                if current_time - self.last_fall_time > drop_time:
                    self.update()
                    self.last_fall_time = current_time

            # 보너스/패널티 메시지 표시
            if time.time() < self.show_bonus_until:
                self.draw_bonus_message()

            # 게임 완료 체크
            if self.state == GAME_STATE_COMPLETED and time.time() - self.show_bonus_until > 0:
                self.running = False
                break

            # 이벤트 처리
            self.handle_events()

            pygame.display.flip()
            self.clock.tick(60)

        if self.state == GAME_STATE_COMPLETED:
            print("축하합니다! 모든 레벨을 클리어했습니다!")
        print(f"Game Over! Final Score: {self.score}, Level: {self.level}")
        pygame.quit()

    def handle_events(self):
        """이벤트를 처리합니다."""
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and self.state == GAME_STATE_PLAYING:
                self.handle_keydown(event)
            elif event.type == pygame.KEYUP and self.state == GAME_STATE_PLAYING:
                self.handle_keyup(event)

        # 키 홀딩 상태 처리
        if self.state == GAME_STATE_PLAYING:
            self.handle_key_holding(current_time)

    def handle_keydown(self, event):
        """키 입력을 처리합니다."""
        if event.key == pygame.K_UP:
            self.try_rotate_piece()
        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
            self.key_pressed[event.key] = True
            self.key_times[event.key] = pygame.time.get_ticks()
            self.try_move_piece(event.key)

    def handle_keyup(self, event):
        """키 해제를 처리합니다."""
        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
            self.key_pressed[event.key] = False

    def handle_key_holding(self, current_time):
        """키 홀딩 상태를 처리합니다."""
        for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
            if self.key_pressed[key] and current_time - self.key_times[key] > self.key_repeat_delay:
                self.try_move_piece(key)
                self.key_times[key] = current_time - self.key_repeat_delay + self.key_repeat_interval

    def try_rotate_piece(self):
        """블록 회전을 시도합니다."""
        rotated_piece = {
            'shape': [list(row) for row in zip(*self.current_piece['shape'][::-1])],
            'color': self.current_piece['color'],
            'x': self.current_piece['x'],
            'y': self.current_piece['y']
        }
        if self.is_valid(rotated_piece, 0, 0):
            self.current_piece = rotated_piece

    def try_move_piece(self, key):
        """블록 이동을 시도합니다."""
        if key == pygame.K_LEFT and self.is_valid(self.current_piece, -1, 0):
            self.current_piece['x'] -= 1
        elif key == pygame.K_RIGHT and self.is_valid(self.current_piece, 1, 0):
            self.current_piece['x'] += 1
        elif key == pygame.K_DOWN and self.is_valid(self.current_piece, 0, 1):
            self.current_piece['y'] += 1

    def draw_bonus_message(self):
        """보너스/패널티 메시지를 표시합니다."""
        bonus_surface = middle_font.render(self.bonus_text, True, self.bonus_color)
        bonus_rect = bonus_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(bonus_surface, bonus_rect)

    def get_ghost_position(self):
        """현재 블록의 착지 위치를 계산합니다."""
        if self.level != 1:  # 1레벨에서만 작동
            return None

        ghost_piece = {
            'shape': self.current_piece['shape'],
            'x': self.current_piece['x'],
            'y': self.current_piece['y']
        }

        # 블록을 더 이상 내려갈 수 없을 때까지 아래로 이동
        while self.is_valid(ghost_piece, 0, 1):
            ghost_piece['y'] += 1

        return ghost_piece

    def draw_ghost_piece(self, ghost_piece):
        """착지 위치에 가이드를 그립니다."""
        if not ghost_piece:
            return

        # 반투명 효과를 위한 surface 생성
        ghost_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(ghost_surface, GUIDE_COLOR, (0, 0, GRID_SIZE, GRID_SIZE))

        # 블록의 각 셀에 대해 가이드 표시
        for i, row in enumerate(ghost_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    x = (ghost_piece['x'] + j) * GRID_SIZE
                    y = (ghost_piece['y'] + i) * GRID_SIZE
                    self.screen.blit(ghost_surface, (x, y))

if __name__ == "__main__":
    game = Tetris()  # 게임 인스턴스 생성
    game.run()       # 게임 실행