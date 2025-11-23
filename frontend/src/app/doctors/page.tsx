'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Card } from '@/components/ui';

interface Doctor {
	id: number;
	user: {
		first_name: string;
		last_name: string;
		email: string;
	};
	specialization: string;
	department: number;
	contact_info: string;
}

export default function DoctorsList() {
	const [doctors, setDoctors] = useState<Doctor[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchDoctors = async () => {
			try {
				const response = await api.get('/doctors/');
				setDoctors(response.data);
			} catch (error) {
				console.error('Failed to fetch doctors:', error);
			} finally {
				setLoading(false);
			}
		};

		fetchDoctors();
	}, []);

	if (loading) return <div className="text-center mt-10">Loading...</div>;

	return (
		<div className="space-y-6">
			<div className="flex justify-between items-center">
				<h1 className="text-2xl font-bold text-gray-900">Doctors Directory</h1>
			</div>

			<div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
				{doctors.map((doctor) => (
					<Card key={doctor.id} className="hover:shadow-lg transition-shadow">
						<div className="flex items-center space-x-4">
							<div className="flex-shrink-0">
								<div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xl">
									{doctor.user.first_name[0]}
									{doctor.user.last_name[0]}
								</div>
							</div>
							<div className="flex-1 min-w-0">
								<p className="text-lg font-medium text-gray-900 truncate">
									Dr. {doctor.user.first_name} {doctor.user.last_name}
								</p>
								<p className="text-sm text-gray-500 truncate">{doctor.specialization}</p>
							</div>
						</div>
						<div className="mt-4 border-t border-gray-100 pt-4">
							<dl className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2">
								<div className="sm:col-span-2">
									<dt className="text-sm font-medium text-gray-500">Contact</dt>
									<dd className="mt-1 text-sm text-gray-900">{doctor.contact_info}</dd>
								</div>
								<div className="sm:col-span-2">
									<dt className="text-sm font-medium text-gray-500">Email</dt>
									<dd className="mt-1 text-sm text-gray-900">{doctor.user.email}</dd>
								</div>
							</dl>
						</div>
					</Card>
				))}
			</div>
		</div>
	);
}
