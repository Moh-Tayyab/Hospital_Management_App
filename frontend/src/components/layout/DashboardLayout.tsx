'use client';

import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface DashboardLayoutProps {
	children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
	const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
	const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

	const toggleSidebar = () => {
		setIsSidebarCollapsed(!isSidebarCollapsed);
	};

	const toggleMobileSidebar = () => {
		setIsMobileSidebarOpen(!isMobileSidebarOpen);
	};

	return (
		<div className="min-h-screen bg-gray-50 dark:bg-dark-bg">
			{/* Desktop Sidebar */}
			<div className="hidden lg:block">
				<Sidebar isCollapsed={isSidebarCollapsed} onToggle={toggleSidebar} />
			</div>

			{/* Mobile Sidebar */}
			{isMobileSidebarOpen && (
				<>
					{/* Mobile Overlay */}
					<div
						className="fixed inset-0 bg-black/50 z-[1099] lg:hidden animate-fade-in"
						onClick={toggleMobileSidebar}
					/>
					{/* Mobile Sidebar Drawer */}
					<div className="lg:hidden animate-slide-right">
						<Sidebar />
					</div>
				</>
			)}

			{/* Main Content Area */}
			<div
				className={`transition-all duration-300 ${isSidebarCollapsed ? 'lg:ml-20' : 'lg:ml-64'
					}`}
			>
				<Header
					onMenuClick={toggleMobileSidebar}
					showMenuButton={true}
				/>

				<main className="p-4 md:p-6 lg:p-8">
					<div className="max-w-7xl mx-auto">
						{children}
					</div>
				</main>
			</div>
		</div>
	);
};

export default DashboardLayout;
