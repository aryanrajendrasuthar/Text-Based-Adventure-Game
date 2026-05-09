import { useState, useRef, KeyboardEvent } from 'react';

interface Props {
  onSubmit: (cmd: string) => void;
  onHistory: (dir: 'up' | 'down') => string;
  disabled: boolean;
}

export function CommandInput({ onSubmit, onHistory, disabled }: Props) {
  const [value, setValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && value.trim()) {
      onSubmit(value.trim());
      setValue('');
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setValue(onHistory('up'));
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setValue(onHistory('down'));
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        padding: '8px 16px',
        background: '#111',
        borderTop: '1px solid #00ff4133',
        gap: '8px',
      }}
    >
      <span
        style={{
          color: '#00ff41',
          fontFamily: "'Fira Code', monospace",
          fontSize: '14px',
          userSelect: 'none',
          animation: disabled ? 'none' : 'blink 1s step-end infinite',
        }}
      >
        &gt;
      </span>
      <input
        ref={inputRef}
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        disabled={disabled}
        placeholder={disabled ? 'Processing...' : 'Enter command...'}
        autoFocus
        spellCheck={false}
        autoComplete="off"
        style={{
          flex: 1,
          background: 'transparent',
          border: 'none',
          outline: 'none',
          color: '#ffcc02',
          fontFamily: "'Fira Code', monospace",
          fontSize: '14px',
          caretColor: '#00ff41',
        }}
      />
      <button
        onClick={() => { if (value.trim()) { onSubmit(value.trim()); setValue(''); } }}
        disabled={disabled || !value.trim()}
        style={{
          background: '#00ff4120',
          border: '1px solid #00ff4155',
          color: '#00ff41',
          fontFamily: "'Fira Code', monospace",
          fontSize: '12px',
          padding: '4px 12px',
          cursor: disabled ? 'not-allowed' : 'pointer',
          borderRadius: '3px',
        }}
      >
        SEND
      </button>
    </div>
  );
}
