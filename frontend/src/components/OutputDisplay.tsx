import { useEffect, useRef } from 'react';
import { OutputLine } from '../types';

interface Props {
  lines: OutputLine[];
}

const colorMap: Record<OutputLine['type'], string> = {
  system: '#64ffda',
  command: '#ffcc02',
  narrative: '#00ff41',
  error: '#ff5555',
  achievement: '#ffd700',
  combat: '#ff6b6b',
  ending: '#c084fc',
};

export function OutputDisplay({ lines }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [lines]);

  return (
    <div
      style={{
        flex: 1,
        overflowY: 'auto',
        padding: '12px 16px',
        fontFamily: "'Fira Code', monospace",
        fontSize: '14px',
        lineHeight: '1.7',
        background: '#0a0a0a',
      }}
    >
      {lines.map(line => (
        <pre
          key={line.id}
          style={{
            margin: '2px 0',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            color: colorMap[line.type] ?? '#00ff41',
            textShadow: line.type === 'achievement'
              ? '0 0 8px #ffd700'
              : line.type === 'ending'
                ? '0 0 12px #c084fc'
                : line.type === 'combat'
                  ? '0 0 4px #ff6b6b44'
                  : '0 0 2px #00ff4133',
          }}
        >
          {line.text}
        </pre>
      ))}
      {/* CRT scanline overlay effect via CSS */}
      <div ref={bottomRef} />
    </div>
  );
}
