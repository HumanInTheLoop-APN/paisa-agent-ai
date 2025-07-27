import { useAiChatApi } from "@nlux/react";
import React, { createContext, useContext, ReactNode } from "react";

type AiChatApiType = ReturnType<typeof useAiChatApi>;

const AiChatContext = createContext<AiChatApiType | null>(null);

interface AiChatProviderProps {
  children: ReactNode;
}

/**
 * Provider component that creates and shares a single instance of the chat API
 */
export const AiChatProvider: React.FC<AiChatProviderProps> = ({ children }) => {
  const api = useAiChatApi();

  return (
    <AiChatContext.Provider value={api}>{children}</AiChatContext.Provider>
  );
};

/**
 * Custom hook that provides access to the shared chat API instance
 * Must be used within an AiChatProvider
 */
export const useAiChat = (): AiChatApiType => {
  const context = useContext(AiChatContext);

  if (!context) {
    throw new Error("useAiChat must be used within an AiChatProvider");
  }

  return context;
};
