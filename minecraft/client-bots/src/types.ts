export interface BotConfig {
  id: string;
  username: string;
  host: string;
  port: number;
  auth: "microsoft" | "mojang" | "offline";
  email?: string;
  password?: string;
  accessToken?: string;
  controllerUrl: string;
  controllerApiKey: string;
}

export interface BotState {
  id: string;
  username: string;
  connected: boolean;
  health: number;
  hunger: number;
  position: { x: number; y: number; z: number };
  dimension: string;
}

export interface ActionPayload {
  action: string;
  target?: string;
  params: Record<string, unknown>;
}
