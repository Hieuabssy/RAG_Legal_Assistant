import React, { useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';
import Button from '../common/Button';

const InputBar = ({ onSend, isLoading, loadingStage }) => {
    const [query, setQuery] = React.useState('');
    const inputRef = useRef(null);

    // Focus input khi load hoặc xong tin nhắn
    useEffect(() => {
        if (!isLoading && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isLoading]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim() && !isLoading) {
            onSend(query);
            setQuery('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto relative p-4 bg-secondary/80 backdrop-blur-md border-t border-slate-700/50 z-20">

            {/* Loading Indicator mỏng nhẹ */}
            {isLoading && (
                <div className="absolute -top-7 left-0 right-0 flex justify-center animate-fade-in pointer-events-none">
                    <div className="bg-slate-800 border border-sky-400/30 text-sky-300 text-xs px-4 py-1.5 rounded-full shadow-lg flex items-center shadow-sky-400/10">
                        <Sparkles size={12} className="mr-2 animate-pulse text-sky-400" />
                        <span className="font-medium tracking-wide">{loadingStage}</span>
                    </div>
                </div>
            )}

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="relative group flex items-end gap-3 glass rounded-2xl p-2 shadow-2xl transition-all focus-within:ring-2 focus-within:ring-sky-400/50">
                <textarea
                    ref={inputRef}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isLoading}
                    placeholder="Hỏi về bất kỳ điều khoản hình sự, hành chính hay dân sự nào..."
                    className="w-full max-h-[120px] min-h-[52px] bg-transparent text-slate-100 placeholder-slate-400 focus:outline-none resize-none px-4 py-3.5 text-[15px] scrollbar-thin scrollbar-thumb-slate-700"
                    rows={1}
                    style={{ height: 'auto' }}
                />
                <Button
                    type="submit"
                    disabled={!query.trim() || isLoading}
                    className="h-12 w-12 !p-0 shrink-0 rounded-xl"
                >
                    {isLoading ? (
                        <div className="w-5 h-5 border-2 border-slate-700 border-t-white rounded-full animate-spin" />
                    ) : (
                        <Send size={20} className="text-secondary ml-1" />
                    )}
                </Button>
            </form>
            <div className="text-center mt-3 text-[10px] text-slate-500 font-medium">
                Hệ thống RAG AI có thể mắc sai lầm. Hãy luôn tham chiếu trực tiếp với Căn cứ pháp lý.
            </div>
        </div>
    );
};

export default InputBar;
