// 게임 상수 정의
const GAME_WIDTH = 450;
const INFO_WIDTH = 150;
const SCREEN_WIDTH = GAME_WIDTH + INFO_WIDTH;
const SCREEN_HEIGHT = 600;
const GRID_SIZE = 30;
const GAME_COLUMNS = Math.floor(GAME_WIDTH / GRID_SIZE);
const GAME_ROWS = Math.floor(SCREEN_HEIGHT / GRID_SIZE);

// 색상 정의
const COLORS = {
    SCREEN_BACKGROUND: '#322CBB',
    EMPTY_CELL: '#000000',
    GAME_BACKGROUND_TOP: '#322CBB',
    GAME_BACKGROUND_BOTTOM: '#2E5FD8',
    GAME_BORDER: '#322CBB',
    INFO_BACKGROUND: '#242C54',
    INFO_BORDER: '#242C54',
    PREVIEW_BACKGROUND: '#000000',
    PREVIEW_BORDER: '#000000',
    WHITE: '#FFFFFF',
    GUIDE_COLOR: 'rgba(255, 255, 255, 0.2)',
    YELLOW: '#FFBB02',
    RED: '#DE4C45'
};

// 테트로미노 블록 정의
const TETROMINOES = {
    'I': {
        shape: [[1, 1, 1, 1]],
        color: '#0099FF'
    },
    'T': {
        shape: [[1, 1, 1],
                [0, 1, 0]],
        color: '#00FF66'
    },
    'Z': {
        shape: [[1, 1, 0],
                [0, 1, 1]],
        color: '#FF0066'
    },
    'S': {
        shape: [[0, 1, 1],
                [1, 1, 0]],
        color: '#9900FF'
    },
    'O': {
        shape: [[1, 1],
                [1, 1]],
        color: '#00CCFF'
    },
    'L': {
        shape: [[1, 1, 1],
                [1, 0, 0]],
        color: '#FF6600'
    },
    'J': {
        shape: [[1, 1, 1],
                [0, 0, 1]],
        color: '#FFFF00'
    }
};

// 게임 상태 상수
const GAME_STATES = {
    PLAYING: 'playing',
    PAUSED: 'paused',
    GAME_OVER: 'game_over',
    LEVEL_TRANSITION: 'level_transition',
    COUNTDOWN: 'countdown',
    COMPLETED: 'completed'
};

// 레벨 설정
const LEVEL_SETTINGS = {
    1: { dropTime: 1000, targetTime: 120 },
    2: { dropTime: 900, targetTime: 110 },
    3: { dropTime: 800, targetTime: 100 },
    4: { dropTime: 700, targetTime: 90 },
    5: { dropTime: 600, targetTime: 80 },
    6: { dropTime: 500, targetTime: 70 },
    7: { dropTime: 400, targetTime: 60 },
    8: { dropTime: 300, targetTime: 50 },
    9: { dropTime: 200, targetTime: 45 },
    10: { dropTime: 100, targetTime: 40 }
};

class Tetris {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // 캔버스 크기 설정
        this.canvas.width = SCREEN_WIDTH;
        this.canvas.height = SCREEN_HEIGHT;
        
        // 게임 초기화
        this.init();
        
        // 키보드 이벤트 리스너 설정
        this.setupControls();
        
