import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Scale, Zap, ShieldCheck, Database, ArrowRight } from 'lucide-react';
import Button from '../components/common/Button';

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen relative flex flex-col items-center justify-center overflow-hidden">

            {/* Background Decorators */}
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600 rounded-full blur-[150px] opacity-20 pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-sky-400 rounded-full blur-[150px] opacity-10 pointer-events-none"></div>

            {/* Navbar (Mini) */}
            <nav className="absolute top-0 w-full p-6 flex justify-between items-center z-20">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-sky-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <Scale className="text-white" size={20} />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight text-white">Legal<span className="text-sky-400">AI</span></h1>
                </div>
                <div className="glass px-4 py-2 rounded-full text-sm font-medium flex items-center shadow-lg">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></div>
                    System Online
                </div>
            </nav>

            <main className="z-10 text-center px-4 w-full flex flex-col items-center max-w-5xl">

                {/* Banner */}
                <div className="inline-flex glass px-4 py-2 rounded-full mb-8 items-center text-sm font-medium animate-fade-in shadow-xl backdrop-blur-md">
                    <SparklesIcon className="w-4 h-4 text-sky-400 mr-2" />
                    <span className="text-slate-200">Retrieval-Augmented Generation (RAG) 2.0</span>
                </div>

                {/* Hero Section */}
                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 animate-fade-in" style={{ animationDelay: '0.1s', animationFillMode: 'both' }}>
                    Tra Cứu Pháp Luật <br className="hidden md:block" />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-indigo-500">Thông Minh & Tức Thì</span>
                </h1>

                <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-in" style={{ animationDelay: '0.2s', animationFillMode: 'both' }}>
                    Hệ thống được hỗ trợ bởi AI (Gemini 1.5 Flash) kết hợp công nghệ Hybrid Search (Vector + BM25)
                    nhằm đem lại kết quả trích dẫn pháp lý chính xác và trực quan nhất.
                </p>

                {/* CTA Button */}
                <div className="animate-fade-in" style={{ animationDelay: '0.3s', animationFillMode: 'both' }}>
                    <Button
                        onClick={() => navigate('/chat')}
                        className="text-lg px-8 py-4 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white shadow-xl shadow-indigo-500/25 border-none transform hover:scale-105 transition-all"
                    >
                        Bắt Đầu Tra Cứu <ArrowRight className="ml-2" size={20} />
                    </Button>
                </div>

                {/* Features grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-24 animate-fade-in" style={{ animationDelay: '0.5s', animationFillMode: 'both' }}>
                    <FeatureCard
                        icon={<Zap size={24} className="text-yellow-400" />}
                        title="Truy Vấn Tự Nhiên"
                        desc="Cho phép người dùng hỏi bằng ngôn ngữ tự nhiên, tiếng lóng. LLM sẽ tự động phân tích và viết lại."
                    />
                    <FeatureCard
                        icon={<ShieldCheck size={24} className="text-emerald-400" />}
                        title="Độ Chính Xác Cao"
                        desc="Mô hình BAAI Cross-encoder Reranking chấm điểm lại độ liên quan để chọn ra Top 5 văn bản tốt nhất."
                    />
                    <FeatureCard
                        icon={<Database size={24} className="text-indigo-400" />}
                        title="Hybrid Vector Search"
                        desc="Kết hợp tìm kiếm ngữ nghĩa (M3/SBERT) và tìm kiếm từ khóa chéo (BM25) trên CSDL PostgreSQL."
                    />
                </div>

            </main>
        </div>
    );
};

// UI Component nhỏ cho features
const FeatureCard = ({ icon, title, desc }) => (
    <div className="glass p-6 rounded-2xl text-left border border-slate-700/50 hover:bg-slate-800/50 transition duration-300 shadow-xl group">
        <div className="w-12 h-12 bg-slate-800/80 rounded-xl flex items-center justify-center mb-4 border border-slate-700 shadow-inner group-hover:scale-110 transition-transform">
            {icon}
        </div>
        <h3 className="text-xl font-bold text-slate-100 mb-2">{title}</h3>
        <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
    </div>
);

const SparklesIcon = (props) => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
        <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z" />
    </svg>
)

export default HomePage;
