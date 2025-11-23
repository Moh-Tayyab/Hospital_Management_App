import React, { HTMLAttributes } from 'react';

export type BadgeVariant = 'primary' | 'success' | 'danger' | 'warning' | 'info' | 'neutral';
export type BadgeSize = 'sm' | 'md';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
	variant?: BadgeVariant;
	size?: BadgeSize;
	dot?: boolean;
	icon?: React.ReactNode;
}

const Badge = ({
	variant = 'neutral',
	size = 'md',
	dot = false,
	icon,
	className = '',
	children,
	...props
}: BadgeProps) => {
	const baseStyles = 'inline-flex items-center font-medium rounded-full transition-colors duration-200';

	const sizeStyles = {
		sm: 'px-2 py-0.5 text-xs gap-1',
		md: 'px-2.5 py-1 text-sm gap-1.5',
	};

	const variantStyles = {
		primary: 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300',
		success: 'bg-success-100 text-success-700 dark:bg-success-900 dark:text-success-300',
		danger: 'bg-danger-100 text-danger-700 dark:bg-danger-900 dark:text-danger-300',
		warning: 'bg-warning-100 text-warning-700 dark:bg-warning-900 dark:text-warning-300',
		info: 'bg-info-100 text-info-700 dark:bg-info-900 dark:text-info-300',
		neutral: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300',
	};

	const dotColors = {
		primary: 'bg-primary-600',
		success: 'bg-success-600',
		danger: 'bg-danger-600',
		warning: 'bg-warning-600',
		info: 'bg-info-600',
		neutral: 'bg-gray-600',
	};

	const combinedClassName = `${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`;

	return (
		<span className={combinedClassName} {...props}>
			{dot && (
				<span
					className={`w-1.5 h-1.5 rounded-full ${dotColors[variant]}`}
					aria-hidden="true"
				/>
			)}
			{icon && <span className="flex-shrink-0">{icon}</span>}
			{children}
		</span>
	);
};

export default Badge;
