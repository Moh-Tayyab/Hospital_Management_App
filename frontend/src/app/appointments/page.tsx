'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button, Badge, Card, Modal, Input } from '@/components/ui';
import {
	FiChevronLeft,
	FiChevronRight,
	FiCalendar,
	FiClock,
	FiPlus,
	FiFilter,
} from 'react-icons/fi';

// Mock appointments data
const mockAppointments = [
	{
		id: 1,
		patientName: 'John Doe',
		patientId: 'P001',
		doctorName: 'Dr. Sarah Smith',
		type: 'Consultation',
		date: '2025-11-25',
		time: '09:00',
		duration: 30,
		status: 'Scheduled',
	},
	{
		id: 2,
		patientName: 'Jane Smith',
		patientId: 'P002',
		doctorName: 'Dr. Michael Johnson',
		type: 'Follow-up',
		date: '2025-11-25',
		time: '10:30',
		duration: 45,
		status: 'Confirmed',
	},
	{
		id: 3,
		patientName: 'Robert Brown',
		patientId: 'P003',
		doctorName: 'Dr. Emily Davis',
		type: 'Emergency',
		date: '2025-11-25',
		time: '14:00',
		duration: 60,
		status: 'In Progress',
	},
	{
		id: 4,
		patientName: 'Lisa Anderson',
		patientId: 'P004',
		doctorName: 'Dr. Sarah Smith',
		type: 'Consultation',
		date: '2025-11-26',
		time: '11:00',
		duration: 30,
		status: 'Scheduled',
	},
	{
		id: 5,
		patientName: 'Michael Wilson',
		patientId: 'P005',
		doctorName: 'Dr. James Lee',
		type: 'Surgery Consultation',
		date: '2025-11-26',
		time: '15:00',
		duration: 90,
		status: 'Scheduled',
	},
];

