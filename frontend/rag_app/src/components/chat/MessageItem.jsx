import React from 'react';
import { Bot, User, Scale, AlertCircle, FileText, Bookmark, Settings2, Sparkles } from 'lucide-react';
import SourceCard from './SourceCard';

// Hook nhỏ để giả lập hiệu ứng gõ chữ
const TypingText = ({ text }) => {
    const [displayedText, setDisplayedText] = React.useState('');

    React.useEffect(() => {
        let i = 0;
        const interval = setInterval(() => {
            setDisplayedText(text.slice(0, i));
            i++;
            if (i > text.length) clearInterval(interval);
        }, 20); // Tốc độ gõ
        return () => clearInterval(interval);
    }, [text]);

    return <span>{displayedText}</span>;
};

// Component Bong bóng chat
const MessageItem = ({ message }) => {
    const isUser = message.role === 'user';
    const isError = message.error;

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}>
            <div className={`flex max-w-[85%] md:max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-4`}>

                {/* Avatar */}
                <div className={`p-2 rounded-xl shrink-0 ${isUser ? 'bg-indigo-600' : 'bg-slate-700/80 border border-slate-600'}`}>
                    {isUser ? <User size={20} className="text-white" /> : <Bot size={20} className={isError ? "text-red-400" : "text-sky-400"} />}
                </div>

                {/* Nội dung */}
                <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} space-y-3`}>

                    {/* Bong bóng chính */}
                    <div className={`px-5 py-3.5 rounded-2xl shadow-lg border ${isUser
                        ? 'bg-indigo-600 text-white rounded-tr-none border-indigo-500/50'
                        : isError
                            ? 'bg-red-500/10 border-red-500/30 text-slate-200 rounded-tl-none'
                            : 'glass text-slate-200 rounded-tl-none'
                        }`}>
                        {isUser ? (
                            <p className="text-base md:text-lg leading-relaxed whitespace-pre-wrap">{message.content}</p>
                        ) : (
                            <p className="text-[15px] leading-relaxed whitespace-pre-wrap">
                                {/* Nếu load xong, chạy hiêu ứng gõ cho AI context */}
                                <TypingText text={message.content} />
                            </p>
                        )}

                        {/* Cảnh báo lỗi */}
                        {isError && (
                            <div className="mt-2 text-xs flex items-center text-red-400">
                                <AlertCircle size={14} className="mr-1" />
                                Bạn cần bật API chạy trên port 8000
                            </div>
                        )}
                    </div>

                    {/* RAG Specific UI Element - Card diễn giải (Rewriting) và Căn cứ pháp lý (Sources) */}
                    {!isUser && !isError && message.rewritten_query && (
                        <div className="w-full flex justify-start pl-2 animate-fade-in" style={{ animationDelay: '0.8s', animationFillMode: 'both' }}>
                            <div className="bg-slate-800/60 border border-sky-400/20 px-4 py-3 rounded-xl max-w-sm flex items-start gap-3">
                                <Sparkles size={16} className="text-sky-400 shrink-0 mt-0.5" />
                                <div>
                                    <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block mb-1">Truy vấn đã phân tích (LLM)</span>
                                    <p className="text-sm text-sky-200 font-medium italic">"{message.rewritten_query}"</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Nguồn luật RAG trả về (Sources) */}
                    {!isUser && message.results && message.results.length > 0 && (
                        <div className="w-full mt-2 animate-fade-in" style={{ animationDelay: '1.2s', animationFillMode: 'both' }}>
                            <div className="flex items-center text-slate-400 text-sm mb-3">
                                <Scale size={16} className="mr-2 text-indigo-400" />
                                <span className="font-semibold uppercase tracking-wider text-xs">Căn cứ pháp lý ({message.results.length})</span>
                            </div>
                            <div className="flex flex-col gap-3">
                                {message.results.map((doc, idx) => (
                                    <SourceCard key={doc.id || idx} doc={doc} index={idx} />
                                ))}
                            </div>
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};

export default MessageItem;
