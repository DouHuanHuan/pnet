import React from 'react';

const StatusIndicator = ({ status }) => {
    if (status === 'processing') {
        return (
            <div className="status-message processing">
                <div className="spinner"></div>
                <span>处理中...</span>
            </div>
        );
    }

    if (status === 'completed') {
        return (
            <div className="status-message completed">
                <span>处理完毕</span>
            </div>
        );
    }

    return null;
};

export default StatusIndicator;