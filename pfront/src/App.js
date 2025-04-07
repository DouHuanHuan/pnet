import React, {useState} from 'react';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import StatusIndicator from './components/StatusIndicator';
import './styles/main.css';
import {handleFileSelect, handlePredict} from './handler/file-handler';

function App() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState(null);

    return (
        <div className="app">
            <Header/>

            <main className="main-content">
                <FileUpload onFileSelect={handleFileSelect(setFile, setStatus)}/>

                <button
                    className={`predict-button ${!file ? 'disabled' : ''}`}
                    onClick={handlePredict(file, setStatus)}
                    disabled={!file}
                >
                    开始预测
                </button>

                <StatusIndicator status={status}/>
            </main>
        </div>
    );
}

export default App;