'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { Button } from '@/components/ui';

interface Doctor {
	id: number;
	user: {
		first_name: string;
		last_name: string;
	};
	specialization: string;
}

interface Slot {
	start_time: string;
	end_time: string;
	formatted_time: string;
}

export default function NewAppointment() {
	const router = useRouter();
	const [doctors, setDoctors] = useState<Doctor[]>([]);
	const [selectedDoctor, setSelectedDoctor] = useState<string>('');
	const [selectedDate, setSelectedDate] = useState<string>('');
	const [slots, setSlots] = useState<Slot[]>([]);
	const [selectedSlot, setSelectedSlot] = useState<string>('');
	const [reason, setReason] = useState('');
	const [loading, setLoading] = useState(false);

	useEffect(() => {
		const fetchDoctors = async () => {
			try {
				const response = await api.get('/doctors/');
				setDoctors(response.data);
			} catch (error) {
				console.error('Failed to fetch doctors:', error);
			}
		};
		fetchDoctors();
	}, []);

	useEffect(() => {
		if (selectedDoctor && selectedDate) {
			const fetchSlots = async () => {
				try {
					const response = await api.get(`/doctors/${selectedDoctor}/availability/?date=${selectedDate}`);
					setSlots(response.data.slots);
				} catch (error) {
					console.error('Failed to fetch slots:', error);
				}
			};
			fetchSlots();
		}
	}, [selectedDoctor, selectedDate]);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);
		try {
			await api.post('/appointments/', {
				doctor: selectedDoctor,
				appointment_time: selectedSlot,
				reason,
				duration: 30
			});
			router.push('/appointments');
		} catch (error) {
			console.error('Failed to book appointment:', error);
			alert('Failed to book appointment. Please try again.');
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="max-w-2xl mx-auto bg-white shadow sm:rounded-lg p-6">
			<h1 className="text-2xl font-bold text-gray-900 mb-6">Book New Appointment</h1>

			<form onSubmit={handleSubmit} className="space-y-6">
				<div>
					<label className="block text-sm font-medium text-gray-700">Select Doctor</label>
					<select
						required
						className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
						value={selectedDoctor}
						onChange={(e) => setSelectedDoctor(e.target.value)}
					>
						<option value="">Choose a doctor...</option>
						{doctors.map((doc) => (
							<option key={doc.id} value={doc.id}>
								Dr. {doc.user.first_name} {doc.user.last_name} ({doc.specialization})
							</option>
						))}
					</select>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-700">Select Date</label>
					<input
						type="date"
						required
						min={new Date().toISOString().split('T')[0]}
						className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
						value={selectedDate}
						onChange={(e) => setSelectedDate(e.target.value)}
					/>
				</div>

				{slots.length > 0 && (
					<div>
						<label className="block text-sm font-medium text-gray-700">Available Slots</label>
						<div className="mt-2 grid grid-cols-3 gap-3">
							{slots.map((slot) => (
								<div
									key={slot.start_time}
									className={`cursor-pointer text-center p-2 rounded-md border text-sm ${selectedSlot === slot.start_time
											? 'bg-blue-600 text-white border-blue-600'
											: 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
										}`}
									onClick={() => setSelectedSlot(slot.start_time)}
								>
									{new Date(slot.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
								</div>
							))}
						</div>
					</div>
				)}

				<div>
					<label className="block text-sm font-medium text-gray-700">Reason for Visit</label>
					<textarea
						required
						rows={3}
						className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
						value={reason}
						onChange={(e) => setReason(e.target.value)}
					/>
				</div>

				<div className="flex justify-end">
					<Button type="submit" disabled={loading || !selectedSlot}>
						{loading ? 'Booking...' : 'Confirm Booking'}
					</Button>
				</div>
			</form>
		</div>
	);
}
