'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Card } from '@/components/ui';

interface MedicalRecord {
	id: number;
	doctor: number; // In a real app, this would be expanded to doctor details
	visit_date: string;
	diagnosis: string;
	prescriptions: string;
	visit_notes: string;
}

export default function MedicalRecordsList() {
	const [records, setRecords] = useState<MedicalRecord[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchRecords = async () => {
			try {
				const response = await api.get('/medical-records/');
				setRecords(response.data);
			} catch (error) {
				console.error('Failed to fetch medical records:', error);
			} finally {
				setLoading(false);
			}
		};

		fetchRecords();
	}, []);

	if (loading) return <div className="text-center mt-10">Loading...</div>;

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-bold text-gray-900">Medical Records</h1>

			{records.length === 0 ? (
				<Card className="text-center py-10">
					<p className="text-gray-500">No medical records found.</p>
				</Card>
			) : (
				<div className="space-y-4">
					{records.map((record) => (
						<Card key={record.id} className="hover:shadow-md transition-shadow">
							<div className="border-l-4 border-blue-500 pl-4">
								<div className="flex justify-between items-start">
									<div>
										<h3 className="text-lg font-medium text-gray-900">
											Visit on {new Date(record.visit_date).toLocaleDateString()}
										</h3>
										<p className="text-sm text-gray-500 mt-1">Diagnosis: {record.diagnosis}</p>
									</div>
								</div>
								<div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
									<div>
										<h4 className="text-sm font-medium text-gray-900">Prescriptions</h4>
										<p className="mt-1 text-sm text-gray-600 whitespace-pre-line">{record.prescriptions}</p>
									</div>
									<div>
										<h4 className="text-sm font-medium text-gray-900">Notes</h4>
										<p className="mt-1 text-sm text-gray-600">{record.visit_notes}</p>
									</div>
								</div>
							</div>
						</Card>
					))}
				</div>
			)}
		</div>
	);
}
