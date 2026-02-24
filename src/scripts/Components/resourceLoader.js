const prodRoute = 'https://static.pchujoy.com/public/games-assets/parchados';

export class ResourceLoader {
    static isProd = true;

    constructor(scene) {
        this.scene = scene;
    }

    static ReturnPath() {
        // Priority 1: Window override (useful for custom hosting)
        if (typeof window !== 'undefined' && window.PARCHADOS_ASSETS_PATH) {
            return window.PARCHADOS_ASSETS_PATH;
        }

        // Priority 2: Production route
        if (this.isProd) {
            return prodRoute;
        }

        // Priority 3: Local dev route
        return './src';
    }
}
