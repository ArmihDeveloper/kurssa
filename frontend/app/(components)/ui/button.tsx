import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'interactive';
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className, ...props }) => {
  const baseStyle = "font-poppins py-2 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2";

  let variantStyle = "";
  switch (variant) {
    case 'primary':
      variantStyle = "bg-primary text-white hover:bg-blue-700 focus:ring-primary";
      break;
    case 'secondary':
      variantStyle = "bg-secondary text-white hover:bg-green-700 focus:ring-secondary";
      break;
    case 'accent':
      variantStyle = "bg-accent text-white hover:bg-orange-700 focus:ring-accent";
      break;
    case 'interactive':
      variantStyle = "bg-interactive text-white hover:bg-purple-800 focus:ring-interactive";
      break;
    default:
      variantStyle = "bg-primary text-white hover:bg-blue-700 focus:ring-primary";
  }

  return (
    <button className={`${baseStyle} ${variantStyle} ${className}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
