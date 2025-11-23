'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Navbar() {
	const router = useRouter();
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	useEffect(() => {
		const token = localStorage.getItem('access_token');
		setIsLoggedIn(!!token);
	}, []);

	const handleLogout = () => {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
		setIsLoggedIn(false);
		router.push('/login');
	};

	return (
		<nav className="bg-white shadow-lg">
			<div className="max-w-7xl mx-auto px-4">
				<div className="flex justify-between h-16">
					<div className="flex">
						<Link href="/" className="flex-shrink-0 flex items-center">
							<span className="font-bold text-xl text-blue-600">Hospital MS</span>
						</Link>
						<div className="hidden md:ml-6 md:flex md:space-x-8">
							<Link href="/dashboard" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500">
								Dashboard
							</Link>
							<Link href="/doctors" className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 border-transparent">
								Doctors
							</Link>
						</div>
					</div>
					<div className="flex items-center">
						{isLoggedIn ? (
							<button
								onClick={handleLogout}
								className="ml-4 px-4 py-2 rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
							>
								Logout
							</button>
						) : (
							<Link
								href="/login"
								className="ml-4 px-4 py-2 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
							>
								Login
							</Link>
						)}
					</div>
				</div>
			</div>
		</nav>
	);
}
