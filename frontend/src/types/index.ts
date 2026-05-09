export interface PlayerState {
  name: string;
  hp: number;
  max_hp: number;
  attack: number;
  defense: number;
  inventory: string[];
  current_room: string;
  gold: number;
  xp: number;
  level: number;
  equipped_weapon: string | null;
  equipped_armor: string | null;
  flags: Record<string, boolean | string | number>;
}

export interface RoomState {
  id: string;
  name: string;
  description: string;
  ascii_art: string;
  exits: Record<string, string>;
  items: string[];
  npcs: string[];
  enemies: string[];
  visited: boolean;
}

export interface EnemyState {
  id: string;
  name: string;
  hp: number;
  max_hp: number;
  attack: number;
  defense: number;
  is_boss: boolean;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  unlocked: boolean;
}

export interface GameState {
  player: PlayerState;
  current_room: RoomState | null;
  alive_enemies: EnemyState[];
  achievements: Achievement[];
  game_over: boolean;
  ending: string | null;
  command_count: number;
  bosses_defeated: number;
}

export interface GameResponse {
  session_id: string;
  messages: string[];
  state: GameState;
}

export interface OutputLine {
  id: number;
  text: string;
  type: 'system' | 'command' | 'narrative' | 'error' | 'achievement' | 'combat' | 'ending';
}
