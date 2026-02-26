import { SUPPORTED_LOCALES } from './i18n.js';

const prodRoute = process.env.ASSET_PATH || 'https://static.pchujoy.com/public/games-assets/parchados';

export class ResourceLoader {
    static isProd = process.env.NODE_ENV === 'production';
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
        // Locales are bundled locally via CopyWebpackPlugin in webpack/base.js
        return `./scripts/locales/${safeLang}.json`;
    }
}
