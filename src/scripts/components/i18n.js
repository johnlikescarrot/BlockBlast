export class I18nManager {
    constructor(scene) {
        this.scene = scene;
        this.storageKey = 'blockblast_language';
        // Try to get from localStorage, default to 'en'
        let storedLang = 'en';
        try {
            storedLang = localStorage.getItem(this.storageKey) || 'en';
        } catch (e) {
            console.warn('I18nManager: Could not access localStorage.', e);
        }
        this.currentLanguage = storedLang;
        this.locales = {};
    }

    init() {
        const languages = ['en', 'es'];
        for (const lang of languages) {
            const cacheKey = `locale_${lang}`;
            if (this.scene.cache.json.exists(cacheKey)) {
                this.locales[lang] = this.scene.cache.json.get(cacheKey);
            } else {
                console.warn(`I18nManager: Locale ${lang} not found in cache.`);
            }
        }

        // Ensure current language is valid among loaded locales, fallback to 'en'
        if (!this.locales[this.currentLanguage]) {
            this.currentLanguage = 'en';
        }
    }

    setLanguage(lang) {
        if (this.locales[lang]) {
            this.currentLanguage = lang;
            try {
                localStorage.setItem(this.storageKey, lang);
            } catch (e) {
                console.warn('I18nManager: Could not save to localStorage.', e);
            }
        }
    }

    get language() {
        return this.currentLanguage;
    }

    t(key) {
        const translation = this.locales[this.currentLanguage]?.[key];
        if (translation === undefined) {
            // console.warn(`I18nManager: Key "${key}" not found in "${this.currentLanguage}" locale.`);
            return key;
        }
        return translation;
    }
}
