'use client';

import React, { useState } from 'react';
import { FiSearch, FiBell, FiMoon, FiSun, FiMenu } from 'react-icons/fi';
import { FaUserCircle } from 'react-icons/fa';
import Badge from '../ui/Badge';

interface HeaderProps {
	onMenuClick?: () => void;
	showMenuButton?: boolean;
}

const Header = ({ onMenuClick, showMenuButton = false }: HeaderProps) => {
	const [isDark, setIsDark] = useState(false);
	const [searchQuery, setSearchQuery] = useState('');
	const [showNotifications, setShowNotifications] = useState(false);
	const [showProfile, setShowProfile] = useState(false);

	const toggleTheme = () => {
		setIsDark(!isDark);
		// In a real app, this would update the theme context
		document.documentElement.classList.toggle('dark');
	};

	const notifications = [
		{ id: 1, message: 'New appointment scheduled', time: '5 min ago', unread: true },
		{ id: 2, message: 'Lab results available for Patient #1234', time: '1 hour ago', unread: true },
		{ id: 3, message: 'Meeting reminder at 3:00 PM', time: '2 hours ago', unread: false },
	];

	const unreadCount = notifications.filter(n => n.unread).length;

	return (
		<header className="sticky top-0 z-[1100] bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 h-16">
			<div className="h-full px-4 flex items-center justify-between gap-4">
				{/* Left Section */}
				<div className="flex items-center gap-4 flex-1">
					{showMenuButton && (
						<button
							onClick={onMenuClick}
							className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 lg:hidden"
							aria-label="Open menu"
						>
							<FiMenu size={24} />
						</button>
					)}

					{/* Search Bar */}
					<div className="hidden md:flex items-center flex-1 max-w-lg">
						<div className="relative w-full">
							<FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
							<input
								type="text"
								placeholder="Search patients, doctors, appointments... (⌘K)"
								value={searchQuery}
								onChange={(e) => setSearchQuery(e.target.value)}
								className="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 border border-transparent rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:text-gray-200 placeholder-gray-500"
							/>
						</div>
					</div>
				</div>

				{/* Right Section */}
				<div className="flex items-center gap-2">
					{/* Search Icon (Mobile) */}
					<button
						className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 md:hidden"
						aria-label="Search"
					>
						<FiSearch size={20} />
					</button>

					{/* Theme Toggle */}
					<button
						onClick={toggleTheme}
						className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300"
						aria-label="Toggle theme"
					>
						{isDark ? <FiSun size={20} /> : <FiMoon size={20} />}
					</button>

					{/* Notifications */}
					<div className="relative">
						<button
							onClick={() => setShowNotifications(!showNotifications)}
							className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300 relative"
							aria-label="Notifications"
						>
							<FiBell size={20} />
							{unreadCount > 0 && (
								<span className="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
							)}
						</button>

						{/* Notifications Dropdown */}
						{showNotifications && (
							<div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg animate-scale-in">
								<div className="p-4 border-b border-gray-200 dark:border-gray-700">
									<div className="flex items-center justify-between">
										<h3 className="font-semibold text-gray-900 dark:text-white">Notifications</h3>
										{unreadCount > 0 && (
											<Badge variant="danger" size="sm">{unreadCount} new</Badge>
										)}
									</div>
								</div>
								<div className="max-h-96 overflow-y-auto">
									{notifications.map((notification) => (
										<div
											key={notification.id}
											className={`p-4 border-b border-gray-100 dark:border-gray-700 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer ${notification.unread ? 'bg-primary-50/50 dark:bg-primary-900/10' : ''
												}`}
										>
											<p className="text-sm text-gray-900 dark:text-white font-medium">
												{notification.message}
											</p>
											<p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
												{notification.time}
											</p>
										</div>
									))}
								</div>
								<div className="p-3 border-t border-gray-200 dark:border-gray-700">
									<button className="text-sm text-primary-600 dark:text-primary-400 hover:underline w-full text-center">
										View all notifications
									</button>
								</div>
							</div>
						)}
					</div>

					{/* User Profile */}
					<div className="relative">
						<button
							onClick={() => setShowProfile(!showProfile)}
							className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
							aria-label="User menu"
						>
							<FaUserCircle size={32} className="text-gray-600 dark:text-gray-400" />
							<div className="hidden lg:block text-left">
								<p className="text-sm font-medium text-gray-900 dark:text-white">Dr. Sarah Smith</p>
								<p className="text-xs text-gray-500 dark:text-gray-400">Administrator</p>
							</div>
						</button>

						{/* Profile Dropdown */}
						{showProfile && (
							<div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg animate-scale-in">
								<div className="p-4 border-b border-gray-200 dark:border-gray-700">
									<p className="font-semibold text-gray-900 dark:text-white">Dr. Sarah Smith</p>
									<p className="text-sm text-gray-500 dark:text-gray-400">sarah.smith@hospital.com</p>
								</div>
								<div className="py-2">
									<a href="/profile" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
										My Profile
									</a>
									<a href="/settings" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
										Settings
									</a>
									<a href="/help" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
										Help & Support
									</a>
								</div>
								<div className="border-t border-gray-200 dark:border-gray-700 py-2">
									<button className="block w-full text-left px-4 py-2 text-sm text-danger-600 dark:text-danger-400 hover:bg-gray-100 dark:hover:bg-gray-700">
										Logout
									</button>
								</div>
							</div>
						)}
					</div>
				</div>
			</div>

			{/* Click outside to close dropdowns */}
			{(showNotifications || showProfile) && (
				<div
					className="fixed inset-0 z-[-1]"
					onClick={() => {
						setShowNotifications(false);
						setShowProfile(false);
					}}
				/>
			)}
		</header>
	);
};

export default Header;
