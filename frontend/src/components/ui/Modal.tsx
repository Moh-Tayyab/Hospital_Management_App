'use client';

import React, { useEffect, useRef } from 'react';
import { FiX } from 'react-icons/fi';

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface ModalProps {
	isOpen: boolean;
	onClose: () => void;
	title?: string;
	children: React.ReactNode;
	size?: ModalSize;
	showCloseButton?: boolean;
	closeOnBackdropClick?: boolean;
	closeOnEscape?: boolean;
	footer?: React.ReactNode;
}

const Modal = ({
	isOpen,
	onClose,
	title,
	children,
	size = 'md',
	showCloseButton = true,
	closeOnBackdropClick = true,
	closeOnEscape = true,
	footer,
}: ModalProps) => {
	const modalRef = useRef<HTMLDivElement>(null);
	const previousActiveElement = useRef<HTMLElement | null>(null);

	const sizeStyles = {
		sm: 'max-w-md',
		md: 'max-w-lg',
		lg: 'max-w-2xl',
		xl: 'max-w-4xl',
		full: 'max-w-full m-4',
	};

	// Handle escape key
	useEffect(() => {
		if (!isOpen || !closeOnEscape) return;

		const handleEscape = (e: KeyboardEvent) => {
			if (e.key === 'Escape') {
				onClose();
			}
		};

		document.addEventListener('keydown', handleEscape);
		return () => document.removeEventListener('keydown', handleEscape);
	}, [isOpen, closeOnEscape, onClose]);

	// Handle focus trap
	useEffect(() => {
		if (!isOpen) return;

		// Store previously focused element
		previousActiveElement.current = document.activeElement as HTMLElement;

		// Focus first focusable element in modal
		const focusableElements = modalRef.current?.querySelectorAll(
			'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
		);

		if (focusableElements && focusableElements.length > 0) {
			(focusableElements[0] as HTMLElement).focus();
		}

		// Restore focus on unmount
		return () => {
			previousActiveElement.current?.focus();
		};
	}, [isOpen]);

	// Prevent body scroll when modal is open
	useEffect(() => {
		if (isOpen) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}

		return () => {
			document.body.style.overflow = '';
		};
	}, [isOpen]);

	if (!isOpen) return null;

	const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
		if (closeOnBackdropClick && e.target === e.currentTarget) {
			onClose();
		}
	};

	return (
		<div
			className="fixed inset-0 z-[1300] flex items-center justify-center p-4 animate-fade-in"
			onClick={handleBackdropClick}
			aria-modal="true"
			role="dialog"
			aria-labelledby={title ? 'modal-title' : undefined}
		>
			{/* Backdrop */}
			<div className="absolute inset-0 bg-black/50 backdrop-blur-sm" aria-hidden="true" />

			{/* Modal Container */}
			<div
				ref={modalRef}
				className={`relative bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full ${sizeStyles[size]} animate-scale-in`}
			>
				{/* Header */}
				{(title || showCloseButton) && (
					<div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
						{title && (
							<h2
								id="modal-title"
								className="text-xl font-semibold text-gray-900 dark:text-gray-100"
							>
								{title}
							</h2>
						)}
						{showCloseButton && (
							<button
								onClick={onClose}
								className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
								aria-label="Close modal"
							>
								<FiX size={24} />
							</button>
						)}
					</div>
				)}

				{/* Body */}
				<div className="px-6 py-4 max-h-[calc(100vh-200px)] overflow-y-auto">
					{children}
				</div>

				{/* Footer */}
				{footer && (
					<div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
						{footer}
					</div>
				)}
			</div>
		</div>
	);
};

export default Modal;
