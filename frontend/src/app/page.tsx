'use client';

import Link from 'next/link';
import { FaHospital } from 'react-icons/fa';
import {
  FiUsers,
  FiCalendar,
  FiActivity,
  FiShield,
  FiZap,
  FiCheckCircle,
} from 'react-icons/fi';
import { Button, Card } from '@/components/ui';

export default function Home() {
  const features = [
    {
      icon: <FiUsers size={24} />,
      title: 'Patient Management',
      description: 'Comprehensive patient records, medical history, and treatment tracking',
    },
    {
      icon: <FiCalendar size={24} />,
      title: 'Appointment Scheduling',
      description: 'Efficient scheduling system with real-time availability and reminders',
    },
    {
      icon: <FiActivity size={24} />,
      title: 'Electronic Health Records',
      description: 'Secure, accessible medical records with HIPAA compliance',
    },
    {
      icon: <FiShield size={24} />,
      title: 'Security & Compliance',
      description: 'Enterprise-grade security with role-based access control',
    },
    {
      icon: <FiZap size={24} />,
      title: 'Real-time Updates',
      description: 'Instant notifications and live status updates across the system',
    },
    {
      icon: <FiCheckCircle size={24} />,
      title: 'Lab Integration',
      description: 'Seamless integration with laboratory systems and diagnostic tools',
    },
  ];

  const stats = [
    { value: '1,234', label: 'Patients Managed' },
    { value: '99.9%', label: 'System Uptime' },
    { value: '24/7', label: 'Support Available' },
    { value: '100%', label: 'HIPAA Compliant' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center text-white shadow-md">
                <FaHospital size={20} />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                HealthMS
              </span>
            </Link>
            <div className="flex items-center gap-4">
              <Link
                href="/login"
                className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
              >
                Sign In
              </Link>
              <Link href="/dashboard">
                <Button variant="primary" size="sm">
                  Go to Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full text-sm font-medium mb-6 animate-fade-in">
            <span className="w-2 h-2 bg-primary-600 rounded-full animate-pulse"></span>
            Modern Hospital Management System
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 animate-slide-up">
            Healthcare Management
            <br />
            <span className="bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
              Made Simple
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-10 max-w-3xl mx-auto animate-slide-up">
            Streamline your hospital operations with our comprehensive, secure, and
            user-friendly management system designed for modern healthcare facilities.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up">
            <Link href="/dashboard">
              <Button variant="primary" size="lg" leftIcon={<FiZap />}>
                Get Started
              </Button>
            </Link>
            <Link href="/demo">
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-12 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <p className="text-4xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                  {stat.value}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Everything You Need
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Powerful features to manage every aspect of your hospital operations
              efficiently and securely.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card
                key={index}
                variant="elevated"
                hoverable
                className="animate-fade-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="p-3 w-12 h-12 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 bg-gradient-to-r from-primary-600 to-primary-800">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Hospital Management?
          </h2>
          <p className="text-xl text-primary-100 mb-10">
            Join hundreds of healthcare facilities using HealthMS to improve patient
            care and operational efficiency.
          </p>
          <Link href="/dashboard">
            <Button variant="secondary" size="lg" leftIcon={<FiZap />}>
              Access Dashboard
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-black text-gray-400 px-4 sm:px-6 lg:px-8 py-12">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center text-white">
              <FaHospital size={16} />
            </div>
            <span className="text-lg font-bold text-white">HealthMS</span>
          </div>
          <p className="text-sm mb-4">
            © 2025 HealthMS. All rights reserved. | HIPAA Compliant
          </p>
          <div className="flex items-center justify-center gap-6 text-sm">
            <Link href="/privacy" className="hover:text-white transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="hover:text-white transition-colors">
              Terms of Service
            </Link>
            <Link href="/support" className="hover:text-white transition-colors">
              Support
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
