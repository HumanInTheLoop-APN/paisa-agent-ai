import React, { useEffect, useState } from 'react';
import { AiChat, ChatAdapter, StreamingAdapterObserver } from '@nlux/react';
import { chatService } from '../services/chatService';
import { CustomResponseRenderer } from './CustomResponseRenderer';
import '@nlux/themes/nova.css';
import { authService } from '../services/authService';
import { useAiChat, AiChatProvider } from './useAiChat';

interface ChatInterfaceProps {
    onClose: () => void;
    submitMessage: string;
}

// Custom adapter for our backend API
const agentAdapter: ChatAdapter<any> = {
    streamText: async (message: string, observer: StreamingAdapterObserver) => {
        try {
            // get current session id from local storage
            let currentSessionId = localStorage.getItem('currentSessionId');
            if (!currentSessionId) {
                const session = await chatService.createSession();
                localStorage.setItem('currentSessionId', session.id);
                currentSessionId = session.id;
            }

            const auth_token = authService.getToken();

            // Send the message to the backend
            const response = await fetch(process.env.REACT_APP_API_URL + `/sessions/${currentSessionId}/chat`, {
                method: 'POST',
                body: `{"content": "${message}"}`,
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth_token}`, },
            });

            if (response.status !== 200) {
                console.log("--- response.status !== 200");
                observer.error(new Error('Failed to connect to the server'));
                return;
            }

            if (!response.body) {
                console.log("--- !response.body !!!!!!!!!!!!!!!!!!!!!!!!!");
                return;
            }

            const reader = response.body.getReader();
            const textDecoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                const event = JSON.parse(textDecoder.decode(value));

                console.log({ event });

                if (event.done || done) {
                    console.log('--- await reader.read() done')
                    break;
                }

                observer.next(event);
            }

            console.log('--- complete')
            observer.complete();

        } catch (error) {
            console.error('Error sending message:', error);
            observer.error(error as Error);
        }
    }
};

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ onClose, submitMessage }) => {
    const [isInitialized, setIsInitialized] = useState(false);

    useEffect(() => {
        if (isInitialized) return;
        setIsInitialized(true);

        setTimeout(() => {
            if (submitMessage) {
                // We'll handle this inside the AiChatProvider
                console.log('Submit message ready:', submitMessage);
                setIsInitialized(true);
            }
        }, 100);
    }, [submitMessage, isInitialized]);

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex flex-col">
            {/* Header */}
            <div className="bg-white/95 backdrop-blur-lg px-5 py-4 border-b border-black/10 flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-lg">
                        💬
                    </div>
                    <div>
                        <h2 className="m-0 text-xl font-semibold text-gray-800">
                            Financial Advisor
                        </h2>
                        <p className="m-0 text-sm text-gray-500">
                            Ask me anything about your finances
                        </p>
                    </div>
                </div>

                <button
                    onClick={onClose}
                    className="bg-transparent border-none text-2xl cursor-pointer text-gray-500 p-2 rounded-full transition-all duration-200 hover:bg-black/10 hover:text-gray-800"
                >
                    ✕
                </button>
            </div>

            {/* Chat Container */}
            <div className="flex-1 bg-white/95 backdrop-blur-lg m-5 rounded-2xl overflow-hidden shadow-2xl">
                <AiChatProvider>
                    <ChatWithProvider
                        submitMessage={submitMessage}
                        agentAdapter={agentAdapter}
                    />
                </AiChatProvider>
            </div>
        </div>
    );
};

// Internal component that uses the AiChatProvider context
const ChatWithProvider: React.FC<{
    submitMessage: string;
    agentAdapter: ChatAdapter<any>;
}> = ({ submitMessage, agentAdapter }) => {
    const api = useAiChat();

    useEffect(() => {
        if (submitMessage) {
            setTimeout(() => {
                api.composer.send(submitMessage);
                console.log('Sent message:', submitMessage);
            }, 100);
        }
    }, [submitMessage, api]);

    return (
        <AiChat
            api={api}
            adapter={agentAdapter}
            messageOptions={{
                responseRenderer: CustomResponseRenderer
            }}
        />
    );
};