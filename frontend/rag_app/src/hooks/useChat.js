import { useState } from 'react';
import axios from 'axios';

// Định dạng chung của một Message: { role: 'user' | 'ai', content: str, results?: array, rewritten_query?: str }
export const useChat = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [loadingStage, setLoadingStage] = useState('');

    const stages = [
        "Đang viết lại truy vấn (LLM)...",
        "Đang nhúng ngữ nghĩa (Embedding)...",
        "Đang tìm kiếm hỗn hợp (Vector + BM25)...",
        "Đang xếp hạng kết quả (Reranking)..."
    ];

    const sendMessage = async (query) => {
        if (!query.trim()) return;

        // Thêm tin nhắn của user vào hội thoại
        const newUserMsg = { role: 'user', content: query };
        setMessages(prev => [...prev, newUserMsg]);
        setIsLoading(true);
        setError(null);

        // Hiệu ứng Loading
        let stageIdx = 0;
        setLoadingStage(stages[0]);
        const interval = setInterval(() => {
            stageIdx = (stageIdx + 1) % stages.length;
            setLoadingStage(stages[stageIdx]);
        }, 1200);

        try {
            // Giao tiếp với FastAPI Backend chạy qua biến môi trường
            const apiURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await axios.post(`${apiURL}/search`, {
                query: query
            });

            const data = response.data;

            // Lời giải thích mặc định của AI cho nội dung 
            let aiContent = "Dưới đây là các kết quả pháp lý liên quan đến câu hỏi của bạn:";
            if (!data.results || data.results.length === 0) {
                aiContent = "Xin lỗi, tôi không tìm thấy văn bản pháp lý nào phù hợp với câu hỏi của bạn.";
            }

            // Thêm kết quả của AI trả về
            const newAiMsg = {
                role: 'ai',
                content: data.generated_answer || aiContent,
                rewritten_query: data.rewritten_query, // Truy vấn đã viết lại nhờ RAG LLM
                results: data.results // Các văn bản trả ra từ VectorDB/BM25 + Rerank
            };

            setMessages(prev => [...prev, newAiMsg]);

        } catch (err) {
            console.error("Lỗi khi tìm kiếm:", err);
            setError("Đã xảy ra lỗi kết nối với hệ thống máy chủ RAG!");
            // Vẫn add AI Message báo lỗi
            setMessages(prev => [...prev, {
                role: 'ai',
                content: "Xin lỗi, đã xảy ra lỗi trong quá trình kết nối với cơ sở dữ liệu pháp luật. Vui lòng thử lại sau.",
                error: true
            }]);
        } finally {
            clearInterval(interval);
            setIsLoading(false);
            setLoadingStage('');
        }
    };

    return {
        messages,
        isLoading,
        error,
        loadingStage,
        sendMessage
    };
};
