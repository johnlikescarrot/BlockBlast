# BlockBlast (Parchados)

BlockBlast is a browser-based block puzzle game built with the Phaser 3 framework. Players drag and drop geometric pieces onto an 8x8 game board to form complete rows and columns, which are then cleared for points. The game features a time-based mechanic where players must place pieces before a timer expires, along with power-ups like bombs and reducers that add strategic depth to the gameplay.

The project is designed as an embeddable web game that can be integrated into external platforms. It exposes a global `Parchados.run()` API that allows host applications to customize game behavior through callbacks and configuration options, including high score tracking, sponsor integration, and event handling for analytics and gameplay state changes. Score submissions are encrypted using RSA for secure server-side validation.

## Game Initialization API

The main entry point for running the game. Accepts configuration options including callbacks for game events, initial high score, and sponsor/season identifiers for integration with external platforms.

```javascript
// Basic game initialization
window.Parchados.run();

// Advanced initialization with all options
window.Parchados.run({
    highScore: 50000,           // Previous high score to display
    sponsor: true,              // Enable sponsor branding
    seasonId: 12,               // Season identifier for leaderboards
    gameId: 456,                // Game instance identifier
    onGameStart: (evt) => {
        console.log('Game started:', evt);
        // evt contains: { state: 'game_start', name: 'blockblast' }
    },
    onGameEnd: (encryptedData) => {
        // encryptedData is RSA-encrypted JSON containing score and IDs
        console.log('Game ended with encrypted payload');
        fetch('/api/submit-score', {
            method: 'POST',
            body: JSON.stringify({ data: encryptedData })
        });
    },
    onDataSend: (data) => {
        // Custom data handler for analytics
        console.log('Game data:', data);
    }
});
```

## Scene Management System

The game uses Phaser's scene system with four main scenes that handle different game states. BootScene loads initial assets, UIScene manages overlays and audio, MenuScene provides the main menu, and MainScene handles core gameplay.

```javascript
import { BootScene } from "./scripts/scenes/BootScene.js";
import { UIScene } from "./scripts/scenes/UIScene.js";
import { MenuScene } from "./scripts/scenes/MenuScene.js";
import { MainScene } from "./scripts/scenes/MainScene.js";
import WebFontLoaderPlugin from 'phaser3-rex-plugins/plugins/webfontloader-plugin.js';
import UIPlugin from 'phaser3-rex-plugins/templates/ui/ui-plugin.js';

const gameOptions = {
    type: Phaser.AUTO,
    parent: 'phaser-div',
    width: 1080,
    height: 1080,
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
    },
    scene: [BootScene, UIScene, MenuScene, MainScene],
    fps: { target: 60 },
    plugins: {
        global: [{
            key: 'rexWebFontLoader',
            plugin: WebFontLoaderPlugin,
            start: true
        }],
        scene: [{
            key: 'rexUI',
            plugin: UIPlugin,
            mapping: 'rexUI'
        }]
    }
};

const game = new Phaser.Game(gameOptions);
game.config.metadata = {
    highScore: 0,
    sponsor: false,
    seasonId: 0,
    gameId: 0,
    onGameStart: () => {},
    onGameEnd: () => {},
    onDataSend: () => {}
};
```

## Piece Generation and Management

The game generates random tetromino-style pieces from a predefined list of 39 shapes. Pieces are represented as 5x5 binary strings where '1' indicates a filled cell. The piece system supports multiple colors and power-up variants.

```javascript
// Piece shape definitions (5x5 grid as 25-character string)
const PIECE_SHAPES = [
    "0010000100001000010000100",  // Vertical line (5 blocks)
    "0000000100001000010000000",  // Vertical line (3 blocks)
    "0000000000111110000000000",  // Horizontal line (5 blocks)
    "0000001110011100111000000",  // 3x3 square
    "0000001100011000000000000",  // 2x2 square
    "0000000100011100000000000",  // T-shape inverted
    "0000001000010000110000000",  // L-shape
    "0000001000011000010000000",  // S-shape
    "0000001000010000111000000",  // Large L-shape
    // ... 39 total shapes
];

// Color variants for pieces
const colorsList = [
    "blockblast_piece_shadow.png",  // Empty space indicator
    "blockblast_piece_a.png",
    "blockblast_piece_b.png",
    "blockblast_piece_c.png",
    // ... up to 14 color variants
];

// Generate a random piece with random color
function GeneratePiece() {
    let pShape = PIECE_SHAPES[Math.floor(Math.random() * PIECE_SHAPES.length)];
    let pTexture = Math.floor(Math.random() * (colorsList.length - 1)) + 1;
    let chr = String.fromCharCode(97 + pTexture);
    let newPShape = "";

    for (let i = 0; i < 25; i++) {
        newPShape += pShape.charAt(i) === "1" ? chr : "0";
    }

    return { color: colorsList[pTexture], shape: newPShape };
}
```

