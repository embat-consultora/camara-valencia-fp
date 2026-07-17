// @ts-check
import { test, expect } from '@playwright/test';
class StreamlitAppPage {
  constructor(page) {
    this.page = page;
  }

  // Obtiene el frame de Streamlit
  async getFrame() {
    const frameElement = await this.page.waitForSelector('iframe[title="streamlitApp"]', { timeout: 60000 });
    return await frameElement.contentFrame();
  }

  async navigateTo(url) {
    await this.page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }

  async handleWakeupIfNeeded() {
    // El wakeup button está en la página principal, NO en el iframe
    const wakeupButton = this.page.getByTestId('wakeup-button-viewer');
    console.log("Buscando el boton de wakeup")
    const isSleeping = await wakeupButton.isVisible({ timeout: 10000 }).catch(() => false);
    if (isSleeping) {
      console.log("Estaba dormida, haciendo click en el boton de wakeup")
      await wakeupButton.click({force:true});
    }
  }

  async waitForAppReady() {
    const frame = await this.getFrame();
    // Espera que el spinner desaparezca dentro del iframe
    await frame.waitForSelector('[data-testid="stSpinner"]', { state: 'detached', timeout: 30000 }).catch(() => {});
    await this.page.waitForLoadState('networkidle', { timeout: 30000 });
  }

  async waitForEmailInput() {
    const frame = await this.getFrame();
    // Busca el placeholder DENTRO del iframe
    await frame.getByPlaceholder('Ingrese email o usuario').waitFor({ state: 'visible', timeout: 120000 });
  }
}
test.describe('Streamlit Apps Wake-up @smoke', () => {
  test('Cámara Valencia FP app loads and wakes up', async ({ page }) => {
    const streamlitApp = new StreamlitAppPage(page);
    console.log("Navigating to Cámara Valencia FP app");
    await streamlitApp.navigateTo('https://camara-valencia-fp.streamlit.app/');
    console.log("Veo si esta durmiendo");
    await streamlitApp.handleWakeupIfNeeded();
    console.log("Ya la deberia haber despertado");
    await streamlitApp.waitForAppReady();   
    
    await streamlitApp.waitForEmailInput();   
  });

  test('Cámara MCC app loads and wakes up', async ({ page }) => {
    const streamlitApp = new StreamlitAppPage(page);
    
    await streamlitApp.navigateTo('https://camara-mcc.streamlit.app/');
    await streamlitApp.handleWakeupIfNeeded();
    await streamlitApp.waitForAppReady();   
    
    await streamlitApp.waitForEmailInput();   
  });
});