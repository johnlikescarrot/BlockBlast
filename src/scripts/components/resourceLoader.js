import { SUPPORTED_LOCALES } from './i18n.js';

const prodRoute = 'https://static.pchujoy.com/public/games-assets/parchados';

export class ResourceLoader {
    static isProd = true;
    static supportedLocales = new Set(SUPPORTED_LOCALES);

    constructor(scene) {
        this.scene = scene;
    }

    static ReturnPath() {
        if (this.isProd) {
            return prodRoute;
        } else {
            return './src';
        }
    }

    static ReturnLocalePath(lang) {
        const safeLang = this.supportedLocales.has(lang) ? lang : 'en';
        if (this.isProd) {
            return `${prodRoute}/scripts/locales/${safeLang}.json`;
        }
        return `./src/scripts/locales/${safeLang}.json`;
    }
}
