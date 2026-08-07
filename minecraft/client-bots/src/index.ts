import 'dotenv/config';
import { BotManager } from './bot-manager';
import { BotConfig } from './types';

const manager = new BotManager();

async function main() {
  const host = process.env.MINECRAFT_HOST || 'localhost';
  const port = parseInt(process.env.MINECRAFT_PORT || '25565', 10);
  const controllerUrl = process.env.AI_CONTROLLER_URL || 'http://localhost:8000';
  const controllerApiKey = process.env.AI_CONTROLLER_API_KEY || 'changeme';
  const botCount = parseInt(process.env.BOT_COUNT || '1', 10);

  const configs: BotConfig[] = [];
  for (let i = 0; i < botCount; i++) {
    configs.push({
      id: `bot-${i}`,
      username: `AI_Agent_${String(i).padStart(4, '0')}`,
      host,
      port,
      auth: 'offline',
      controllerUrl,
      controllerApiKey,
    });
  }

  await manager.startBots(configs);

  process.on('SIGINT', async () => {
    console.log('Shutting down...');
    await manager.stopAll();
    process.exit(0);
  });
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
