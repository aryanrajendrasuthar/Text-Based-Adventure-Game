import { useEffect } from 'react';
import { useGame } from './hooks/useGame';
import { StartScreen } from './components/StartScreen';
import { OutputDisplay } from './components/OutputDisplay';
import { CommandInput } from './components/CommandInput';
import { Sidebar } from './components/Sidebar';

export default function App() {
  const {
    sessionId,
    gameState,
    output,
    loading,
    started,
    startGame,
    loadExistingGame,
    sendCommand,
    navigateHistory,
    resetGame,
  } = useGame();

  const hasExisting = !!localStorage.getItem('sessionId');

  if (!started) {
    return (
      <StartScreen
        onStart={startGame}
        onLoad={loadExistingGame}
        hasExisting={hasExisting}
        loading={loading}
      />
    );
  }

  return (
    <div
      style={{
        display: 'flex',
        height: '100vh',
        background: '#050505',
        overflow: 'hidden',
        position: 'relative',
      }}
    >
      {/* CRT scanline overlay */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          background:
            'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)',
          pointerEvents: 'none',
          zIndex: 100,
        }}
      />

      {/* Main terminal area */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          minWidth: 0,
        }}
      >
        {/* Header bar */}
        <div
          style={{
            padding: '8px 16px',
            background: '#0d0d0d',
            borderBottom: '1px solid #00ff4122',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
          }}
        >
          <span style={{ color: '#00ff41', fontFamily: "'Fira Code', monospace", fontSize: '12px' }}>
            ◉ AETHERMOOR TERMINAL
          </span>
          {gameState && (
            <span style={{ color: '#444', fontFamily: "'Fira Code', monospace", fontSize: '11px' }}>
              {gameState.player.name} · Lvl {gameState.player.level} · {gameState.player.hp}/{gameState.player.max_hp} HP
            </span>
          )}
          {loading && (
            <span style={{ color: '#ffcc0288', fontFamily: "'Fira Code', monospace", fontSize: '11px', marginLeft: 'auto' }}>
              ⟳ Processing...
            </span>
          )}
          {gameState?.game_over && (
            <span style={{ color: '#ff5555', fontFamily: "'Fira Code', monospace", fontSize: '12px', marginLeft: 'auto' }}>
              GAME ENDED — {gameState.ending?.toUpperCase()}
            </span>
          )}
        </div>

        <OutputDisplay lines={output} />

        <CommandInput
          onSubmit={sendCommand}
          onHistory={navigateHistory}
          disabled={loading || (gameState?.game_over ?? false)}
        />
      </div>

      {/* Sidebar */}
      {gameState && (
        <Sidebar
          gameState={gameState}
          onSave={() => alert(`Game auto-saves after every command.\nSession ID: ${sessionId}`)}
          onReset={resetGame}
        />
      )}
    </div>
  );
}
