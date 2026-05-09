import { useState, KeyboardEvent } from 'react';

interface Props {
  onStart: (name: string) => void;
  onLoad: () => void;
  hasExisting: boolean;
  loading: boolean;
}

export function StartScreen({ onStart, onLoad, hasExisting, loading }: Props) {
  const [name, setName] = useState('');

  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && name.trim()) onStart(name.trim());
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#050505',
        fontFamily: "'Fira Code', monospace",
      }}
    >
      <div
        style={{
          textAlign: 'center',
          maxWidth: '560px',
          padding: '40px',
          border: '1px solid #00ff4133',
          background: '#0a0a0a',
          boxShadow: '0 0 40px #00ff4111',
        }}
      >
        {/* ASCII title */}
        <pre
          style={{
            color: '#00ff41',
            fontSize: '13px',
            textShadow: '0 0 10px #00ff4166',
            margin: '0 0 8px',
          }}
        >
{`
  █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗
 ██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
 ███████║█████╗     ██║   ███████║█████╗  ██████╔╝
 ██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
 ██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
 ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
         M O O R
`}
        </pre>
        <p style={{ color: '#64ffda', fontSize: '14px', margin: '0 0 4px' }}>
          THE LOST KINGDOM OF AETHERMOOR
        </p>
        <p style={{ color: '#444', fontSize: '12px', margin: '0 0 32px' }}>
          A text-based adventure · 20 rooms · 3 endings · 10 achievements
        </p>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', color: '#888', fontSize: '12px', marginBottom: '8px', textAlign: 'left' }}>
            ENTER YOUR NAME:
          </label>
          <input
            value={name}
            onChange={e => setName(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Adventurer"
            maxLength={30}
            autoFocus
            style={{
              width: '100%',
              boxSizing: 'border-box',
              background: '#111',
              border: '1px solid #00ff4144',
              color: '#ffcc02',
              fontFamily: "'Fira Code', monospace",
              fontSize: '14px',
              padding: '10px 14px',
              outline: 'none',
              caretColor: '#00ff41',
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: '12px', flexDirection: 'column' }}>
          <button
            onClick={() => name.trim() && onStart(name.trim())}
            disabled={loading || !name.trim()}
            style={{
              background: loading ? '#111' : '#00ff4120',
              border: '1px solid #00ff41',
              color: '#00ff41',
              fontFamily: "'Fira Code', monospace",
              fontSize: '14px',
              padding: '12px',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s',
            }}
          >
            {loading ? 'LOADING...' : '▶ BEGIN ADVENTURE'}
          </button>

          {hasExisting && (
            <button
              onClick={onLoad}
              disabled={loading}
              style={{
                background: 'transparent',
                border: '1px solid #64ffda44',
                color: '#64ffda',
                fontFamily: "'Fira Code', monospace",
                fontSize: '13px',
                padding: '10px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              ↩ CONTINUE SAVED GAME
            </button>
          )}
        </div>

        <p style={{ color: '#333', fontSize: '11px', marginTop: '24px' }}>
          Type 'help' in-game for commands. Use ↑↓ arrows for command history.
        </p>
      </div>
    </div>
  );
}
