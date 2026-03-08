import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { X, FileText, Loader2 } from 'lucide-react';
import Button from '../common/Button';

const DocumentViewerModal = ({ ten_van_ban, onClose }) => {
    const [content, setContent] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDocument = async () => {
            setIsLoading(true);
            try {
                const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                const response = await axios.get(`${apiURL}/document?ten_van_ban=${encodeURIComponent(ten_van_ban)}`);
                setContent(response.data.content);
            } catch (err) {
                console.error("Lỗi khi tải văn bản:", err);
                setError("Không thể tải toàn văn bản pháp luật này từ cơ sở dữ liệu.");
            } finally {
                setIsLoading(false);
            }
        };

        if (ten_van_ban) {
            fetchDocument();
        }
    }, [ten_van_ban]);

    if (!ten_van_ban) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
            <div className="bg-slate-900 border border-slate-700 shadow-2xl rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden relative">

                {/* Header Modal */}
                <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-800/50">
                    <h3 className="text-lg md:text-xl font-bold text-blue-300 flex items-center gap-3">
                        <FileText size={24} className="text-sky-400" />
                        {ten_van_ban}
                    </h3>
                    <button
                        onClick={onClose}
                        className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Body Modal */}
                <div className="flex-1 overflow-y-auto p-6 md:p-8 scrollbar-thin scrollbar-thumb-slate-700 bg-secondary/30 relative">

                    {isLoading ? (
                        <div className="flex flex-col items-center justify-center h-full text-slate-400 space-y-4">
                            <Loader2 size={40} className="animate-spin text-sky-400" />
                            <p>Đang tải dữ liệu văn bản từ Database...</p>
                        </div>
                    ) : error ? (
                        <div className="bg-red-500/10 border border-red-500/30 text-red-300 p-4 rounded-xl text-center">
                            {error}
                        </div>
                    ) : (
                        <div className="text-slate-300 text-base md:text-lg leading-relaxed whitespace-pre-wrap font-serif">
                            {content}
                        </div>
                    )}
                </div>

                {/* Footer Modal */}
                <div className="p-4 border-t border-slate-800 bg-slate-800/30 flex justify-end">
                    <Button onClick={onClose} variant="secondary">Đóng</Button>
                </div>
            </div>
        </div>
    );
};

export default DocumentViewerModal;