## Board Placement Validation

Core gameplay logic that validates whether a piece can be placed at a given position on the 8x8 board. Checks for boundary conditions and collision with existing pieces.

```javascript
const PIECE_DIMENSION = 5;

// Check if piece can be placed at position (x, y)
function CanPutPiece(pieceShape, x, y, boardMatrix) {
    for (let i = 0; i < PIECE_DIMENSION; i++) {
        for (let j = 0; j < PIECE_DIMENSION; j++) {
            if (pieceShape.charAt((PIECE_DIMENSION * i) + j) !== '0') {
                // Check bounds
                if (i + y > boardMatrix.length - 1 ||
                    j + x > boardMatrix[0].length - 1 ||
                    i + y < 0 || j + x < 0) {
                    return false;
                }
                // Check collision with existing pieces
                if (boardMatrix[j + x][i + y] !== 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

// Place piece on board and update state
function InsertPiece(piece, x, y, boardMatrix, lineCounterX, lineCounterY) {
    let scorePoints = 0;
    for (let i = 0; i < PIECE_DIMENSION; i++) {
        for (let j = 0; j < PIECE_DIMENSION; j++) {
            if (piece.shape.charAt((PIECE_DIMENSION * i) + j) !== '0') {
                boardMatrix[j + x][i + y] = 1;
                lineCounterX[i + y] += 1;
                lineCounterY[j + x] += 1;
                scorePoints += 10;
            }
        }
    }
    return scorePoints;
}
```

## Line Breaking System

Detects and clears complete rows and columns, calculating combo bonuses based on the number of lines cleared simultaneously.

```javascript
// Check for complete lines after piece placement
function ShowBreakingLines(boardSize, lineCounterX, lineCounterY, lineCounterXadd, lineCounterYadd) {
    const linesToClear = [];

    for (let i = 0; i < boardSize; i++) {
        // Check horizontal lines (rows)
        if (lineCounterXadd[i] + lineCounterX[i] === boardSize) {
            linesToClear.push(i);
        }
        // Check vertical lines (columns, offset by 8)
        if (lineCounterYadd[i] + lineCounterY[i] === boardSize) {
            linesToClear.push(i + 8);
        }
    }
    return linesToClear;
}

// Calculate combo bonus (triangular number formula)
function CalculateComboBonus(linesCleared) {
    let bonus = 0;
    for (let i = 1; i <= linesCleared; i++) {
        bonus += i;
    }
    return bonus * 1000;  // 1 line = 1000, 2 lines = 3000, 3 lines = 6000
}

// Example usage
const lines = [0, 3, 10];  // Row 0, Row 3, Column 2 (10-8=2)
const comboBonus = CalculateComboBonus(3);  // Returns 6000
```

## Power-Up System

Three power-up types can appear on pieces: Bomb (destroys surrounding cells), Reducer (converts remaining pieces to 1x1 squares), and Rotate (rotates the board).

```javascript
// Power-up types
const powerUpsList = ["bomb", "reduct", "rotate"];

// Bomb power-up: destroys 3x3 area around activation point
function BombBreakingLines(fila, columna, boardMatrix) {
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            const nuevaFila = fila + i;
            const nuevaColumna = columna + j;

            if (nuevaFila >= 0 && nuevaFila < 8 &&
                nuevaColumna >= 0 && nuevaColumna < 8) {
                if (!(i === 0 && j === 0)) {  // Skip center
                    boardMatrix[nuevaFila][nuevaColumna] = 0;
                }
            }
        }
    }
}

// Reducer power-up: convert remaining pieces to 1x1 squares
function ConverterPowerUp(optionsBools, optionsPieces) {
    const singleSquareShape = "0000000000001000000000000";

    for (let k = 0; k < 3; k++) {
        if (optionsBools[k]) {
            optionsPieces[k] = {
                color: optionsPieces[k].color,
                shape: singleSquareShape
            };
        }
    }
}

// Convert piece to include random power-up
function convertirPowerUp(shape) {
    let array = shape.split('');
    let posiciones_1 = array.map((c, i) => c !== '0' ? i : -1).filter(i => i >= 0);

    if (posiciones_1.length === 0) return shape;

    let posicion_aleatoria = posiciones_1[Math.floor(Math.random() * posiciones_1.length)];
    let powerUpType = Math.floor(Math.random() * 2) + 1;  // 1=bomb, 2=reduct
    array[posicion_aleatoria] = powerUpType;

    return array.join('');
}
```

