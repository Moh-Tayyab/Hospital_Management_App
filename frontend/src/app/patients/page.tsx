'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Button, Input, Badge, Card, Modal } from '@/components/ui';
import {
	FiSearch,
	FiFilter,
	FiPlus,
	FiEdit2,
	FiTrash2,
	FiEye,
	FiDownload,
} from 'react-icons/fi';
import Link from 'next/link';

// Mock data - in production, this would come from API
const mockPatients = [
	{
		id: 'P001',
		name: 'John Doe',
		age: 45,
		gender: 'Male',
		phone: '(555) 123-4567',
		email: 'john.doe@email.com',
		status: 'Outpatient',
		lastVisit: '2025-11-20',
		doctor: 'Dr. Sarah Smith',
	},
	{
		id: 'P002',
		name: 'Jane Smith',
		age: 32,
		gender: 'Female',
		phone: '(555) 234-5678',
		email: 'jane.smith@email.com',
		status: 'Inpatient',
		lastVisit: '2025-11-22',
		doctor: 'Dr. Michael Johnson',
	},
	{
		id: 'P003',
		name: 'Robert Brown',
		age: 58,
		gender: 'Male',
		phone: '(555) 345-6789',
		email: 'robert.brown@email.com',
		status: 'Discharged',
		lastVisit: '2025-11-15',
		doctor: 'Dr. Emily Davis',
	},
	{
		id: 'P004',
		name: 'Lisa Anderson',
		age: 28,
		gender: 'Female',
		phone: '(555) 456-7890',
		email: 'lisa.anderson@email.com',
		status: 'Outpatient',
		lastVisit: '2025-11-21',
		doctor: 'Dr. Sarah Smith',
	},
	{
		id: 'P005',
		name: 'Michael Wilson',
		age: 67,
		gender: 'Male',
		phone: '(555) 567-8901',
		email: 'michael.wilson@email.com',
		status: 'Inpatient',
		lastVisit: '2025-11-23',
		doctor: 'Dr. James Lee',
	},
];

