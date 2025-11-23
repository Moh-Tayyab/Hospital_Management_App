import React, { ButtonHTMLAttributes, forwardRef } from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
	variant?: ButtonVariant;
	size?: ButtonSize;
	isLoading?: boolean;
	leftIcon?: React.ReactNode;
	rightIcon?: React.ReactNode;
	fullWidth?: boolean;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
	(
		{
			variant = 'primary',
			size = 'md',
			isLoading = false,
			leftIcon,
			rightIcon,
			fullWidth = false,
			children,
			className = '',
			disabled,
			...props
		},
		ref
	) => {
		const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none';

		const variantStyles = {
			primary: 'bg-gradient-to-br from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 focus:ring-primary-500 shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0',
			secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-400 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700',
			outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500 dark:border-primary-400 dark:text-primary-400 dark:hover:bg-primary-950',
			ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-400 dark:text-gray-300 dark:hover:bg-gray-800',
			danger: 'bg-danger-600 text-white hover:bg-danger-700 focus:ring-danger-500 shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0',
		};

		const sizeStyles = {
			sm: 'px-3 py-1.5 text-sm rounded-md gap-1.5',
			md: 'px-4 py-2 text-base rounded-lg gap-2',
			lg: 'px-6 py-3 text-lg rounded-lg gap-2.5',
		};

		const widthStyles = fullWidth ? 'w-full' : '';

		const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${widthStyles} ${className}`;

		return (
			<button
				ref={ref}
				className={combinedClassName}
				disabled={disabled || isLoading}
				{...props}
			>
				{isLoading ? (
					<>
						<svg
							className="animate-spin h-4 w-4"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle
								className="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								strokeWidth="4"
							></circle>
							<path
								className="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							></path>
						</svg>
						<span>Loading...</span>
					</>
				) : (
					<>
						{leftIcon && <span className="flex-shrink-0">{leftIcon}</span>}
						{children}
						{rightIcon && <span className="flex-shrink-0">{rightIcon}</span>}
					</>
				)}
			</button>
		);
	}
);

Button.displayName = 'Button';

export default Button;
