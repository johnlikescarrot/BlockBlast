    BreakLine(x, y) {
        if (this.linesToClear.length < 1 || this.gamefinish) {
            this.FinishTurn();
            return;
        }
        if (this.animationsIterator === 0) {
            this.PauseTimer();
            // Scaling shake and flash exponentially for TRANSCENDENT impact
            let intensity = Math.pow(this.linesToClear.length, 1.5) * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE;
            let flashDuration = JUICE_CONFIG.FLASH_DURATION * (1 + this.linesToClear.length * 0.2);
            this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);
            this.cameras.main.flash(flashDuration, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);
        }
