const prodRoute =  'https://static.pchujoy.com/public/games-assets/parchados';


export class ResourceLoader{
 
    static isProd = true;

    constructor(scene){
        this.scene = scene;
    }

    static ReturnPath(){
        if(this.isProd){
            return prodRoute
        }
        else{
            return './src'
        }
    }

    static ReturnLocalePath(lang) {
        if (this.isProd) {
             return `${prodRoute}/scripts/locales/${lang}.json`;
        }
        return `./src/scripts/locales/${lang}.json`;
    }
}
