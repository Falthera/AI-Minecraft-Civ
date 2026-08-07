import { BotWorker } from './bot-worker';
import { BotConfig, BotState } from './types';

export class BotManager {
  private workers: Map<string, BotWorker> = new Map();
  private states: Map<string, BotState> = new Map();

  async startBots(configs: BotConfig[]): Promise<void> {
    for (const config of configs) {
      const worker = new BotWorker(config, this);
      this.workers.set(config.id, worker);
      this.states.set(config.id, {
        id: config.id,
        username: config.username,
        connected: false,
        health: 0,
        hunger: 0,
        position: { x: 0, y: 0, z: 0 },
        dimension: 'unknown',
      });
      worker.start();
    }
  }

  onBotConnected(id: string): void {
    const state = this.states.get(id);
    if (state) {
      state.connected = true;
    }
    console.log(`[BotManager] Bot ${id} connected`);
  }

  onBotDisconnected(id: string): void {
    const state = this.states.get(id);
    if (state) {
      state.connected = false;
    }
  }

  onBotDied(id: string): void {
    console.log(`[BotManager] Bot ${id} died — do not reconnect per hardcore rules.`);
    const state = this.states.get(id);
    if (state) {
      state.connected = false;
      state.health = 0;
    }
    // Do not restart dead bots.
  }

  updateBotState(id: string, partial: Partial<BotState>): void {
    const state = this.states.get(id);
    if (state) {
      Object.assign(state, partial);
    }
  }

  getState(id: string): BotState | undefined {
    return this.states.get(id);
  }

  getAllStates(): BotState[] {
    return Array.from(this.states.values());
  }

  async stopAll(): Promise<void> {
    const promises = Array.from(this.workers.values()).map(w => w.stop());
    await Promise.all(promises);
    this.workers.clear();
  }
}
