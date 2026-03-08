import React from 'react';

const Spinner = ({ size = 'md', className = '' }) => {
    const sizes = {
        sm: "w-4 h-4 border-2",
        md: "w-8 h-8 border-4",
        lg: "w-12 h-12 border-4"
    };

    return (
        <div className={`flex items-center justify-center ${className}`}>
            <div
                className={`${sizes[size]} border-slate-700 border-t-sky-400 rounded-full animate-spin`}
            />
        </div>
    );
};

export default Spinner;