## Audio Manager

Centralized audio system handling background music and sound effects with volume control and focus handling.

```javascript
import { AudioManager } from './scripts/components/audioManager.js';

// Initialize audio manager in UIScene
const audioManager = new AudioManager(scene);
audioManager.load();
audioManager.init();

// Available sound effects
const sfxKeys = [
    'alarma',      // Timer warning
    'destruccion', // Line destruction
    'preview',     // Piece pickup
    'soltar',      // Piece placement
    'aviso',       // Power-up warning
    'bomba',       // Bomb explosion
    'reduccion',   // Reducer activation
    'puntos',      // Points scored
    'tapete',      // Game over mat
    'ui_click',    // UI button click
    'ui_page'      // Page turn
];

// Control audio playback
audioManager.menuMusic.play();
audioManager.gameplayMusic.play();
audioManager.setAudioVolume(0.5);  // 0 to 1 range
audioManager.pauseMusic();
audioManager.resumeMusic();

// Play sound effects
audioManager.bomba.play();
audioManager.destruccion.play();
audioManager.ui_click.play();
```

## Panel UI System

Modal panel system for displaying pause menu, options, credits, game over screen, and tutorial pages.

```javascript
import { Panel } from './scripts/components/panel.js';

// Create and show UI panels
const panel = new Panel(scene);
panel.create(1080);
panel.createPausePanel(1080);
panel.createOptionsPanel(1080);
panel.createCreditsPanel(1080);
panel.createScorePanel(1080);
panel.createInstructionsPanel(1080);
panel.createReloadPanel(1080);

// Show/hide panels with animations
panel.showPause();
panel.hidePause();

panel.showOptions();
panel.hideOptions();

panel.showCredits();
panel.hideCredits();

panel.showInstructions(() => {
    console.log('Tutorial closed');
});
panel.hideInstructions();

// Display game over score
const finalScore = 150000;
const highScore = 200000;
panel.showScore(finalScore, highScore);
panel.hideScore();

panel.showReload();
panel.hideReload();
```

## Internationalization (i18n) System

Multi-language support system that manages translations and persists language preferences to localStorage.

```javascript
import { I18nManager, SUPPORTED_LOCALES } from './scripts/components/i18n.js';

// Supported languages
console.log(SUPPORTED_LOCALES);  // ["en", "es"]

// Initialize i18n manager
const i18n = new I18nManager(scene);
i18n.init();

// Get current language
console.log(i18n.language);  // "en" or "es"

// Set language (persisted to localStorage)
i18n.setLanguage('es');

// Translate keys
const pauseText = i18n.t('PAUSE');           // "PAUSA" in Spanish
const scoreText = i18n.t('SCORE');           // "PUNTUACION" in Spanish
const tutorialText = i18n.t('TUTORIAL');     // "TUTORIAL"
const gameOverText = i18n.t('GAME_OVER');    // "FIN DE PARTIDA" in Spanish

// Available translation keys
const translationKeys = [
    'SCORE', 'PAUSE', 'OPTIONS', 'CREDITS', 'TUTORIAL',
    'GAME_OVER', 'TIME', 'RECORD', 'MUSIC', 'SOUND',
    'FULLSCREEN', 'LANGUAGE', 'RESTART', 'ARE_YOU_SURE_RESTART',
    'PROGRAMMING', 'ART_ANIMATION', 'MARKETING_UI',
    'MUSIC_SOUND', 'DIRECTION', 'EXECUTIVE_PRODUCER',
    'TUTORIAL_PAGE_1_TEXT_1', 'TUTORIAL_PAGE_1_TEXT_2',
    'TUTORIAL_PAGE_2_TEXT_1', 'TUTORIAL_PAGE_2_TEXT_2',
    'TUTORIAL_PAGE_3_TEXT_1'
];
```

## Resource Loader Configuration

Static utility class for managing asset paths between development and production environments.

