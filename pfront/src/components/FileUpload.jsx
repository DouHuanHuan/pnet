import React from 'react';

const FileUpload = ({onFileSelect}) => {
    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <section className="file-section">
            <h2>选择DICOM文件</h2>
            <div className="file-input-container">
                <input
                    type="file"
                    id="dicom-file"
                    accept=".toml"
                    onChange={handleFileChange}
                />
                <label htmlFor="dicom-file" className="file-label">
                    点击选择文件
                </label>
            </div>
        </section>
    );
};

export default FileUpload;