        // 게임 루프 시작
        this.gameLoop();
    }

    init() {
        // 게임 상태 초기화
        this.state = GAME_STATES.COUNTDOWN;
        this.grid = Array(GAME_ROWS).fill().map(() => Array(GAME_COLUMNS).fill(COLORS.EMPTY_CELL));
        this.score = 0;
        this.level = 1;
        this.linesCleared = 0;
        
        // 블록 가방 초기화
        this.pieceBag = [];
        this.initPieceBag();
        
        // 현재 블록과 다음 블록 설정
        this.currentPiece = this.getNextPiece();
        this.nextPiece = this.getNextPiece();
        
        // 시간 관련 변수 초기화
        this.lastFallTime = Date.now();
        this.levelStartTime = Date.now();
        this.countdownStart = Date.now();
        
        // 게임 실행 상태
        this.isRunning = true;
        
        // 키 입력 상태
        this.keyStates = {
            left: false,
            right: false,
            down: false
        };
    }

    initPieceBag() {
        const pieces = Object.keys(TETROMINOES);
        this.pieceBag = [...pieces].sort(() => Math.random() - 0.5);
    }

    getNextPiece() {
        if (this.pieceBag.length === 0) {
            this.initPieceBag();
        }
        
        const pieceName = this.pieceBag.pop();
        const piece = TETROMINOES[pieceName];
        
        return {
            shape: JSON.parse(JSON.stringify(piece.shape)),
            color: piece.color,
            x: Math.floor(GAME_COLUMNS / 2) - Math.floor(piece.shape[0].length / 2),
            y: 0
        };
    }

    setupControls() {
        document.addEventListener('keydown', (event) => {
            if (this.state !== GAME_STATES.PLAYING) return;
            
            switch (event.code) {
                case 'ArrowLeft':
                    this.keyStates.left = true;
                    this.movePiece(-1, 0);
                    break;
                case 'ArrowRight':
                    this.keyStates.right = true;
                    this.movePiece(1, 0);
                    break;
                case 'ArrowDown':
                    this.keyStates.down = true;
                    this.movePiece(0, 1);
                    break;
                case 'ArrowUp':
                    this.rotatePiece();
                    break;
            }
        });

        document.addEventListener('keyup', (event) => {
            switch (event.code) {
                case 'ArrowLeft':
                    this.keyStates.left = false;
                    break;
                case 'ArrowRight':
                    this.keyStates.right = false;
                    break;
                case 'ArrowDown':
                    this.keyStates.down = false;
                    break;
            }
        });
    }

    movePiece(dx, dy) {
        if (this.isValidMove(this.currentPiece, dx, dy)) {
            this.currentPiece.x += dx;
            this.currentPiece.y += dy;
            return true;
        }
        return false;
    }

    rotatePiece() {
        const rotated = {
            ...this.currentPiece,
            shape: this.currentPiece.shape[0].map((_, i) =>
                this.currentPiece.shape.map(row => row[i]).reverse()
            )
        };
        
        if (this.isValidMove(rotated, 0, 0)) {
            this.currentPiece = rotated;
        }
    }

    isValidMove(piece, dx, dy) {
        return piece.shape.every((row, y) =>
            row.every((value, x) => {
                if (!value) return true;
                
                const newX = piece.x + x + dx;
                const newY = piece.y + y + dy;
                
                return (
                    newX >= 0 &&
                    newX < GAME_COLUMNS &&
                    newY < GAME_ROWS &&
                    (newY < 0 || this.grid[newY][newX] === COLORS.EMPTY_CELL)
                );
            })
        );
    }

    lockPiece() {
        this.currentPiece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    const gridY = this.currentPiece.y + y;
                    if (gridY >= 0) {
                        this.grid[gridY][this.currentPiece.x + x] = this.currentPiece.color;
                    }
                }
            });
        });

        this.clearLines();
        this.currentPiece = this.nextPiece;
        this.nextPiece = this.getNextPiece();

        if (!this.isValidMove(this.currentPiece, 0, 0)) {
            this.state = GAME_STATES.GAME_OVER;
            this.isRunning = false;
        }
    }

    clearLines() {
        let linesCleared = 0;
        
        for (let y = GAME_ROWS - 1; y >= 0; y--) {
            if (this.grid[y].every(cell => cell !== COLORS.EMPTY_CELL)) {
                this.grid.splice(y, 1);
                this.grid.unshift(Array(GAME_COLUMNS).fill(COLORS.EMPTY_CELL));
                linesCleared++;
                y++;
            }
        }

        if (linesCleared > 0) {
            this.score += linesCleared * 100 * this.level;
            this.linesCleared += linesCleared;
            
            if (this.linesCleared >= 10) {
                this.levelUp();
            }
        }
    }

    levelUp() {
        if (this.level < 10) {
            this.level++;
            this.linesCleared = 0;
            this.state = GAME_STATES.LEVEL_TRANSITION;
            setTimeout(() => {
                this.state = GAME_STATES.PLAYING;
            }, 2000);
        } else {
            this.state = GAME_STATES.COMPLETED;
        }
    }

    drawBlock(x, y, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
        
        // 3D 효과
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE);
    }

    drawPiece(piece) {
        piece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    this.drawBlock(piece.x + x, piece.y + y, piece.color);
                }
            });
        });
    }

    drawGhost() {
        if (this.level === 1) {
            const ghost = {
                ...this.currentPiece,
                y: this.currentPiece.y
            };

            while (this.isValidMove(ghost, 0, 1)) {
                ghost.y++;
            }

            this.ctx.globalAlpha = 0.3;
            this.drawPiece(ghost);
            this.ctx.globalAlpha = 1;
        }
    }

    drawGrid() {
        // 배경 그라데이션
        const gradient = this.ctx.createLinearGradient(0, 0, 0, SCREEN_HEIGHT);
        gradient.addColorStop(0, COLORS.GAME_BACKGROUND_TOP);
        gradient.addColorStop(1, COLORS.GAME_BACKGROUND_BOTTOM);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, GAME_WIDTH, SCREEN_HEIGHT);

        // 그리드 그리기
        this.grid.forEach((row, y) => {
            row.forEach((color, x) => {
                if (color !== COLORS.EMPTY_CELL) {
                    this.drawBlock(x, y, color);
                }
            });
        });
    }

    drawInfo() {
        // 정보 영역 배경
        this.ctx.fillStyle = COLORS.INFO_BACKGROUND;
        this.ctx.fillRect(GAME_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT);

        // 점수와 레벨 표시
        this.ctx.fillStyle = COLORS.WHITE;
        this.ctx.font = '20px Arial';
        this.ctx.fillText(`Level: ${this.level}`, GAME_WIDTH + 20, 30);
        this.ctx.fillText(`Score: ${this.score}`, GAME_WIDTH + 20, 60);

        // 다음 블록 미리보기
        this.ctx.fillStyle = COLORS.PREVIEW_BACKGROUND;
        this.ctx.fillRect(GAME_WIDTH + 20, 80, 110, 110);
        
        const previewX = GAME_WIDTH + 50;
        const previewY = 100;
        
        this.nextPiece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    this.drawBlock(
                        (previewX / GRID_SIZE) + x,
                        (previewY / GRID_SIZE) + y,
                        this.nextPiece.color
                    );
                }
            });
        });
    }

    drawCountdown() {
        if (this.state === GAME_STATES.COUNTDOWN) {
            const elapsed = (Date.now() - this.countdownStart) / 1000;
            const count = 3 - Math.floor(elapsed);
            
            if (count > 0) {
                this.ctx.fillStyle = COLORS.WHITE;
                this.ctx.font = '50px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.fillText(count.toString(), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
                this.ctx.textAlign = 'left';
            } else {
                this.state = GAME_STATES.PLAYING;
            }
        }
    }

    update() {
        const now = Date.now();
        
        if (this.state === GAME_STATES.PLAYING) {
            // 자동 낙하
            if (now - this.lastFallTime > LEVEL_SETTINGS[this.level].dropTime) {
                if (!this.movePiece(0, 1)) {
                    this.lockPiece();
                }
                this.lastFallTime = now;
            }

            // 키 홀딩 처리
            if (this.keyStates.left) this.movePiece(-1, 0);
            if (this.keyStates.right) this.movePiece(1, 0);
            if (this.keyStates.down) this.movePiece(0, 1);
        }
    }

    draw() {
        // 화면 클리어
        this.ctx.fillStyle = COLORS.SCREEN_BACKGROUND;
        this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

        this.drawGrid();
        this.drawGhost();
        this.drawPiece(this.currentPiece);
        this.drawInfo();
        this.drawCountdown();

        // 게임 오버 표시
        if (this.state === GAME_STATES.GAME_OVER) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
            
            this.ctx.fillStyle = COLORS.WHITE;
            this.ctx.font = '40px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('GAME OVER', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
            this.ctx.font = '20px Arial';
            this.ctx.fillText(`Final Score: ${this.score}`, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40);
            this.ctx.textAlign = 'left';
        }
    }

    gameLoop() {
        if (this.isRunning) {
            this.update();
            this.draw();
            requestAnimationFrame(() => this.gameLoop());
        }
    }
}

// 게임 시작
window.onload = () => {
    new Tetris();
}; 