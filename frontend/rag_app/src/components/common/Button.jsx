import React from 'react';

const Button = ({
    children,
    onClick,
    type = 'button',
    variant = 'primary',
    className = '',
    disabled = false,
    ...props
}) => {
    const baseStyles = "px-6 py-2.5 rounded-xl font-semibold transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary: "bg-sky-400 hover:bg-sky-500 text-slate-900 shadow-lg shadow-sky-400/20",
        secondary: "glass text-white hover:bg-slate-800/80 border border-slate-700",
        ghost: "text-slate-400 hover:text-white hover:bg-slate-800",
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${baseStyles} ${variants[variant]} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};

export default Button;