```javascript
import { ResourceLoader } from './scripts/components/resourceLoader.js';

// ResourceLoader automatically detects environment
class ResourceLoader {
    static isProd = process.env.NODE_ENV === 'production';
    static supportedLocales = new Set(['en', 'es']);

    static ReturnPath() {
        // Returns CDN route for production assets
        return 'https://static.pchujoy.com/public/games-assets/parchados';
    }

    static ReturnLocalePath(lang) {
        const safeLang = this.supportedLocales.has(lang) ? lang : 'en';
        return `./scripts/locales/${safeLang}.json`;
    }
}

// Usage in asset loading (BootScene/MainScene)
this.load.image('table', ResourceLoader.ReturnPath() + '/images/parchados_chess.png');

this.load.atlas('piece',
    ResourceLoader.ReturnPath() + '/images/blockblast_piece/sprites.png',
    ResourceLoader.ReturnPath() + '/images/blockblast_piece/sprites.json'
);

this.load.audio('mainTheme', [
    ResourceLoader.ReturnPath() + '/audios/title.ogg',
    ResourceLoader.ReturnPath() + '/audios/title.m4a'
]);

// Load locale files
SUPPORTED_LOCALES.forEach(locale => {
    this.load.json(`locale_${locale}`, ResourceLoader.ReturnLocalePath(locale));
});
```

## Timer System

Time-based gameplay mechanic that decreases available time as the game progresses, creating increasing difficulty.

```javascript
// Timer configuration
const minTimePerTurn = 5;      // Minimum seconds per turn
const maxTimePerTurn = 25;     // Starting seconds per turn

// Create timer slider using rexUI plugin
const timeSlider = scene.rexUI.add.slider({
    x: centerX,
    y: centerY,
    width: 700,
    height: 50,
    orientation: 'x',
    value: 1,
    track: scene.add.sprite(0, 0, 'timerBar', 'Delineado cronometro.png'),
    indicator: scene.add.sprite(0, 0, 'timerBar', 'verde.png'),
    thumb: scene.add.sprite(0, 0, 'timerBar', 'Reloj.png'),
    input: 'none'
}).layout();

// Animate timer countdown
const sliderTween = scene.tweens.add({
    targets: timeSlider,
    duration: maxTimePerTurn * 1000,
    value: { getStart: () => 1, getEnd: () => 0 },
    onUpdate: (tween, target) => {
        let value = target.value;
        let indicator = target.getElement('indicator');

        // Update indicator width
        let indicatorWidth = value * 600;
        indicator.resize(indicatorWidth, 40);

        if (value <= 0.3) {
            // Flash warning colors
            indicator.setFrame('rojo.png');
            audioManager.alarma.play();
        }
    },
    onComplete: () => {
        console.log('Time expired!');
        StartGameOver();
    }
});
```

## Drag and Drop Interaction

Touch and mouse input handling for piece placement with visual preview feedback.

```javascript
// Enable drag on piece containers
scene.input.on('dragstart', function(pointer, gameObject) {
    if (!isPaused) {
        audioManager.preview.play();
        gameObject.parentContainer.visible = false;
        currentPiece = optionsPieces[parseInt(gameObject.parentContainer.name)];
        pointerContainer.visible = true;
        canCheck = true;
    }
});

scene.input.on('drag', (pointer, gameObject, dragX, dragY) => {
    if (!isPaused) {
        pointerContainer.x = pointer.worldX - 2 * squareSize;
        pointerContainer.y = pointer.worldY - 2 * squareSize;
    }
});

scene.input.on('dragend', function(pointer, gameObject) {
    if (!isPaused) {
        canCheck = false;
        pointerContainer.visible = false;

        if (CanPutPiece(currentPiece.shape, pointerX, pointerY, boardMatrix)) {
            InsertPiece(currentPiece, pointerX, pointerY);
            // Screen shake for feedback
            cameras.main.shake(100, 0.002);
        } else {
            // Return piece to original position
            gameObject.parentContainer.visible = true;
            optionsBools[parseInt(gameObject.parentContainer.name)] = true;
        }
    }
});
```

## Development and Build Commands

Commands for running the development server and building for production.

```bash
# Install dependencies
npm install

# Start development server with hot reload
npm start

# Build for production (outputs to dist/ folder)
npm run build
```

## Summary

BlockBlast is designed as a modular, embeddable puzzle game that integrates seamlessly with external gaming platforms. The main use cases include embedding the game in web portals with custom event tracking, implementing leaderboard systems through the encrypted score submission API, and white-labeling with sponsor branding. The game tracks session data including scores, gameplay duration, and high scores, which are securely transmitted using RSA encryption.

Integration patterns follow a callback-based architecture where the host application provides handlers for game lifecycle events. The `onGameStart` callback receives game state information for analytics initialization, while `onGameEnd` receives encrypted score payloads for secure server-side validation. The game's responsive scaling (1080x1080 with FIT mode) ensures consistent display across devices, and the audio system includes automatic pause-on-blur handling for a polished user experience. The internationalization system supports English and Spanish with localStorage persistence, making the game accessible to a wider audience.
