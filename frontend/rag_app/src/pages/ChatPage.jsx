import React from 'react';
import { useChat } from '../hooks/useChat';
import ChatWindow from '../components/chat/ChatWindow';
import InputBar from '../components/chat/InputBar';
import { Scale, ArrowLeft, History } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ChatPage = () => {
    const { messages, isLoading, loadingStage, error, sendMessage } = useChat();
    const navigate = useNavigate();

    return (
        <div className="h-screen flex bg-secondary overflow-hidden">

            {/* Sidebar (Desktop) */}
            <aside className="hidden md:flex flex-col w-72 h-full bg-slate-900 border-r border-slate-800 shrink-0">

                {/* Header App */}
                <div className="h-16 flex items-center px-6 border-b border-slate-800">
                    <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
                        <div className="bg-indigo-600 p-1.5 rounded-lg">
                            <Scale size={18} className="text-white" />
                        </div>
                        <span className="font-bold text-lg tracking-tight">LegalRAG</span>
                    </div>
                </div>

                {/* History Area */}
                <div className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-800">
                    <div className="flex items-center text-xs text-slate-500 font-semibold uppercase mb-4 tracking-wider">
                        <History size={14} className="mr-2" />
                        Lịch sử tra cứu
                    </div>

                    <div className="space-y-2">
                        {messages.filter(m => m.role === 'user').map((m, i) => (
                            <div key={i} className="px-3 py-2.5 rounded-lg bg-slate-800/40 hover:bg-slate-800 text-sm text-slate-300 truncate cursor-pointer transition-colors border border-transparent hover:border-slate-700">
                                {m.content}
                            </div>
                        ))}
                        {messages.length === 0 && (
                            <div className="text-slate-600 text-sm italic px-2 py-4 text-center border-2 border-dashed border-slate-800 rounded-xl">
                                Chưa có phiên hỏi đáp nào
                            </div>
                        )}
                    </div>
                </div>
            </aside>

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative h-full w-full">
                {/* Mobile Header (Only valid on md-down) */}
                <header className="md:hidden h-14 flex items-center px-4 border-b border-slate-800 bg-slate-900 absolute top-0 w-full z-10 glass">
                    <button onClick={() => navigate('/')} className="p-2 mr-2 text-slate-400 hover:text-white">
                        <ArrowLeft size={20} />
                    </button>
                    <div className="font-bold text-md flex items-center">
                        <Scale size={16} className="text-indigo-400 mr-2" /> LegalRAG
                    </div>
                </header>

                {/* Error Banner nếu có */}
                {error && (
                    <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-red-500/20 border border-red-500/50 text-red-200 px-6 py-2 rounded-xl text-sm z-30 shadow-lg backdrop-blur-md animate-fade-in flex items-center">
                        <span>{error}</span>
                    </div>
                )}

                {/* Vùng chat (Có padding trên mobile cho header) */}
                <div className="flex-1 h-full pt-14 md:pt-0 overflow-hidden flex flex-col">
                    <ChatWindow messages={messages} />
                </div>

                {/* Vùng Input */}
                <div className="w-full pb-4 px-2 md:px-0">
                    <InputBar onSend={sendMessage} isLoading={isLoading} loadingStage={loadingStage} />
                </div>

            </main>
        </div>
    );
};

export default ChatPage;
