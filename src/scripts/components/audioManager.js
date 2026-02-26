import * as Phaser from 'phaser';
import {ResourceLoader} from '../components/resourceLoader.js';

export class AudioManager
{
    constructor(scene){
        this.scene = scene;
    }

    load(){
        
        //main Themes
        this.scene.load.audio('mainTheme', [ResourceLoader.ReturnPath()+'/audios/title.ogg',ResourceLoader.ReturnPath()+'/audios/title.m4a'])
        this.scene.load.audio('gameplayMusic', [ResourceLoader.ReturnPath()+'/audios/maintheme.ogg',ResourceLoader.ReturnPath()+'/audios/maintheme.m4a'])

        this.scene.load.audio('alarma', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_alarma_loop.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_alarma_loop.m4a'])
        this.scene.load.audio('destruccion', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_destruccion.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_destruccion.m4a'])
        this.scene.load.audio('preview', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_ficha_preview.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_ficha_preview.m4a'])
        this.scene.load.audio('soltar', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_ficha_soltar.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_ficha_soltar.m4a'])
        this.scene.load.audio('aviso', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_powerup_aviso.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_powerup_aviso.m4a'])
        this.scene.load.audio('bomba', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_powerup_bomba.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_powerup_bomba.m4a'])
        this.scene.load.audio('reduccion', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_powerup_reduccion.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_powerup_reduccion.m4a'])
        this.scene.load.audio('puntos', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_puntos.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_puntos.m4a'])
        this.scene.load.audio('tapete', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_tapete.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_tapete.m4a'])
        this.scene.load.audio('ui_click', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_ui_button_click.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_ui_button_click.m4a'])
        this.scene.load.audio('ui_page', [ResourceLoader.ReturnPath()+'/audios/ogg/sfx_ui_button_page.ogg',ResourceLoader.ReturnPath()+'/audios/m4a/sfx_ui_button_page.m4a'])

    }

    init(){
        
        this.scene.sound.pauseOnBlur = false

        //sfx
        this.sfx = [];
        this.addSFX();
        
        //menuTheme
        this.menuMusic = this.scene.sound.add('mainTheme', {
            volume: .5,
            loop: true
        });

        //gameplayTheme
        this.gameplayMusic = this.scene.sound.add('gameplayMusic', {
            volume: .5,
            loop: true
        });
    
        if (!this.scene.sound.locked)
        {
            // already unlocked so play
            this.getCurrentTheme().play();
            
            this.setAudioVolume(this.scene.data.get('musicVolume'));
        }
        else
        {
            // wait for 'unlocked' to fire and then play
            this.scene.sound.once(Phaser.Sound.Events.UNLOCKED, () => {
                this.getCurrentTheme().play();
                
                this.setAudioVolume(this.scene.data.get('musicVolume'));
            })
        }

        this.scene.game.events.on(Phaser.Core.Events.BLUR, () => {
            this.handleLoseFocus();
        })
    
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden)
            {
                return
            }
    
            this.handleLoseFocus();
        })
        
    }

    addSFX(){

        this.alarma = this.scene.sound.add('alarma', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.alarma);

        this.destruccion = this.scene.sound.add('destruccion', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.destruccion);
        
        this.preview = this.scene.sound.add('preview', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.preview);
        
        this.soltar = this.scene.sound.add('soltar', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.soltar);
        
        this.aviso = this.scene.sound.add('aviso', {
            volume: .5,
            loop: true
        });
        this.sfx.push(this.aviso);
        
        this.bomba = this.scene.sound.add('bomba', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.bomba);
        
        this.reduccion = this.scene.sound.add('reduccion', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.reduccion);
        
        this.puntos = this.scene.sound.add('puntos', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.puntos);
        
        this.tapete = this.scene.sound.add('tapete', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.tapete);
        
        this.ui_click = this.scene.sound.add('ui_click', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.ui_click);
        
        this.ui_page = this.scene.sound.add('ui_page', {
            volume: .5,
            loop: false
        });
        this.sfx.push(this.ui_page);
        
    }

    getCurrentTheme(){
        
        let currentScene;
        if (this.scene.currentScene != null) currentScene = this.scene.currentScene.scene.key;
        else currentScene = 'MenuScene'
        switch(currentScene){
            case 'MenuScene':
                return this.menuMusic;
            case 'MainScene':
                return this.gameplayMusic;
            default:
                break;
        }
    }
    
    handleLoseFocus()
    {
        
        if (this.scene.currentScene != null) {
            // assuming a Paused scene that has a pause modal
            if (this.scene.currentScene.isPaused)
            {
                return
            }
            // pause music or stop all sounds
            //this.pauseMusic();
            //this.scene.currentScene.PauseGame?this.scene.currentScene.PauseGame();
            //this.scene.currentScene.isPaused = true;
        }
        
    }

    setAudioVolume(value){
        
        this.menuMusic.volume = value;
        this.gameplayMusic.volume = value;
        this.updateSFXVolume(value);
        
    }

    playMusic(){
        this.getCurrentTheme().play();
        
    }

    resumeMusic(){
        
        if (this.scene.currentScene.isPaused) {
            this.volumeDownTween?.remove();
            this.volumeDownTween = null;

            let audio = this.getCurrentTheme()
            audio.resume();
            let volumeUpTween = this.scene.tweens.add({
                targets: audio,
                ease: 'sine.inout',
                duration: 500,
                repeat: 0,
                volume: {
                    getStart: () => 0,
                    getEnd: () => this.scene.data.get('musicVolume')
                },
                onComplete: () => {
                    this.volumeDownTween?.remove();
                    volumeUpTween = null;
                }
            });
        }
        
    }

    pauseMusic(){
        
        let audio = this.getCurrentTheme();
        this.volumeDownTween = this.scene.tweens.add({
            targets: audio,
            ease: 'sine.inout',
            duration: 500,
            repeat: 0,
            volume: {
                getStart: () => this.scene.data.get('musicVolume'),
                getEnd: () => 0
            },
            onComplete: () => {
                this.volumeDownTween?.remove();
                this.volumeDownTween = null;
                audio.pause();
            }
        });
        
    }

    stopMusic(){
        
        this.getCurrentTheme().stop();
        
    }

    updateSFXVolume(value){
        for(let i = 0; i < this.sfx.length; i++){
            if (this.sfx[i].key != 'scoreMarkSound') this.sfx[i].volume = value;
            else this.sfx[i].volume = value >= 0.05 ? value + .2 : value;
        }
        
    }
}