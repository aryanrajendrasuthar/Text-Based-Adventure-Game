import axios from 'axios';
import { GameResponse } from '../types';

const BASE = '/game';

export const api = {
  newGame: (playerName: string): Promise<GameResponse> =>
    axios.post(`${BASE}/new`, { player_name: playerName }).then(r => r.data),

  loadGame: (sessionId: string): Promise<GameResponse> =>
    axios.get(`${BASE}/${sessionId}`).then(r => r.data),

  sendCommand: (sessionId: string, command: string): Promise<GameResponse> =>
    axios.post(`${BASE}/${sessionId}/command`, { command }).then(r => r.data),

  getAchievements: (sessionId: string) =>
    axios.get(`${BASE}/${sessionId}/achievements`).then(r => r.data),
};
