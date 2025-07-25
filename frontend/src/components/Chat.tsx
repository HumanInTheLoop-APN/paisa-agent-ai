import React, { useState } from 'react';

export const Chat: React.FC = () => {
    const [messages, setMessages] = useState<{ author: string, text: string }[]>([]);
    const [input, setInput] = useState('');

    const sendMessage = () => {
        if (!input.trim()) return;
        setMessages([...messages, { author: 'user', text: input }]);
        setInput('');
        // TODO: Call backend API and append agent response
    };

    return (
        <div style={{ background: '#F0F4F9', padding: 16, borderRadius: 8 }}>
            <div style={{ minHeight: 200, marginBottom: 8 }}>
                {messages.map((msg, i) => (
                    <div key={i} style={{ textAlign: msg.author === 'user' ? 'right' : 'left' }}>
                        <b>{msg.author}:</b> {msg.text}
                    </div>
                ))}
            </div>
            <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' ? sendMessage() : undefined}
                placeholder="Type your message..."
                style={{ width: '80%', marginRight: 8 }}
            />
            <button onClick={sendMessage} style={{ background: '#2962FF', color: '#fff', border: 'none', borderRadius: 4, padding: '4px 12px' }}>
                Send
            </button>
        </div>
    );
}; 