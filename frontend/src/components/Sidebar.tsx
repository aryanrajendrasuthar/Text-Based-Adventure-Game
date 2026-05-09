import { GameState, Achievement } from '../types';

interface Props {
  gameState: GameState;
  onSave: () => void;
  onReset: () => void;
}

function HpBar({ current, max }: { current: number; max: number }) {
  const pct = Math.max(0, Math.min(100, (current / max) * 100));
  const color = pct > 60 ? '#00ff41' : pct > 30 ? '#ffcc02' : '#ff5555';
  return (
    <div style={{ marginTop: '4px' }}>
      <div
        style={{
          height: '8px',
          background: '#1a1a1a',
          borderRadius: '4px',
          border: '1px solid #333',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            height: '100%',
            width: `${pct}%`,
            background: color,
            boxShadow: `0 0 6px ${color}`,
            transition: 'width 0.3s ease',
          }}
        />
      </div>
      <span style={{ fontSize: '11px', color: '#888' }}>
        {current}/{max}
      </span>
    </div>
  );
}

function StatRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
      <span style={{ color: '#888', fontSize: '12px' }}>{label}</span>
      <span style={{ color: '#00ff41', fontSize: '12px', fontWeight: 600 }}>{value}</span>
    </div>
  );
}

function AchievementItem({ ach }: { ach: Achievement }) {
  return (
    <div
      style={{
        marginBottom: '6px',
        padding: '4px 6px',
        background: ach.unlocked ? '#ffd70011' : '#ffffff05',
        border: `1px solid ${ach.unlocked ? '#ffd70044' : '#222'}`,
        borderRadius: '3px',
      }}
    >
      <div style={{ fontSize: '11px', color: ach.unlocked ? '#ffd700' : '#555' }}>
        {ach.unlocked ? '✅' : '🔒'} {ach.unlocked ? ach.name : '???'}
      </div>
      {ach.unlocked && (
        <div style={{ fontSize: '10px', color: '#666', marginTop: '2px' }}>
          {ach.description}
        </div>
      )}
    </div>
  );
}

export function Sidebar({ gameState, onSave, onReset }: Props) {
  const { player, current_room, alive_enemies, achievements, bosses_defeated, command_count } = gameState;

  return (
    <div
      style={{
        width: '260px',
        background: '#0d0d0d',
        borderLeft: '1px solid #00ff4122',
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        padding: '12px',
        gap: '16px',
        fontFamily: "'Fira Code', monospace",
      }}
    >
      {/* Player Stats */}
      <section>
        <h3 style={{ color: '#00ff41', fontSize: '12px', margin: '0 0 8px', textTransform: 'uppercase', letterSpacing: '2px' }}>
          ⚔️ {player.name}
        </h3>
        <div style={{ color: '#888', fontSize: '11px', marginBottom: '4px' }}>
          Level {player.level}
        </div>
        <div style={{ color: '#ccc', fontSize: '11px', marginBottom: '2px' }}>HP</div>
        <HpBar current={player.hp} max={player.max_hp} />
        <div style={{ height: '8px' }} />
        <StatRow label="⚔ Attack" value={player.attack} />
        <StatRow label="🛡 Defense" value={player.defense} />
        <StatRow label="💰 Gold" value={player.gold} />
        <StatRow label="⭐ XP" value={player.xp} />
        <StatRow label="📜 Commands" value={command_count} />
        <StatRow label="👹 Bosses" value={`${bosses_defeated}/3`} />
      </section>

      {/* Location */}
      {current_room && (
        <section>
          <h3 style={{ color: '#64ffda', fontSize: '11px', margin: '0 0 6px', textTransform: 'uppercase', letterSpacing: '2px' }}>
            📍 Location
          </h3>
          <div style={{ color: '#aaa', fontSize: '12px' }}>{current_room.name}</div>
          {Object.keys(current_room.exits).length > 0 && (
            <div style={{ color: '#555', fontSize: '11px', marginTop: '4px' }}>
              Exits: {Object.keys(current_room.exits).join(', ')}
            </div>
          )}
        </section>
      )}

      {/* Active Enemies */}
      {alive_enemies.length > 0 && (
        <section>
          <h3 style={{ color: '#ff5555', fontSize: '11px', margin: '0 0 6px', textTransform: 'uppercase', letterSpacing: '2px' }}>
            ⚠️ Enemies
          </h3>
          {alive_enemies.map(e => (
            <div key={e.id} style={{ marginBottom: '6px' }}>
              <div style={{ color: e.is_boss ? '#ff0055' : '#ff6b6b', fontSize: '12px' }}>
                {e.is_boss ? '👹' : '👾'} {e.name}
              </div>
              <HpBar current={e.hp} max={e.max_hp} />
            </div>
          ))}
        </section>
      )}

      {/* Inventory */}
      <section>
        <h3 style={{ color: '#ffcc02', fontSize: '11px', margin: '0 0 6px', textTransform: 'uppercase', letterSpacing: '2px' }}>
          📦 Inventory ({player.inventory.length})
        </h3>
        {player.inventory.length === 0 ? (
          <div style={{ color: '#444', fontSize: '11px' }}>Empty</div>
        ) : (
          <div style={{ color: '#ccc', fontSize: '11px', lineHeight: '1.8' }}>
            {player.inventory.map(id => (
              <div key={id}>
                • {id.replace(/_/g, ' ')}
                {id === player.equipped_weapon ? ' ⚔' : ''}
                {id === player.equipped_armor ? ' 🛡' : ''}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Achievements */}
      <section>
        <h3 style={{ color: '#ffd700', fontSize: '11px', margin: '0 0 6px', textTransform: 'uppercase', letterSpacing: '2px' }}>
          🏆 Achievements ({achievements.filter(a => a.unlocked).length}/{achievements.length})
        </h3>
        {achievements.map(a => (
          <AchievementItem key={a.id} ach={a} />
        ))}
      </section>

      {/* Action Buttons */}
      <section style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: 'auto' }}>
        <button
          onClick={onSave}
          style={{
            background: '#00ff4115',
            border: '1px solid #00ff4144',
            color: '#00ff41',
            fontFamily: "'Fira Code', monospace",
            fontSize: '11px',
            padding: '6px',
            cursor: 'pointer',
            borderRadius: '3px',
          }}
        >
          💾 Save Game
        </button>
        <button
          onClick={onReset}
          style={{
            background: '#ff555515',
            border: '1px solid #ff555544',
            color: '#ff5555',
            fontFamily: "'Fira Code', monospace",
            fontSize: '11px',
            padding: '6px',
            cursor: 'pointer',
            borderRadius: '3px',
          }}
        >
          🔄 New Game
        </button>
      </section>
    </div>
  );
}
