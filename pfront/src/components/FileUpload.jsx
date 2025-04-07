import React, {useState} from 'react';

const FileUpload = ({onFileSelect}) => {
    const [selectedFileName, setSelectedFileName] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            setSelectedFileName(file.name);
            onFileSelect(file);
        }
    };

    return (
        <section className="file-section">
            <h2>选择 DICOM 文件</h2>
            <div className="file-input-container">
                <input
                    type="file"
                    id="dicom-file"
                    accept=".toml"
                    onChange={handleFileChange}
                    style={{display: 'none'}}
                />
                <label htmlFor="dicom-file" className="file-label">
                    点击选择文件
                </label>
                {selectedFileName && (
                    <div className="file-name-display">
                        已选择文件: <strong>{selectedFileName}</strong>
                    </div>
                )}
            </div>
        </section>
    );
};

export default FileUpload;
