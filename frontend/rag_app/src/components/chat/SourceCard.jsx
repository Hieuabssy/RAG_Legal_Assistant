import React from 'react';
import { FileText, Bookmark, Target } from 'lucide-react';

const SourceCard = ({ doc, index }) => {
    // Lấy dữ liệu an toàn
    const docName = doc.ten_van_ban || 'Không rõ tên văn bản';
    const content = doc.page_content || 'Không có nội dung';
    const score = doc.rerank_score ? doc.rerank_score.toFixed(4) : "N/A";

    return (
        <div
            className="bg-slate-800/80 rounded-xl p-5 border border-slate-700/50 hover:border-slate-600 transition-colors shadow-lg group"
            style={{ animationDelay: `${index * 0.1 + 1.2}s`, animationFillMode: 'both' }}
        >
            <div className="flex items-start justify-between mb-3 gap-4">
                <h4 className="text-blue-300 font-bold text-lg flex-1 leading-snug">
                    <FileText size={18} className="inline mr-1.5 align-text-bottom text-indigo-400" />
                    <button
                        onClick={() => window.openDocumentModal(docName)}
                        className="hover:underline hover:text-sky-300 transition-colors text-left"
                    >
                        {docName}
                    </button>
                </h4>
            </div>

            <div className="bg-slate-900/50 p-5 rounded-lg text-slate-200 text-sm md:text-base leading-relaxed border border-slate-800 overflow-y-auto max-h-64 group-hover:bg-slate-900/80 transition-colors scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
                {/* Render dấu xuống dòng an toàn */}
                {content.split('\n').map((line, i) => (
                    <React.Fragment key={i}>
                        {line}
                        <br />
                    </React.Fragment>
                ))}
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
                {doc.chu_de && (
                    <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-1 rounded border border-slate-700 flex items-center">
                        <Bookmark size={10} className="mr-1" /> {doc.chu_de}
                    </span>
                )}
                {doc.loai_van_ban && (
                    <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-1 rounded border border-slate-700 flex items-center">
                        <FileText size={10} className="mr-1" /> {doc.loai_van_ban}
                    </span>
                )}
                {doc.link_goc && (
                    <a href={doc.link_goc} target="_blank" rel="noreferrer" className="text-[10px] text-sky-400 hover:text-sky-300 hover:bg-sky-900/40 bg-slate-800 px-2 py-1 rounded border border-slate-700 hover:border-sky-500/50 flex items-center transition-colors">
                        <Target size={10} className="mr-1" /> Xem bản gốc
                    </a>
                )}
            </div>
        </div>
    );
};

export default SourceCard;
