import React, { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';
import { ShieldCheck, Scale, History } from 'lucide-react';

const ChatWindow = ({ messages }) => {
    const bottomRef = useRef(null);

    // Tự động cuộn xuống cuối khi có tin nhắn mới
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent flex flex-col items-center">
            <div className="w-full max-w-4xl flex flex-col space-y-8">

                {/* Lời chào Welcome Header */}
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full min-h-[50vh] animate-fade-in space-y-6 opacity-80">
                        <div className="w-20 h-20 rounded-full bg-indigo-500/10 border border-indigo-400/20 flex items-center justify-center shadow-lg shadow-indigo-500/10">
                            <Scale size={40} className="text-indigo-400" />
                        </div>
                        <div className="text-center space-y-3">
                            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Trợ Lý Pháp Luật AI</h2>
                            <p className="text-sm text-slate-400 max-w-md mx-auto leading-relaxed">
                                Xin chào! Tôi có thể giúp bạn tra cứu nhanh các điều luật, quy định hình sự và hành chính. Hãy đặt câu hỏi bất kỳ.
                            </p>
                        </div>
                        <div className="flex flex-wrap justify-center gap-3 w-full max-w-lg mt-6">
                            {[
                                "Trộm chó bị phạt bao nhiêu tiền?",
                                "Vượt đèn đỏ xe máy phạt sao?",
                                "Tội lừa đảo chiếm đoạt tài sản qua mạng?"
                            ].map((hint, idx) => (
                                <div key={idx} className="bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-2 text-xs text-slate-300 hover:bg-slate-700 cursor-pointer transition">
                                    "{hint}"
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Danh sách tin nhắn */}
                {messages.map((msg, idx) => (
                    <MessageItem key={idx} message={msg} />
                ))}

                {/* Div ẩn để auto scroll */}
                <div ref={bottomRef} className="h-4" />
            </div>
        </div>
    );
};

export default ChatWindow;
