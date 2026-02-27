const UI_CONFIG = {
    SHOW_DURATION: 450,
    HIDE_DURATION: 300,
    BLUR_QUALITY: 1,
    BLUR_X: 1,
    BLUR_Y: 1,
    BLUR_STRENGTH: 2
};
export class Panel {
    constructor(scene) {
        this.scene = scene;
        this.updateCredits();
        this._hideInstructionsCallback = null;
        this.blurFX = null;
    }
    animateShow(container) {
        container.setVisible(true);
        container.setScale(0.8);
        container.setAlpha(0);
        this.scene.tweens.add({
            targets: container,
            alpha: { value: 1, ease: "Sine.easeOut" },
            scale: { value: 1, ease: "Elastic.easeOut", easeParams: [1, 0.5] },
            duration: UI_CONFIG.SHOW_DURATION
        });
        if (this.scene.currentScene && !this.blurFX) {
            this.blurFX = this.scene.currentScene.cameras.main.postFX?.addBlur?.(UI_CONFIG.BLUR_QUALITY, UI_CONFIG.BLUR_X, UI_CONFIG.BLUR_Y, UI_CONFIG.BLUR_STRENGTH);
        }
    }
    animateHide(container, onComplete) {
        this.scene.tweens.add({
            targets: container,
            alpha: { value: 0, ease: "Sine.easeIn" },
            scale: { value: 0, ease: "Back.easeIn" },
            duration: UI_CONFIG.HIDE_DURATION,
            onComplete: () => {
                container.setVisible(false);
                if (this.blurFX) {
                    this.scene.currentScene?.cameras?.main?.postFX?.remove?.(this.blurFX);
                    this.blurFX = null;
                }
                if (onComplete) onComplete();
            }
        });
    }
    updateCredits() {
        this.credits = [
            [this.scene.i18n.t('PROGRAMMING'), 'Diego Johnson', 'Braulio Baldeon'],
            [this.scene.i18n.t('ART_ANIMATION'), 'Edward Torres'],
            [this.scene.i18n.t('MARKETING_UI'), 'Karoline Jimenez'],
            [this.scene.i18n.t('MUSIC_SOUND'), 'Gunter Brenner'],
            [this.scene.i18n.t('DIRECTION'), 'Jorge García'],
            [this.scene.i18n.t('EXECUTIVE_PRODUCER'), 'Phillip Chu Joy']
        ];
    }

    create(dim) {
        let background = this.scene.add.image(dim / 2, dim / 2, 'fade').setDisplaySize(dim, dim).setInteractive();
        let background2 = this.scene.add.image(dim / 2, dim / 2, 'fade').setDisplaySize(dim, dim).setInteractive();
        this.panel = this.scene.add.image(dim / 2, dim / 2, 'panel').setScale(1);

        this.panelContainer = this.scene.add.container(0, 0, [background, this.panel]);
        this.panelContainer.setDepth(10).setVisible(false);

        this.reloadPanel = this.scene.add.image(dim / 2, dim / 2, 'panel').setScale(.7);
        this.reloadPanelContainer = this.scene.add.container(0, 0, [background2, this.reloadPanel]);
        this.reloadPanelContainer.setDepth(10).setVisible(false);
    }