export default function AppointmentsPage() {
	const [selectedDate, setSelectedDate] = useState(new Date());
	const [viewMode, setViewMode] = useState<'day' | 'week' | 'month'>('week');
	const [isAddModalOpen, setIsAddModalOpen] = useState(false);
	const [filterStatus, setFilterStatus] = useState('All');

	const getStatusVariant = (status: string) => {
		switch (status) {
			case 'Scheduled':
				return 'primary';
			case 'Confirmed':
				return 'info';
			case 'In Progress':
				return 'warning';
			case 'Completed':
				return 'success';
			case 'Cancelled':
				return 'danger';
			default:
				return 'neutral';
		}
	};

	const getAppointmentColor = (status: string) => {
		switch (status) {
			case 'Scheduled':
				return 'border-l-primary-500 bg-primary-50 dark:bg-primary-900/20';
			case 'Confirmed':
				return 'border-l-info-500 bg-info-50 dark:bg-info-900/20';
			case 'In Progress':
				return 'border-l-warning-500 bg-warning-50 dark:bg-warning-900/20';
			case 'Completed':
				return 'border-l-success-500 bg-success-50 dark:bg-success-900/20';
			case 'Cancelled':
				return 'border-l-danger-500 bg-danger-50 dark:bg-danger-900/20';
			default:
				return 'border-l-gray-500 bg-gray-50 dark:bg-gray-800';
		}
	};

	// Filter appointments by date and status
	const todayAppointments = mockAppointments.filter((apt) => {
		const aptDate = new Date(apt.date).toDateString();
		const selectedDateStr = selectedDate.toDateString();
		const matchesDate = aptDate === selectedDateStr;
		const matchesStatus = filterStatus === 'All' || apt.status === filterStatus;
		return matchesDate && matchesStatus;
	});

	const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
	const currentWeekStart = new Date(selectedDate);
	currentWeekStart.setDate(selectedDate.getDate() - selectedDate.getDay() + 1);

	const weekDates = Array.from({ length: 7 }, (_, i) => {
		const date = new Date(currentWeekStart);
		date.setDate(currentWeekStart.getDate() + i);
		return date;
	});

	const navigateDate = (direction: 'prev' | 'next') => {
		const newDate = new Date(selectedDate);
		if (viewMode === 'day') {
			newDate.setDate(selectedDate.getDate() + (direction === 'next' ? 1 : -1));
		} else if (viewMode === 'week') {
			newDate.setDate(selectedDate.getDate() + (direction === 'next' ? 7 : -7));
		} else {
			newDate.setMonth(selectedDate.getMonth() + (direction === 'next' ? 1 : -1));
		}
		setSelectedDate(newDate);
	};

	const goToToday = () => {
		setSelectedDate(new Date());
	};

	return (
		<DashboardLayout>
			{/* Page Header */}
			<div className="mb-8 animate-fade-in">
				<h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
					Appointments
				</h1>
				<p className="text-gray-600 dark:text-gray-400">
					Schedule and manage patient appointments
				</p>
			</div>

			{/* Calendar Controls */}
			<Card className="mb-6 animate-slide-up">
				<div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
					{/* Date Navigation */}
					<div className="flex items-center gap-3">
						<Button
							variant="outline"
							size="sm"
							leftIcon={<FiChevronLeft />}
							onClick={() => navigateDate('prev')}
						>
							Previous
						</Button>
						<Button variant="outline" size="sm" onClick={goToToday}>
							Today
						</Button>
						<Button
							variant="outline"
							size="sm"
							rightIcon={<FiChevronRight />}
							onClick={() => navigateDate('next')}
						>
							Next
						</Button>
						<div className="ml-4 flex items-center gap-2 text-gray-900 dark:text-white">
							<FiCalendar size={20} />
							<span className="font-semibold text-lg">
								{selectedDate.toLocaleDateString('en-US', {
									month: 'long',
									day: 'numeric',
									year: 'numeric',
								})}
							</span>
						</div>
					</div>

					{/* View Mode and Actions */}
					<div className="flex items-center gap-3">
						{/* Status Filter */}
						<select
							value={filterStatus}
							onChange={(e) => setFilterStatus(e.target.value)}
							className="px-3 py-1.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:text-gray-100"
						>
							<option value="All">All Status</option>
							<option value="Scheduled">Scheduled</option>
							<option value="Confirmed">Confirmed</option>
							<option value="In Progress">In Progress</option>
							<option value="Completed">Completed</option>
							<option value="Cancelled">Cancelled</option>
						</select>

						{/* View Mode Toggle */}
						<div className="flex bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
							{(['day', 'week', 'month'] as const).map((mode) => (
								<button
									key={mode}
									onClick={() => setViewMode(mode)}
									className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${viewMode === mode
											? 'bg-white dark:bg-gray-700 text-primary-600 dark:text-primary-400 shadow-sm'
											: 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
										}`}
								>
									{mode.charAt(0).toUpperCase() + mode.slice(1)}
								</button>
							))}
						</div>

						<Button
							variant="primary"
							size="md"
							leftIcon={<FiPlus />}
							onClick={() => setIsAddModalOpen(true)}
						>
							New Appointment
						</Button>
					</div>
				</div>
			</Card>

			{/* Week Calendar View */}
			{viewMode === 'week' && (
				<div className="grid grid-cols-7 gap-4 mb-6 animate-slide-up" style={{ animationDelay: '100ms' }}>
					{weekDates.map((date, index) => {
						const isToday = date.toDateString() === new Date().toDateString();
						const isSelected = date.toDateString() === selectedDate.toDateString();
						const dayAppointments = mockAppointments.filter(
							(apt) => new Date(apt.date).toDateString() === date.toDateString()
						);

						return (
							<Card
								key={index}
								padding="sm"
								hoverable
								onClick={() => setSelectedDate(date)}
								className={`cursor-pointer ${isSelected ? 'ring-2 ring-primary-500' : ''
									}`}
							>
								<div className="text-center">
									<p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
										{weekDays[index]}
									</p>
									<div
										className={`w-10 h-10 mx-auto rounded-full flex items-center justify-center font-semibold ${isToday
												? 'bg-primary-600 text-white'
												: isSelected
													? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
													: 'text-gray-900 dark:text-white'
											}`}
									>
										{date.getDate()}
									</div>
									{dayAppointments.length > 0 && (
										<div className="mt-2">
											<Badge variant="primary" size="sm">
												{dayAppointments.length}
											</Badge>
										</div>
									)}
								</div>
							</Card>
						);
					})}
				</div>
			)}

			{/* Today's Schedule */}
			<Card padding="none" className="animate-slide-up" style={{ animationDelay: '200ms' }}>
				<div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
					<h2 className="text-xl font-semibold text-gray-900 dark:text-white">
						{selectedDate.toDateString() === new Date().toDateString()
							? "Today's Schedule"
							: `Schedule for ${selectedDate.toLocaleDateString('en-US', {
								month: 'long',
								day: 'numeric',
							})}`}
					</h2>
				</div>

				{todayAppointments.length === 0 ? (
					<div className="px-6 py-12 text-center">
						<FiCalendar className="mx-auto text-gray-400 mb-3" size={48} />
						<p className="text-lg font-medium text-gray-600 dark:text-gray-400 mb-1">
							No appointments scheduled
						</p>
						<p className="text-sm text-gray-500 dark:text-gray-500 mb-4">
							Add a new appointment to get started
						</p>
						<Button variant="primary" leftIcon={<FiPlus />} onClick={() => setIsAddModalOpen(true)}>
							Schedule Appointment
						</Button>
					</div>
				) : (
					<div className="p-6 space-y-3">
						{todayAppointments.map((appointment) => (
							<div
								key={appointment.id}
								className={`p-4 border-l-4 rounded-lg transition-all hover:shadow-md ${getAppointmentColor(
									appointment.status
								)}`}
							>
								<div className="flex items-start justify-between">
									<div className="flex-1">
										<div className="flex items-center gap-3 mb-2">
											<div className="flex items-center gap-2 text-gray-900 dark:text-white">
												<FiClock size={16} />
												<span className="font-semibold">{appointment.time}</span>
												<span className="text-gray-500 dark:text-gray-400">
													({appointment.duration} min)
												</span>
											</div>
											<Badge variant={getStatusVariant(appointment.status)} size="sm">
												{appointment.status}
											</Badge>
										</div>
										<h3 className="font-semibold text-gray-900 dark:text-white mb-1">
											{appointment.patientName}
											<span className="text-sm text-gray-500 dark:text-gray-400 font-normal ml-2">
												({appointment.patientId})
											</span>
										</h3>
										<div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
											<span>{appointment.doctorName}</span>
											<span>•</span>
											<span>{appointment.type}</span>
										</div>
									</div>
									<div className="flex gap-2">
										<Button variant="outline" size="sm">
											View
										</Button>
										<Button variant="ghost" size="sm">
											Edit
										</Button>
									</div>
								</div>
							</div>
						))}
					</div>
				)}
			</Card>

			{/* Add Appointment Modal */}
			<Modal
				isOpen={isAddModalOpen}
				onClose={() => setIsAddModalOpen(false)}
				title="Schedule New Appointment"
				size="lg"
				footer={
					<>
						<Button variant="ghost" onClick={() => setIsAddModalOpen(false)}>
							Cancel
						</Button>
						<Button variant="primary">Schedule Appointment</Button>
					</>
				}
			>
				<div className="space-y-4">
					<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div className="md:col-span-2">
							<label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Patient
							</label>
							<select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
								<option value="">Select patient...</option>
								<option value="P001">John Doe (P001)</option>
								<option value="P002">Jane Smith (P002)</option>
								<option value="P003">Robert Brown (P003)</option>
							</select>
						</div>

						<div className="md:col-span-2">
							<label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Doctor
							</label>
							<select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
								<option value="">Select doctor...</option>
								<option value="D001">Dr. Sarah Smith - Cardiology</option>
								<option value="D002">Dr. Michael Johnson - Pediatrics</option>
								<option value="D003">Dr. Emily Davis - Orthopedics</option>
							</select>
						</div>

						<Input label="Date" type="date" required fullWidth />
						<Input label="Time" type="time" required fullWidth />

						<div>
							<label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Appointment Type
							</label>
							<select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
								<option value="">Select type...</option>
								<option value="Consultation">Consultation</option>
								<option value="Follow-up">Follow-up</option>
								<option value="Emergency">Emergency</option>
								<option value="Surgery">Surgery Consultation</option>
							</select>
						</div>

						<div>
							<label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Duration (minutes)
							</label>
							<select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
								<option value="15">15 minutes</option>
								<option value="30">30 minutes</option>
								<option value="45">45 minutes</option>
								<option value="60">1 hour</option>
								<option value="90">1.5 hours</option>
								<option value="120">2 hours</option>
							</select>
						</div>

						<div className="md:col-span-2">
							<label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Notes
							</label>
							<textarea
								rows={3}
								className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
								placeholder="Additional notes or special requirements..."
							/>
						</div>
					</div>
				</div>
			</Modal>
		</DashboardLayout>
	);
}
