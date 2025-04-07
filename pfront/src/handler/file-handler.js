export const handleFileSelect = (setFile, setStatus) => async (selectedFile) => {
    setFile(selectedFile);
    setStatus('uploading');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('http://localhost:8000/api/upload/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            console.error('上传失败');
            setStatus('upload_failed');
            return;
        }

        const result = await response.json();
        console.log('上传成功，返回结果：', result);

        setStatus('uploaded');
    } catch (error) {
        console.error('上传出错:', error);
        setStatus('upload_failed');
    }
};


export const handlePredict = (file, setStatus) => () => {
    if (!file) return;

    setStatus('processing');

    setTimeout(() => {
        setStatus('completed');
    }, 2000);
};
