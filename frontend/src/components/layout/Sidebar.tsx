'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
	FiHome,
	FiUsers,
	FiUserPlus,
	FiCalendar,
	FiFileText,
	FiActivity,
	FiSettings,
	FiLogOut,
	FiChevronLeft,
	FiChevronRight,
} from 'react-icons/fi';
import { FaUserMd, FaUserNurse, FaHospital } from 'react-icons/fa';

interface SidebarProps {
	isCollapsed?: boolean;
	onToggle?: () => void;
}

interface NavItem {
	href: string;
	icon: React.ReactNode;
	label: string;
	badge?: string;
}

const Sidebar = ({ isCollapsed = false, onToggle }: SidebarProps) => {
	const pathname = usePathname();

	const navItems: NavItem[] = [
		{ href: '/dashboard', icon: <FiHome size={20} />, label: 'Dashboard' },
		{ href: '/patients', icon: <FiUsers size={20} />, label: 'Patients' },
		{ href: '/doctors', icon: <FaUserMd size={20} />, label: 'Doctors' },
		{ href: '/nurses', icon: <FaUserNurse size={20} />, label: 'Nurses' },
		{ href: '/appointments', icon: <FiCalendar size={20} />, label: 'Appointments', badge: '12' },
		{ href: '/records', icon: <FiFileText size={20} />, label: 'Medical Records' },
		{ href: '/lab-tests', icon: <FiActivity size={20} />, label: 'Lab Tests', badge: '3' },
		{ href: '/departments', icon: <FaHospital size={20} />, label: 'Departments' },
	];

	const bottomNavItems: NavItem[] = [
		{ href: '/settings', icon: <FiSettings size={20} />, label: 'Settings' },
	];

	const isActive = (href: string) => pathname === href || pathname?.startsWith(href + '/');

	return (
		<aside
			className={`fixed left-0 top-0 h-screen bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transition-all duration-300 z-[1100] flex flex-col ${isCollapsed ? 'w-20' : 'w-64'
				}`}
		>
			{/* Logo Section */}
			<div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800">
				<Link href="/dashboard" className="flex items-center gap-3">
					<div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center text-white shadow-md">
						<FaHospital size={20} />
					</div>
					{!isCollapsed && (
						<span className="text-xl font-bold text-gray-900 dark:text-white">
							HealthMS
						</span>
					)}
				</Link>
				{!isCollapsed && onToggle && (
					<button
						onClick={onToggle}
						className="p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 dark:text-gray-400"
						aria-label="Collapse sidebar"
					>
						<FiChevronLeft size={20} />
					</button>
				)}
			</div>

			{/* Navigation Items */}
			<nav className="flex-1 overflow-y-auto py-4 px-2">
				<ul className="space-y-1">
					{navItems.map((item) => (
						<li key={item.href}>
							<Link
								href={item.href}
								className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group relative ${isActive(item.href)
										? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
										: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
									}`}
								title={isCollapsed ? item.label : undefined}
							>
								<span className="flex-shrink-0">{item.icon}</span>
								{!isCollapsed && (
									<>
										<span className="flex-1 font-medium">{item.label}</span>
										{item.badge && (
											<span className="px-2 py-0.5 text-xs font-semibold bg-danger-100 text-danger-700 dark:bg-danger-900 dark:text-danger-300 rounded-full">
												{item.badge}
											</span>
										)}
									</>
								)}
								{isCollapsed && item.badge && (
									<span className="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
								)}
								{/* Active indicator */}
								{isActive(item.href) && (
									<div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary-600 rounded-r-full"></div>
								)}
							</Link>
						</li>
					))}
				</ul>
			</nav>

			{/* Bottom Section */}
			<div className="border-t border-gray-200 dark:border-gray-800 p-2">
				<ul className="space-y-1 mb-2">
					{bottomNavItems.map((item) => (
						<li key={item.href}>
							<Link
								href={item.href}
								className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${isActive(item.href)
										? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
										: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
									}`}
								title={isCollapsed ? item.label : undefined}
							>
								<span className="flex-shrink-0">{item.icon}</span>
								{!isCollapsed && <span className="flex-1 font-medium">{item.label}</span>}
							</Link>
						</li>
					))}
				</ul>
				<button
					className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-all duration-200 ${isCollapsed ? 'justify-center' : ''
						}`}
					title={isCollapsed ? 'Logout' : undefined}
				>
					<FiLogOut size={20} />
					{!isCollapsed && <span className="font-medium">Logout</span>}
				</button>
			</div>

			{/* Expand Button (when collapsed) */}
			{isCollapsed && onToggle && (
				<button
					onClick={onToggle}
					className="absolute -right-3 top-20 w-6 h-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full flex items-center justify-center text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 shadow-md"
					aria-label="Expand sidebar"
				>
					<FiChevronRight size={14} />
				</button>
			)}
		</aside>
	);
};

export default Sidebar;
