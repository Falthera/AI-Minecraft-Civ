import { createBot, Bot, Entity } from 'mineflayer';
import { mineflayer } from 'mineflayer';
import pathfinder from 'mineflayer-pathfinder';
import { BotManager } from './bot-manager';
import { BotConfig, BotState, ActionPayload } from './types';

export class BotWorker {
  private bot: Bot | null = null;
  private config: BotConfig;
  private manager: BotManager;
  private reconnectDelay = 5000;
  private maxReconnectDelay = 60000;

  constructor(config: BotConfig, manager: BotManager) {
    this.config = config;
    this.manager = manager;
  }

  async start(): Promise<void> {
    await this.connect();
  }

  private async connect(): Promise<void> {
    try {
      this.bot = createBot({
        host: this.config.host,
        port: this.config.port,
        username: this.config.username,
        auth: this.config.auth,
        email: this.config.email,
        password: this.config.password,
        accessToken: this.config.accessToken,
        version: false,
      });

      this.bot.on('login', () => {
        console.log(`[BotWorker] ${this.config.username} connected`);
        this.reconnectDelay = 5000;
        pathfinder(this.bot);
        this.manager.onBotConnected(this.config.id);
      });

      this.bot.on('end', () => {
        console.log(`[BotWorker] ${this.config.username} disconnected`);
        this.manager.onBotDisconnected(this.config.id);
        this.scheduleReconnect();
      });

      this.bot.on('error', (err) => {
        console.error(`[BotWorker] ${this.config.username} error:`, err);
      });

      this.bot.on('spawn', () => {
        console.log(`[BotWorker] ${this.config.username} spawned in world`);
      });

      this.bot.on('health', () => {
        this.manager.updateBotState(this.config.id, {
          health: this.bot!.health,
          hunger: this.bot!.food,
          position: this.bot!.entity.position.toObject(),
          dimension: this.bot!.game.dimension,
        });
      });

      this.bot.on('chat', (username, message) => {
        // Forward chat to controller.
      });

      this.bot.on('death', () => {
        console.log(`[BotWorker] ${this.config.username} died`);
        this.manager.onBotDied(this.config.id);
      });

      // Poll controller for actions.
      this.actionPollLoop();
    } catch (error) {
      console.error(`[BotWorker] Failed to start ${this.config.username}:`, error);
      this.scheduleReconnect();
    }
  }

  private async actionPollLoop(): Promise<void> {
    if (!this.bot || !this.bot.entity) return;

    try {
      const action = await this.fetchAction();
      if (action) {
        await this.executeAction(action);
      }
    } catch (error) {
      // Silently continue polling.
    }

    setTimeout(() => this.actionPollLoop(), 1000);
  }

  private async fetchAction(): Promise<ActionPayload | null> {
    // In production: GET /agents/{id}/actions from AI Controller.
    return null;
  }

  private async executeAction(action: ActionPayload): Promise<void> {
    if (!this.bot || !this.bot.entity) return;
    const entity: Entity = this.bot.entity;

    switch (action.action) {
      case 'MOVE':
        if (action.target) {
          const [x, y, z] = action.target.split(',').map(Number);
          await this.bot.pathfinder.goto(new this.bot.pathfinder.goals.GoalNear(x, y, z, 1));
        }
        break;
      case 'MINE':
        if (action.target) {
          const block = this.bot.blockAt(action.target);
          if (block) {
            await this.bot.dig(block);
          }
        }
        break;
      case 'CHOP':
        // Find nearest tree and chop.
        break;
      case 'FARM':
        // Farm nearby crops.
        break;
      case 'BUILD':
        // Place blocks.
        break;
      case 'FIGHT':
        // Attack nearest hostile.
        break;
      case 'EAT':
        // Eat food from inventory.
        break;
      default:
        break;
    }
  }

  private scheduleReconnect(): void {
    setTimeout(() => this.connect(), this.reconnectDelay);
    this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
  }

  async stop(): Promise<void> {
    if (this.bot) {
      this.bot.removeAllListeners();
      this.bot.end();
      this.bot = null;
    }
  }

  getState(): BotState {
    return {
      id: this.config.id,
      username: this.config.username,
      connected: !!this.bot?.connected,
      health: this.bot?.health ?? 0,
      hunger: this.bot?.food ?? 0,
      position: this.bot?.entity.position.toObject() ?? { x: 0, y: 0, z: 0 },
      dimension: this.bot?.game.dimension ?? 'unknown',
    };
  }
}