export default function PatientsPage() {
	const [searchQuery, setSearchQuery] = useState('');
	const [statusFilter, setStatusFilter] = useState('All');
	const [genderFilter, setGenderFilter] = useState('All');
	const [isAddModalOpen, setIsAddModalOpen] = useState(false);

	// Filter patients based on search and filters
	const filteredPatients = mockPatients.filter((patient) => {
		const matchesSearch =
			patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			patient.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
			patient.email.toLowerCase().includes(searchQuery.toLowerCase());

		const matchesStatus =
			statusFilter === 'All' || patient.status === statusFilter;

		const matchesGender =
			genderFilter === 'All' || patient.gender === genderFilter;

		return matchesSearch && matchesStatus && matchesGender;
	});

	const getStatusVariant = (status: string) => {
		switch (status) {
			case 'Inpatient':
				return 'primary';
			case 'Outpatient':
				return 'success';
			case 'Discharged':
				return 'neutral';
			default:
				return 'neutral';
		}
	};

	return (
		<DashboardLayout>
			{/* Page Header */}
			<div className="mb-8 animate-fade-in">
				<h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
					Patients
				</h1>
				<p className="text-gray-600 dark:text-gray-400">
					Manage patient records and information
				</p>
			</div>

			{/* Filters and Actions */}
			<Card className="mb-6 animate-slide-up">
				<div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
					{/* Search and Filters */}
					<div className="flex flex-col sm:flex-row gap-3 flex-1 w-full lg:w-auto">
						{/* Search Bar */}
						<div className="flex-1 max-w-md">
							<Input
								type="text"
								placeholder="Search by name, ID, or email..."
								value={searchQuery}
								onChange={(e) => setSearchQuery(e.target.value)}
								leftIcon={<FiSearch size={18} />}
								fullWidth
							/>
						</div>

						{/* Status Filter */}
						<select
							value={statusFilter}
							onChange={(e) => setStatusFilter(e.target.value)}
							className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:text-gray-100"
						>
							<option value="All">All Status</option>
							<option value="Inpatient">Inpatient</option>
							<option value="Outpatient">Outpatient</option>
							<option value="Discharged">Discharged</option>
						</select>

						{/* Gender Filter */}
						<select
							value={genderFilter}
							onChange={(e) => setGenderFilter(e.target.value)}
							className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:text-gray-100"
						>
							<option value="All">All Gender</option>
							<option value="Male">Male</option>
							<option value="Female">Female</option>
						</select>
					</div>

					{/* Action Buttons */}
					<div className="flex gap-2">
						<Button
							variant="outline"
							size="md"
							leftIcon={<FiDownload size={18} />}
						>
							Export
						</Button>
						<Button
							variant="primary"
							size="md"
							leftIcon={<FiPlus size={18} />}
							onClick={() => setIsAddModalOpen(true)}
						>
							Add Patient
						</Button>
					</div>
				</div>

				{/* Active Filters Display */}
				{(statusFilter !== 'All' || genderFilter !== 'All' || searchQuery) && (
					<div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
						<div className="flex items-center gap-2 flex-wrap">
							<span className="text-sm text-gray-600 dark:text-gray-400">
								Active filters:
							</span>
							{searchQuery && (
								<Badge variant="primary" size="sm">
									Search: "{searchQuery}"
								</Badge>
							)}
							{statusFilter !== 'All' && (
								<Badge variant="info" size="sm">
									Status: {statusFilter}
								</Badge>
							)}
							{genderFilter !== 'All' && (
								<Badge variant="info" size="sm">
									Gender: {genderFilter}
								</Badge>
							)}
							<button
								onClick={() => {
									setSearchQuery('');
									setStatusFilter('All');
									setGenderFilter('All');
								}}
								className="text-sm text-primary-600 dark:text-primary-400 hover:underline"
							>
								Clear all
							</button>
						</div>
					</div>
				)}
			</Card>

			{/* Patients Table */}
			<Card padding="none" className="animate-slide-up" style={{ animationDelay: '100ms' }}>
				<div className="overflow-x-auto">
					<table className="w-full">
						<thead className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700">
							<tr>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Patient ID
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Name
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Age
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Gender
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Contact
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Status
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Last Visit
								</th>
								<th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
									Actions
								</th>
							</tr>
						</thead>
						<tbody className="divide-y divide-gray-200 dark:divide-gray-700">
							{filteredPatients.length === 0 ? (
								<tr>
									<td colSpan={8} className="px-6 py-12 text-center">
										<div className="text-gray-500 dark:text-gray-400">
											<p className="text-lg font-medium mb-1">No patients found</p>
											<p className="text-sm">Try adjusting your search or filters</p>
										</div>
									</td>
								</tr>
							) : (
								filteredPatients.map((patient) => (
									<tr
										key={patient.id}
										className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
									>
										<td className="px-6 py-4 whitespace-nowrap">
											<span className="text-sm font-medium text-primary-600 dark:text-primary-400">
												{patient.id}
											</span>
										</td>
										<td className="px-6 py-4 whitespace-nowrap">
											<div>
												<p className="text-sm font-medium text-gray-900 dark:text-white">
													{patient.name}
												</p>
												<p className="text-sm text-gray-500 dark:text-gray-400">
													{patient.email}
												</p>
											</div>
										</td>
										<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
											{patient.age}
										</td>
										<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
											{patient.gender}
										</td>
										<td className="px-6 py-4 whitespace-nowrap">
											<p className="text-sm text-gray-700 dark:text-gray-300">
												{patient.phone}
											</p>
										</td>
										<td className="px-6 py-4 whitespace-nowrap">
											<Badge variant={getStatusVariant(patient.status)} size="sm">
												{patient.status}
											</Badge>
										</td>
										<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
											{new Date(patient.lastVisit).toLocaleDateString()}
										</td>
										<td className="px-6 py-4 whitespace-nowrap">
											<div className="flex items-center gap-2">
												<Link href={`/patients/${patient.id}`}>
													<button
														className="p-1.5 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded transition-colors"
														title="View Details"
													>
														<FiEye size={18} />
													</button>
												</Link>
												<button
													className="p-1.5 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded transition-colors"
													title="Edit"
												>
													<FiEdit2 size={18} />
												</button>
												<button
													className="p-1.5 text-gray-600 dark:text-gray-400 hover:text-danger-600 dark:hover:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded transition-colors"
													title="Delete"
												>
													<FiTrash2 size={18} />
												</button>
											</div>
										</td>
									</tr>
								))
							)}
						</tbody>
					</table>
				</div>

				{/* Pagination */}
				{filteredPatients.length > 0 && (
					<div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
						<div className="text-sm text-gray-600 dark:text-gray-400">
							Showing <span className="font-medium">{filteredPatients.length}</span> of{' '}
							<span className="font-medium">{mockPatients.length}</span> patients
						</div>
						<div className="flex gap-2">
							<Button variant="outline" size="sm" disabled>
								Previous
							</Button>
							<Button variant="outline" size="sm" disabled>
								Next
							</Button>
						</div>
					</div>
				)}
			</Card>

			{/* Add Patient Modal */}
			<Modal
				isOpen={isAddModalOpen}
				onClose={() => setIsAddModalOpen(false)}
				title="Add New Patient"
				size="lg"
				footer={
					<>
						<Button variant="ghost" onClick={() => setIsAddModalOpen(false)}>
							Cancel
						</Button>
						<Button variant="primary">Save Patient</Button>
					</>
				}
			>
				<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
					<Input label="First Name" placeholder="Enter first name" required fullWidth />
					<Input label="Last Name" placeholder="Enter last name" required fullWidth />
					<Input label="Date of Birth" type="date" required fullWidth />
					<select className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100">
						<option value="">Select Gender</option>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
						<option value="Other">Other</option>
					</select>
					<Input label="Phone Number" type="tel" placeholder="(555) 123-4567" fullWidth />
					<Input label="Email" type="email" placeholder="patient@email.com" fullWidth />
					<Input
						label="Address"
						placeholder="Street address"
						fullWidth
						className="md:col-span-2"
					/>
					<Input label="City" placeholder="City" fullWidth />
					<Input label="State" placeholder="State" fullWidth />
					<Input label="ZIP Code" placeholder="ZIP" fullWidth />
					<select className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 dark:text-gray-100">
						<option value="">Blood Type</option>
						<option value="A+">A+</option>
						<option value="A-">A-</option>
						<option value="B+">B+</option>
						<option value="B-">B-</option>
						<option value="AB+">AB+</option>
						<option value="AB-">AB-</option>
						<option value="O+">O+</option>
						<option value="O-">O-</option>
					</select>
				</div>
			</Modal>
		</DashboardLayout>
	);
}
