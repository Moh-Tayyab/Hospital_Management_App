import React, { InputHTMLAttributes, forwardRef } from 'react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
	label?: string;
	error?: string;
	helperText?: string;
	leftIcon?: React.ReactNode;
	rightIcon?: React.ReactNode;
	fullWidth?: boolean;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
	(
		{
			label,
			error,
			helperText,
			leftIcon,
			rightIcon,
			fullWidth = false,
			className = '',
			id,
			...props
		},
		ref
	) => {
		const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
		const hasError = !!error;

		const baseInputStyles = 'block w-full px-3 py-2 text-base border rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:bg-gray-100 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-600 dark:text-gray-100 dark:disabled:bg-gray-900';

		const stateStyles = hasError
			? 'border-danger-500 focus:border-danger-500 focus:ring-danger-200'
			: 'border-gray-300 focus:border-primary-500 focus:ring-primary-200 dark:focus:ring-primary-800';

		const paddingStyles = leftIcon && rightIcon
			? 'pl-10 pr-10'
			: leftIcon
				? 'pl-10'
				: rightIcon
					? 'pr-10'
					: '';

		const combinedInputClassName = `${baseInputStyles} ${stateStyles} ${paddingStyles} ${className}`;

		return (
			<div className={fullWidth ? 'w-full' : ''}>
				{label && (
					<label
						htmlFor={inputId}
						className="block text-sm font-medium text-gray-700 mb-1.5 dark:text-gray-300"
					>
						{label}
					</label>
				)}
				<div className="relative">
					{leftIcon && (
						<div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500">
							{leftIcon}
						</div>
					)}
					<input
						ref={ref}
						id={inputId}
						className={combinedInputClassName}
						aria-invalid={hasError}
						aria-describedby={
							error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined
						}
						{...props}
					/>
					{rightIcon && (
						<div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500">
							{rightIcon}
						</div>
					)}
				</div>
				{error && (
					<p
						id={`${inputId}-error`}
						className="mt-1.5 text-sm text-danger-600 dark:text-danger-400"
						role="alert"
					>
						{error}
					</p>
				)}
				{!error && helperText && (
					<p
						id={`${inputId}-helper`}
						className="mt-1.5 text-sm text-gray-600 dark:text-gray-400"
					>
						{helperText}
					</p>
				)}
			</div>
		);
	}
);

Input.displayName = 'Input';

export default Input;