    createPausePanel(dim) {
        let pauseTitle = this.scene.add.text(dim / 2, 318, this.scene.i18n.t('PAUSE'), {
            fontFamily: 'Bungee', fontSize: '34px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        pauseTitle.setStroke('#503530', 10);
        let closeImage = this.scene.add.image(dim - 190, 315, 'menuUI', 'Equis_NonClicked.png').setInteractive().setScale(.5);
        closeImage.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.scene.audioManager.resumeMusic();
            this.scene.currentScene.PauseGame();
        });

        let optionsButton = this.scene.add.image(dim / 2, dim / 2 - 80, 'pantalla_pausa_UI', 'Botón_opciones_NonClicked.png').setInteractive().setDisplaySize(400, 75);
        optionsButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hidePause(() => {
                this.showOptions();
            });
        });

        let continueButton = this.scene.add.image(dim / 2, dim / 2 + 25, 'pantalla_pausa_UI', 'Botón_Continuar_NonClicked.png').setInteractive().setDisplaySize(400, 75);
        continueButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.scene.audioManager.resumeMusic();
            this.scene.currentScene.PauseGame();
        });

        let exitButton = this.scene.add.image(dim / 2, dim / 2 + 130, 'pantalla_pausa_UI', 'Botón_Salir_NonClicked.png').setInteractive().setDisplaySize(400, 75);
        exitButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hidePause();
            this.scene.currentScene.BackMenu();
        });

        this.pauseContainer = this.scene.add.container(0, 0, [pauseTitle, closeImage, continueButton, optionsButton, exitButton]);
        this.pauseContainer.setVisible(false).setDepth(10.1);
    }

    createReloadPanel(dim) {
        let reloadTitle = this.scene.add.text(dim / 2, 390, this.scene.i18n.t('RESTART'), {
            fontFamily: 'Bungee', fontSize: '30px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        reloadTitle.setStroke('#503530', 10);
        let closeImage = this.scene.add.image(dim - 290, 380, 'menuUI', 'Equis_NonClicked.png').setInteractive().setScale(.5);
        closeImage.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideReload();
        });

        let text2 = this.scene.add.text(dim / 2, dim / 2 - 40, this.scene.i18n.t('ARE_YOU_SURE_RESTART'), {
            fontFamily: 'Bungee', fontSize: '30px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text2.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.reloadPanel.displayWidth - 100);

        let reloadButton = this.scene.add.image(dim / 2, dim / 2 + 90, 'pantalla_fin_UI', 'Botón_Reiniciar_NonClicked.png').setInteractive().setScale(1);
        reloadButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideReload();
            this.scene.currentScene.RestartGame();
        });

        this.reloadContainer = this.scene.add.container(0, 0, [reloadTitle, closeImage, text2, reloadButton]);
        this.reloadContainer.setVisible(false).setDepth(10.1);
    }

    createFirstTutorialPage(dim) {
        let text1 = this.scene.add.text(dim / 2, 440, this.scene.i18n.t('TUTORIAL_PAGE_1_TEXT_1'), {
            fontFamily: 'Bungee', fontSize: '20px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text1.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.panel.displayWidth - 100);

        let image1 = this.scene.add.image(dim / 2, 550, 'tutorial', 'linecomplete.png').setScale(.5);

        let text2 = this.scene.add.text(dim / 2, dim / 2 + 120, this.scene.i18n.t('TUTORIAL_PAGE_1_TEXT_2'), {
            fontFamily: 'Bungee', fontSize: '20px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text2.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.panel.displayWidth - 100);

        let image2 = this.scene.add.image(dim / 2, dim / 2 + 200, 'tutorial', 'timer.png').setScale(.5);

        const textContainer1 = this.scene.add.container(0, 0, [text1, image1, image2, text2]).setVisible(false);
        return textContainer1;
    }

    createSecondTutorialPage(dim) {
        let text1 = this.scene.add.text(dim / 2, 440, this.scene.i18n.t('TUTORIAL_PAGE_2_TEXT_1'), {
            fontFamily: 'Bungee', fontSize: '20px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text1.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.panel.displayWidth - 100);

        let image1 = this.scene.add.image(dim / 2 - 200 - 60, 580, 'tutorial', 'bomb.png').setScale(1);
        let image2 = this.scene.add.image(dim / 2 + 50 - 80, 570, 'tutorial', 'bombprep.png').setScale(.4);
        let image3 = this.scene.add.image(dim / 2 + 300 - 80, 580, 'tutorial', 'bombexplode.png').setScale(.4);

        let text2 = this.scene.add.text(dim / 2, dim / 2 + 150, this.scene.i18n.t('TUTORIAL_PAGE_2_TEXT_2'), {
            fontFamily: 'Bungee', fontSize: '20px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text2.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.panel.displayWidth - 100);

        const textContainer2 = this.scene.add.container(0, 0, [text1, image1, image2, image3, text2]).setVisible(false);
        return textContainer2;
    }

    createThirdTutorialPage(dim) {
        let text1 = this.scene.add.text(dim / 2, 440, this.scene.i18n.t('TUTORIAL_PAGE_3_TEXT_1'), {
            fontFamily: 'Bungee', fontSize: '20px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        text1.setStroke('#503530', 8).setLineSpacing(0).setWordWrapWidth(this.panel.displayWidth - 100);

        let image4 = this.scene.add.image(dim / 2 - 200 - 60, 580, 'tutorial', 'reduct.png').setScale(1);
        let image5 = this.scene.add.image(dim / 2 + 50 - 80, 570, 'tutorial', 'reductprep.png').setScale(.4);
        let image6 = this.scene.add.image(dim / 2 + 300 - 80, 580, 'tutorial', 'reductworks.png').setScale(.4);

        const textContainer3 = this.scene.add.container(0, 0, [text1, image4, image5, image6]).setVisible(false);
        return textContainer3;
    }

    createInstructionsPanel(dim) {
        this.instructionIndex = 0;
        this.instructionTexts = [this.createFirstTutorialPage(dim), this.createSecondTutorialPage(dim), this.createThirdTutorialPage(dim)];

        this.instructionsTitle = this.scene.add.text(dim / 2, 318, this.scene.i18n.t('TUTORIAL'), {
            fontFamily: 'Bungee', fontSize: '34px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        this.instructionsTitle.setStroke('#503530', 10);
        let closeImage = this.scene.add.image(dim - 190, 315, 'menuUI', 'Equis_NonClicked.png').setInteractive().setScale(.5);
        closeImage.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideInstructions();
            if (this.scene.currentScene.scene.key === 'MainScene') this.scene.currentScene.CloseInstructions();
        });

        this.leftArrow = this.scene.add.image(dim / 2 - 55, dim - 260, 'menuUI', 'Previous_NonClicked.png').setInteractive().setDisplaySize(100, 100);
        this.leftArrow.on('pointerdown', () => this.leftArrowClicked());

        this.rightArrow = this.scene.add.image(dim / 2 + 55, dim - 260, 'menuUI', 'Next_NonClicked.png').setInteractive().setDisplaySize(100, 100);
        this.rightArrow.on('pointerdown', () => this.rightArrowClicked());

        this.instructionsContainer = this.scene.add.container(0, 0,
            [this.instructionsTitle, closeImage, this.instructionTexts[0], this.instructionTexts[1], this.instructionTexts[2], this.leftArrow, this.rightArrow]);
        this.instructionsContainer.setVisible(false).setDepth(10.1);
    }

    createOptionsPanel(dim) {
        let optionsTitle = this.scene.add.text(dim / 2, 318, this.scene.i18n.t('OPTIONS'), {
            fontFamily: 'Bungee', fontSize: '34px', color: '#dddddd', align: 'center'
        }).setOrigin(0.5);
        optionsTitle.setStroke('#503530', 10);

        let closeImage = this.scene.add.image(dim - 190, 315, 'menuUI', 'Equis_NonClicked.png').setInteractive().setScale(.5);
        closeImage.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideOptions();
        });

        let musicTitle = this.scene.add.text(dim / 2 - 200, dim / 2 - 65, this.scene.i18n.t('MUSIC'), {
            font: '800 34px Bungee', color: '#ebebeb', align: 'center'
        }).setOrigin(0.5);
        musicTitle.setStroke('#503530', 8);

        let musicSlider = this.scene.rexUI.add.slider({
            x: dim / 2 + 115,
            y: dim / 2 - 65,
            width: 370,
            height: 30,
            orientation: 'x',
            value: this.scene.data.get('musicVolume'),
            track: this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Barra_vacia.png'),
            indicator: this.addCropResizeMethod(this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Barra_llena.png').setDisplaySize(350, 35)),
            thumb: this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Button1_NonClicked.png').setDisplaySize(35, 60),
            input: 'drag',
            valuechangeCallback: function (value) {
                this.scene.audioManager.menuMusic.volume = value;
                this.scene.audioManager.gameplayMusic.volume = value;
                this.scene.data.set('musicVolume', value);
            },
        }).layout();

        let sfxTitle = this.scene.add.text(dim / 2 - 200, dim / 2 + 25, this.scene.i18n.t('SOUND'), {
            font: '800 34px Bungee', color: '#ebebeb', align: 'center'
        }).setOrigin(0.5);
        sfxTitle.setStroke('#503530', 8);

        let sfxSlider = this.scene.rexUI.add.slider({
            x: dim / 2 + 115,
            y: dim / 2 + 25,
            width: 370,
            height: 30,
            orientation: 'x',
            value: this.scene.data.get('sfxVolume'),
            track: this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Barra_vacia.png'),
            indicator: this.addCropResizeMethod(this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Barra_llena.png').setDisplaySize(350, 35)),
            thumb: this.scene.add.sprite(0, 0, 'pantalla_opciones_UI', 'Button1_NonClicked.png').setDisplaySize(35, 60),
            input: 'drag',
            valuechangeCallback: function (value) {
                this.scene.audioManager.updateSFXVolume(value);
                this.scene.data.set('sfxVolume', value);
            },
        }).layout();

        // Language Controls
        let langTitle = this.scene.add.text(dim / 2 - 200, dim / 2 + 215, this.scene.i18n.t('LANGUAGE'), {
            font: '800 34px Bungee', color: '#ebebeb', align: 'center'
        }).setOrigin(0.5);
        langTitle.setStroke('#503530', 8);

        const activeColor = '#f0dfa7';
        const inactiveColor = '#ebebeb';

        let enButton = this.scene.add.text(dim / 2 + 50, dim / 2 + 215, 'EN', {
            font: '800 34px Bungee', color: this.scene.i18n.language === 'en' ? activeColor : inactiveColor, align: 'center'
        }).setOrigin(0.5).setInteractive();
        enButton.setStroke('#503530', 8);

        let esButton = this.scene.add.text(dim / 2 + 150, dim / 2 + 215, 'ES', {
            font: '800 34px Bungee', color: this.scene.i18n.language === 'es' ? activeColor : inactiveColor, align: 'center'
        }).setOrigin(0.5).setInteractive();
        esButton.setStroke('#503530', 8);

        const langHandler = (lang) => {
            if (this.scene.i18n.language !== lang) {
                this.scene.i18n.setLanguage(lang);
                this.scene.audioManager.ui_click.play();
                this.scene.scene.restart();
            }
        };

        enButton.on('pointerdown', () => langHandler('en'));
        esButton.on('pointerdown', () => langHandler('es'));

        if ((/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream)) {
            musicTitle.setPosition(dim / 2 - 215, dim / 2 - 55);
            musicSlider.setPosition(dim / 2 + 100, dim / 2 - 55);
            sfxTitle.setPosition(dim / 2 - 215, dim / 2 + 65);
            sfxSlider.setPosition(dim / 2 + 100, dim / 2 + 75);
            this.optionsContainer = this.scene.add.container(0, 0,
                [optionsTitle, closeImage, langTitle, enButton, esButton, sfxSlider, sfxTitle, musicTitle, musicSlider]);
        }
        else {
            let fullscreenTitle = this.scene.add.text(dim / 2 - 75, dim / 2 + 125, this.scene.i18n.t('FULLSCREEN'), {
                font: '800 34px Bungee', color: '#ebebeb', align: 'center'
            }).setOrigin(0.5);
            fullscreenTitle.setStroke('#503530', 8);
            this.fullscreenToggleBall = this.scene.add.image(dim / 2 + 205, dim / 2 + 120, 'pantalla_opciones_UI', 'Button2_clicked.png');
            this.fullscreenToggleContainer = this.scene.add.image(dim / 2 + 230, dim / 2 + 120, 'pantalla_opciones_UI', 'Switch_Off.png').setInteractive();
            this.fullscreenToggleContainer.on('pointerdown', () => {
                this.scene.audioManager.ui_click.play();
                this.toggle(this.fullscreenToggleBall, this.fullscreenToggleContainer, dim / 2);
            });
            this.setToggleFullscreen(this.scene.scale.isFullscreen, dim / 2);

            this.optionsContainer = this.scene.add.container(0, 0,
                [optionsTitle, closeImage, sfxSlider, sfxTitle, musicTitle, musicSlider, fullscreenTitle, this.fullscreenToggleContainer, this.fullscreenToggleBall, langTitle, enButton, esButton]);
        }

        this.optionsContainer.setVisible(false).setDepth(10.1);
    }

    createCreditsPanel(dim) {
        let creditsTitleContainer = this.scene.add.image(dim / 2, 535, 'panel').setDisplaySize(800, 700);

        let creditsTitle = this.scene.add.text(dim / 2, 245, this.scene.i18n.t('CREDITS'), {
            font: '700 40px Bungee', color: '#F9F9F9', align: 'center'
        }).setOrigin(0.5);
        creditsTitle.setStroke('#662C2A', 11);

        let closeImage = this.scene.add.image(dim - 150, 245, 'menuUI', 'Equis_NonClicked.png').setInteractive().setScale(.5);
        closeImage.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideCredits();
        });

        this.creditsContainer = this.scene.add.container(0, 0, [creditsTitleContainer, creditsTitle, closeImage]);

        const numCols = 2;
        const itemsPerCol = Math.ceil(this.credits.length / numCols);
        const baseX = dim / 2 - 300;
        const baseY = 350;
        const colOffset = 350;
        const rowSpacing = 140;

        for (let i = 0; i < this.credits.length; i++) {
            const col = Math.floor(i / itemsPerCol);
            const row = i % itemsPerCol;
            const x = baseX + col * colOffset;
            const y = baseY + row * rowSpacing;
            let label = this.addCreditsLabel(x, y, i);
            this.creditsContainer.add(label);
        }

        let logo = this.scene.add.image(dim / 2, dim - 300, 'leapLogo').setScale(1);
        this.creditsContainer.add(logo);
        this.creditsContainer.setVisible(false).setDepth(10.1);
    }

    addCreditsLabel(x, y, index) {
        let title = this.scene.add.text(x + 25, y + 10, this.credits[index][0], {
            fontFamily: 'Bungee', fontSize: '18px', color: '#ebebeb', align: 'left'
        });
        let creditBar = this.scene.add.image(x, y, 'pantalla_pausa_UI', 'Barra.png').setOrigin(0, 0).setDisplaySize(title.getBounds().width + 50, 50).setDepth(10);
        title.setStroke('#662C2A', 5).setDepth(11);

        let names = [];
        for (let i = 1; i < this.credits[index].length; i++) {
            let name = this.scene.add.text(x, (30 * i) + y + 30, this.credits[index][i], {
                font: '700 16px Bungee', color: '#ebebeb', align: 'left'
            });
            name.setStroke('#854A3A', 5);
            names.push(name);
        }

        let labelContainer = this.scene.add.container(0, 0, [creditBar, title]);
        for (let i = 0; i < names.length; i++) { labelContainer.add(names[i]); }
        labelContainer.setDepth(10);
        return labelContainer;
    }

    createScorePanel(dim) {
        let scoreTitle = this.scene.add.text(dim / 2, 318, this.scene.i18n.t('GAME_OVER'), {
            fontFamily: 'Bungee', fontSize: '34px', color: '#f4f4f4', align: 'center'
        }).setOrigin(0.5);
        scoreTitle.setStroke('#553b37', 8);

        let scoreImage = this.scene.add.image(dim / 2, dim / 2 - 70, 'pantalla_fin_UI', 'Contador_puntaje.png').setScale(1);

        this.scoreDisplay = this.scene.add.text(dim / 2, dim / 2 - 60, '0', { font: '800 30px Bungee', color: '#f0dfa7' });
        this.scoreDisplay.setStroke('#3f2e29', 10).setOrigin(.5);

        let timeLabel = this.scene.add.text(dim / 2 - 165, dim / 2 + 30, this.scene.i18n.t('TIME'), { font: '800 30px Bungee', color: '#f4f4f4' });
        timeLabel.setStroke('#553b37', 8);

        this.timeText = this.scene.add.text(dim / 2 + 170, dim / 2 + 70, '00:00:00', { font: '800 30px Bungee', color: '#f0dfa7' });
        this.timeText.setStroke('#553b37', 8).setOrigin(1);

        let recordLabel = this.scene.add.text(dim / 2 - 165, dim / 2 + 95, this.scene.i18n.t('RECORD'), { font: '800 30px Bungee', color: '#f4f4f4' });
        recordLabel.setStroke('#553b37', 8);

        this.recordText = this.scene.add.text(dim / 2 + 170, dim / 2 + 130, '0', { font: '800 30px Bungee', color: '#f0dfa7' });
        this.recordText.setStroke('#553b37', 8).setOrigin(1);

        let restartButton = this.scene.add.image(dim / 2 - 150, dim / 2 + 260, 'pantalla_fin_UI', 'Botón_Reiniciar_NonClicked.png').setInteractive();
        restartButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideScore();
            this.scene.currentScene.RestartGame();
        });

        let menuButton = this.scene.add.image(dim / 2 + 170, dim / 2 + 260, 'pantalla_fin_UI', 'Botón_Salir_NonClicked.png').setInteractive();
        menuButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hideScore();
            this.scene.currentScene.BackMenu();
        });

        this.scoreContainer = this.scene.add.container(0, 0,
            [scoreTitle, scoreImage, this.scoreDisplay, timeLabel, this.timeText, recordLabel, this.recordText, restartButton, menuButton]);
        this.scoreContainer.setVisible(false).setDepth(10.1);
    }

    addCropResizeMethod = function (gameObject) {
        gameObject.resize = function (width, height) {
            gameObject.setCrop(0, 0, width, height);
            return gameObject;
        };
        return gameObject;
    };

    toggle(target, container, center) {
        let start = center + 205;
        let end = center + 255;
        if (target.x != start) {
            start = center + 255;
            end = center + 205;
        }
        let toggleTween = this.scene.tweens.add({
            targets: target,
            ease: 'sine.inout',
            duration: 250,
            repeat: 0,
            x: {
                getStart: () => start,
                getEnd: () => end
            },
            onComplete: () => {
                if (start == center + 205) {
                    container.setTexture('pantalla_opciones_UI', 'Switch_On.png');
                    target.setTexture('pantalla_opciones_UI', 'Button2_NonClicked.png');
                    this.scene.scale.startFullscreen();
                } else {
                    container.setTexture('pantalla_opciones_UI', 'Switch_Off.png');
                    target.setTexture('pantalla_opciones_UI', 'Button2_clicked.png');
                    this.scene.scale.stopFullscreen();
                }
                toggleTween?.remove();
                toggleTween = null;
            }
        });
    }

    setToggleFullscreen(isFullscreen, center) {
        if (!(/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream)) {
            if (isFullscreen) {
                this.fullscreenToggleContainer.setTexture('pantalla_opciones_UI', 'Switch_On.png');
                this.fullscreenToggleBall.setTexture('pantalla_opciones_UI', 'Button2_NonClicked.png').setPosition(center + 255, this.fullscreenToggleBall.y);
            }
            else {
                this.fullscreenToggleContainer.setTexture('pantalla_opciones_UI', 'Switch_Off.png');
                this.fullscreenToggleBall.setTexture('pantalla_opciones_UI', 'Button2_clicked.png').setPosition(center + 205, this.fullscreenToggleBall.y);
            }
        }
    }

    leftArrowClicked() {
        this.scene.audioManager.ui_page.play();
        this.instructionIndex = this.instructionIndex - 1 >= 0 ? this.instructionIndex - 1 : 0;
        this.setInstructionsText();
    }

    rightArrowClicked() {
        this.scene.audioManager.ui_page.play();
        if (this.instructionIndex + 1 < this.instructionTexts.length) {
            this.instructionIndex = this.instructionIndex + 1;
            this.setInstructionsText();
        } else {
            this.hideInstructions();
        }
    }

    setInstructionsText() {
        for (let i = 0; i < this.instructionTexts.length; i++) {
            this.instructionTexts[i].setVisible(false);
        }
        if (this.instructionIndex != 0) {
            this.leftArrow.setVisible(true);
        } else {
            this.leftArrow.setVisible(false);
        }

        if (this.instructionIndex != this.instructionTexts.length - 1) {
            this.rightArrow.setTexture('menuUI', 'Next_NonClicked.png');
        } else {
            this.rightArrow.setTexture('menuUI', 'Equis_NonClicked.png');
        }
        this.instructionTexts[this.instructionIndex].setVisible(true);
        this.instructionsTitle.setText(this.scene.i18n.t('TUTORIAL') + ' ' + (this.instructionIndex + 1) + '/' + this.instructionTexts.length);
    }

    showInstructions(callback) {
        this.instructionIndex = 0;
        this.setInstructionsText();
        this._hideInstructionsCallback = callback || null;
        this.scene.audioManager.ui_page.play();
        this.animateShow(this.instructionsContainer);
        this.panelContainer.setVisible(true);
    }

    hideInstructions() {
        this.animateHide(this.instructionsContainer, () => {
            this.panelContainer.setVisible(false);
            if (this._hideInstructionsCallback) {
                const cb = this._hideInstructionsCallback;
                this._hideInstructionsCallback = null;
                cb();
            }
        });
    }

    showOptions() {
        this.animateShow(this.optionsContainer);
        this.panelContainer.setVisible(true);
        if (this.scene.currentScene.scene.key === 'MenuScene') this.scene.currentScene.optionsButton.setTexture('menuUI', 'Settings_NonClicked.png');
    }

    hideOptions() {
        this.animateHide(this.optionsContainer, () => {
            this.panelContainer.setVisible(false);
            if (this.scene.currentScene.scene.key === 'MainScene') this.showPause();
        });
    }

    showCredits() {
        this.animateShow(this.creditsContainer);
        this.panelContainer.setVisible(true);
    }

    hideCredits() {
        this.animateHide(this.creditsContainer, () => {
            this.panelContainer.setVisible(false);
        });
    }

    showPause() {
        this.animateShow(this.pauseContainer);
        this.panelContainer.setVisible(true);
    }

    hidePause(callback) {
        this.animateHide(this.pauseContainer, () => {
            this.panelContainer.setVisible(false);
            if (callback) callback();
        });
    }

    showReload() {
        this.animateShow(this.reloadContainer);
        this.reloadPanelContainer.setVisible(true);
    }

    hideReload() {
        this.animateHide(this.reloadContainer, () => {
            this.reloadPanelContainer.setVisible(false);
        });
    }

    showScore(score, newHighScore) {
        this.panel.setTexture("panel_dark");
        this.scoreDisplay.setText(score);
        this.recordText.setText(newHighScore);
        let gameplayTime = this.scene.currentScene.finishTime - this.scene.currentScene.startTime;
        this.timeText.setText(this.secondsToString(gameplayTime));
        this.animateShow(this.scoreContainer);
        this.panelContainer.setVisible(true);
    }

    hideScore() {
        this.panel.setTexture("panel");
        this.animateHide(this.scoreContainer, () => {
            this.panelContainer.setVisible(false);
        });
    }

    secondsToString(seconds) {
        const time = Math.floor(seconds);
        let hour = Math.floor(time / 3600);
        hour = (hour < 10) ? '0' + hour : hour;
        let minute = Math.floor((time / 60) % 60);
        minute = (minute < 10) ? '0' + minute : minute;
        let second = time % 60;
        second = (second < 10) ? '0' + second : second;
        return hour + ':' + minute + ':' + second;
    }
}
