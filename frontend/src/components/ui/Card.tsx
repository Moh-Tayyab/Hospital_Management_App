import React, { HTMLAttributes } from 'react';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
	variant?: 'default' | 'bordered' | 'elevated';
	padding?: 'none' | 'sm' | 'md' | 'lg';
	hoverable?: boolean;
}

export interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
	divider?: boolean;
}

export interface CardBodyProps extends HTMLAttributes<HTMLDivElement> { }

export interface CardFooterProps extends HTMLAttributes<HTMLDivElement> {
	divider?: boolean;
	align?: 'left' | 'center' | 'right';
}

const Card = ({
	variant = 'default',
	padding = 'md',
	hoverable = false,
	className = '',
	children,
	...props
}: CardProps) => {
	const baseStyles = 'bg-white rounded-lg transition-all duration-200 dark:bg-gray-800';

	const variantStyles = {
		default: 'border border-gray-200 shadow-sm dark:border-gray-700',
		bordered: 'border-2 border-gray-200 dark:border-gray-700',
		elevated: 'shadow-md',
	};

	const paddingStyles = {
		none: '',
		sm: 'p-4',
		md: 'p-6',
		lg: 'p-8',
	};

	const hoverStyles = hoverable
		? 'hover:shadow-lg hover:-translate-y-1 cursor-pointer'
		: '';

	const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${paddingStyles[padding]} ${hoverStyles} ${className}`;

	return (
		<div className={combinedClassName} {...props}>
			{children}
		</div>
	);
};

const CardHeader = ({
	divider = false,
	className = '',
	children,
	...props
}: CardHeaderProps) => {
	const baseStyles = 'mb-4';
	const dividerStyles = divider ? 'pb-4 border-b border-gray-200 dark:border-gray-700' : '';

	return (
		<div className={`${baseStyles} ${dividerStyles} ${className}`} {...props}>
			{children}
		</div>
	);
};

const CardBody = ({ className = '', children, ...props }: CardBodyProps) => {
	return (
		<div className={className} {...props}>
			{children}
		</div>
	);
};

const CardFooter = ({
	divider = false,
	align = 'right',
	className = '',
	children,
	...props
}: CardFooterProps) => {
	const baseStyles = 'mt-4';
	const dividerStyles = divider ? 'pt-4 border-t border-gray-200 dark:border-gray-700' : '';

	const alignStyles = {
		left: 'text-left',
		center: 'text-center',
		right: 'text-right',
	};

	return (
		<div className={`${baseStyles} ${dividerStyles} ${alignStyles[align]} ${className}`} {...props}>
			{children}
		</div>
	);
};

// Compound component pattern
Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

export default Card;
