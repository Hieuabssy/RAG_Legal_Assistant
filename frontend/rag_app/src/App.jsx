import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import DocumentViewerModal from './components/chat/DocumentViewerModal';

function App() {
  const [activeDocument, setActiveDocument] = useState(null);

  useEffect(() => {
    // Expose a global function to be called from deep components easily 
    // without prop drilling just for this simple modal.
    window.openDocumentModal = (docName) => {
      setActiveDocument(docName);
    };
    return () => {
      delete window.openDocumentModal;
    };
  }, []);

  return (
    <Router>
      <div className="font-sans text-slate-100 bg-secondary min-h-screen">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>

        {/* Global Document Viewer Modal */}
        <DocumentViewerModal
          ten_van_ban={activeDocument}
          onClose={() => setActiveDocument(null)}
        />
      </div>
    </Router>
  );
}

export default App;
