'use client';

import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, Badge } from '@/components/ui';
import {
	FiUsers,
	FiCalendar,
	FiActivity,
	FiTrendingUp,
	FiTrendingDown,
	FiClock,
	FiCheckCircle,
	FiXCircle,
} from 'react-icons/fi';
import { FaUserInjured } from 'react-icons/fa';

export default function DashboardPage() {
	// Mock data - in real app, this would come from API
	const stats = [
		{
			title: 'Total Patients',
			value: '1,234',
			change: '+12.5%',
			isPositive: true,
			icon: <FaUserInjured size={24} />,
			color: 'primary',
		},
		{
			title: "Today's Appointments",
			value: '28',
			change: '+8.2%',
			isPositive: true,
			icon: <FiCalendar size={24} />,
			color: 'success',
		},
		{
			title: 'Available Doctors',
			value: '45',
			change: '-2',
			isPositive: false,
			icon: <FiUsers size={24} />,
			color: 'info',
		},
		{
			title: 'Pending Lab Results',
			value: '12',
			change: '-15.3%',
			isPositive: true,
			icon: <FiActivity size={24} />,
			color: 'warning',
		},
	];

	const recentAppointments = [
		{
			id: 1,
			patient: 'John Doe',
			doctor: 'Dr. Sarah Smith',
			time: '09:00 AM',
			type: 'Consultation',
			status: 'Scheduled',
		},
		{
			id: 2,
			patient: 'Jane Smith',
			doctor: 'Dr. Michael Johnson',
			time: '10:30 AM',
			type: 'Follow-up',
			status: 'In Progress',
		},
		{
			id: 3,
			patient: 'Robert Brown',
			doctor: 'Dr. Emily Davis',
			time: '11:00 AM',
			type: 'Emergency',
			status: 'Completed',
		},
		{
			id: 4,
			patient: 'Lisa Anderson',
			doctor: 'Dr. Sarah Smith',
			time: '02:00 PM',
			type: 'Consultation',
			status: 'Scheduled',
		},
	];

	const patientDistribution = [
		{ status: 'Inpatient', count: 234, percentage: 45, color: 'primary' },
		{ status: 'Outpatient', count: 567, percentage: 35, color: 'success' },
		{ status: 'Emergency', count: 89, percentage: 15, color: 'danger' },
		{ status: 'Discharged', count: 344, percentage: 5, color: 'neutral' },
	];

	const getStatusIcon = (status: string) => {
		switch (status) {
			case 'Scheduled':
				return <FiClock className="inline mr-1" size={14} />;
			case 'In Progress':
				return <FiActivity className="inline mr-1" size={14} />;
			case 'Completed':
				return <FiCheckCircle className="inline mr-1" size={14} />;
			case 'Cancelled':
				return <FiXCircle className="inline mr-1" size={14} />;
			default:
				return null;
		}
	};

	const getStatusVariant = (status: string) => {
		switch (status) {
			case 'Scheduled':
				return 'primary';
			case 'In Progress':
				return 'info';
			case 'Completed':
				return 'success';
			case 'Cancelled':
				return 'danger';
			default:
				return 'neutral';
		}
	};

	return (
		<DashboardLayout>
			{/* Welcome Section */}
			<div className="mb-8 animate-fade-in">
				<h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
					Good Morning, Dr. Sarah
				</h1>
				<p className="text-gray-600 dark:text-gray-400">
					Here's what's happening with your hospital today.
				</p>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				{/* Recent Appointments */}
				<Card variant="elevated" padding="none" className="lg:col-span-2">
					<Card.Header divider className="px-6 pt-6">
						<h2 className="text-xl font-semibold text-gray-900 dark:text-white">
							Recent Appointments
						</h2>
					</Card.Header>
					<Card.Body className="px-6 pb-6">
						<div className="overflow-x-auto">
							<table className="w-full">
								<thead>
									<tr className="text-left text-sm text-gray-600 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">
										<th className="pb-3 font-medium">Patient</th>
										<th className="pb-3 font-medium">Doctor</th>
										<th className="pb-3 font-medium">Time</th>
										<th className="pb-3 font-medium">Type</th>
										<th className="pb-3 font-medium">Status</th>
									</tr>
								</thead>
								<tbody className="text-sm">
									{recentAppointments.map((appointment) => (
										<tr
											key={appointment.id}
											className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
										>
											<td className="py-4 font-medium text-gray-900 dark:text-white">
												{appointment.patient}
											</td>
											<td className="py-4 text-gray-700 dark:text-gray-300">
												{appointment.doctor}
											</td>
											<td className="py-4 text-gray-700 dark:text-gray-300">
												{appointment.time}
											</td>
											<td className="py-4 text-gray-700 dark:text-gray-300">
												{appointment.type}
											</td>
											<td className="py-4">
												<Badge variant={getStatusVariant(appointment.status)} size="sm">
													{getStatusIcon(appointment.status)}
													{appointment.status}
												</Badge>
											</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>
					</Card.Body>
				</Card>

				{/* Patient Distribution */}
				<Card variant="elevated" padding="none">
					<Card.Header divider className="px-6 pt-6">
						<h2 className="text-xl font-semibold text-gray-900 dark:text-white">
							Patient Distribution
						</h2>
					</Card.Header>
					<Card.Body className="px-6 pb-6">
						<div className="space-y-4">
							{patientDistribution.map((item, index) => (
								<div key={index}>
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium text-gray-700 dark:text-gray-300">
											{item.status}
										</span>
										<span className="text-sm font-bold text-gray-900 dark:text-white">
											{item.count}
										</span>
									</div>
									<div className="relative w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
										<div
											className={`absolute left-0 top-0 h-full transition-all duration-500 rounded-full ${item.color === 'primary' ? 'bg-primary-500 dark:bg-primary-600' :
												item.color === 'success' ? 'bg-success-500 dark:bg-success-600' :
													item.color === 'danger' ? 'bg-danger-500 dark:bg-danger-600' :
														'bg-gray-500 dark:bg-gray-600'
												}`}
											style={{ width: `${item.percentage}%` }}
										/>
									</div>
									<p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
										{item.percentage}% of total
									</p>
								</div>
							))}
						</div>
					</Card.Body>
				</Card>
			</div>
		</DashboardLayout>
	);
}
