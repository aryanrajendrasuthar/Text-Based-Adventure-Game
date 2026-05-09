import { useState, useCallback, useRef } from 'react';
import { api } from '../services/api';
import { GameState, OutputLine } from '../types';

let lineCounter = 0;
const nextId = () => ++lineCounter;

function classifyMessage(text: string): OutputLine['type'] {
  if (text.includes('ACHIEVEMENT UNLOCKED')) return 'achievement';
  if (text.includes('GAME OVER') || text.includes('ENDING') || text.includes('THE END')) return 'ending';
  if (
    text.includes('⚔️') || text.includes('💥') || text.includes('☠️') ||
    text.includes('HP:') || text.includes('damage')
  ) return 'combat';
  if (text.startsWith('>')) return 'command';
  return 'narrative';
}

function parseMessages(msgs: string[]): OutputLine[] {
  return msgs.map(m => ({
    id: nextId(),
    text: m,
    type: classifyMessage(m),
  }));
}

export function useGame() {
  const [sessionId, setSessionId] = useState<string | null>(
    () => localStorage.getItem('sessionId')
  );
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [output, setOutput] = useState<OutputLine[]>([]);
  const [loading, setLoading] = useState(false);
  const [playerName, setPlayerName] = useState('');
  const [started, setStarted] = useState(false);
  const commandHistory = useRef<string[]>([]);
  const historyIndex = useRef(-1);

  const appendLines = useCallback((lines: OutputLine[]) => {
    setOutput(prev => [...prev, ...lines]);
  }, []);

  const startGame = useCallback(async (name: string) => {
    setLoading(true);
    try {
      const resp = await api.newGame(name);
      localStorage.setItem('sessionId', resp.session_id);
      setSessionId(resp.session_id);
      setGameState(resp.state);
      setStarted(true);
      appendLines(parseMessages(resp.messages));
    } catch (e) {
      appendLines([{ id: nextId(), text: '❌ Failed to connect to the game server. Is the backend running?', type: 'error' }]);
    } finally {
      setLoading(false);
    }
  }, [appendLines]);

  const loadExistingGame = useCallback(async () => {
    const sid = localStorage.getItem('sessionId');
    if (!sid) return;
    setLoading(true);
    try {
      const resp = await api.loadGame(sid);
      setSessionId(sid);
      setGameState(resp.state);
      setStarted(true);
      appendLines(parseMessages(resp.messages));
    } catch {
      localStorage.removeItem('sessionId');
      setSessionId(null);
    } finally {
      setLoading(false);
    }
  }, [appendLines]);

  const sendCommand = useCallback(async (cmd: string) => {
    if (!sessionId || loading || !cmd.trim()) return;

    // Add to history
    commandHistory.current = [cmd, ...commandHistory.current.slice(0, 49)];
    historyIndex.current = -1;

    appendLines([{ id: nextId(), text: `> ${cmd}`, type: 'command' }]);
    setLoading(true);
    try {
      const resp = await api.sendCommand(sessionId, cmd);
      setGameState(resp.state);
      appendLines(parseMessages(resp.messages));
    } catch (e) {
      appendLines([{ id: nextId(), text: '❌ Network error. Please try again.', type: 'error' }]);
    } finally {
      setLoading(false);
    }
  }, [sessionId, loading, appendLines]);

  const navigateHistory = useCallback((direction: 'up' | 'down'): string => {
    const hist = commandHistory.current;
    if (!hist.length) return '';
    if (direction === 'up') {
      historyIndex.current = Math.min(historyIndex.current + 1, hist.length - 1);
    } else {
      historyIndex.current = Math.max(historyIndex.current - 1, -1);
    }
    return historyIndex.current >= 0 ? hist[historyIndex.current] : '';
  }, []);

  const clearOutput = useCallback(() => setOutput([]), []);

  const resetGame = useCallback(() => {
    localStorage.removeItem('sessionId');
    setSessionId(null);
    setGameState(null);
    setOutput([]);
    setStarted(false);
    historyIndex.current = -1;
    commandHistory.current = [];
  }, []);

  return {
    sessionId,
    gameState,
    output,
    loading,
    playerName,
    setPlayerName,
    started,
    startGame,
    loadExistingGame,
    sendCommand,
    navigateHistory,
    clearOutput,
    resetGame,
  };
}
