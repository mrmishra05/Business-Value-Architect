import React, { useState, useEffect } from 'react';
import { Search, User, CreditCard, BarChart3, Briefcase, MapPin, DollarSign, Clock, Star, Filter, Download, Bell, Trash2, Eye, ExternalLink, Menu, X, Lock, CheckCircle, Globe } from 'lucide-react';

const JobScope = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    role: 'all',
    location: 'all',
    workType: 'all',
    experience: 'all',
    salaryRange: 'all'
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [savedJobs, setSavedJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Mock authentication
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ email: '', password: '', confirmPassword: '' });

  // Generate realistic job data
  const generateJobData = () => {
    const roles = [
      'Customer Success Manager',
      'Senior Customer Success Manager',
      'Customer Success Specialist',
      'Customer Success Director',
      'Customer Success Associate',
      'Scrum Master',
      'Senior Scrum Master',
      'Agile Coach',
      'Scrum Project Manager',
      'Lead Scrum Master'
    ];

    const companies = {
      'India': ['Infosys', 'TCS', 'Wipro', 'HCL Technologies', 'Flipkart', 'Zomato', 'Paytm', 'Swiggy', 'Freshworks', 'Byju\'s'],
      'Singapore': ['Grab', 'Sea Limited', 'DBS Bank', 'Singtel', 'Shopee', 'Gojek', 'Revolut', 'PropertyGuru', 'Carousell', 'Stripe'],
      'Netherlands': ['Booking.com', 'Adyen', 'Philips', 'ING', 'ASML', 'Takeaway.com', 'Coolblue', 'Exact', 'TomTom', 'Randstad'],
      'Germany': ['SAP', 'Siemens', 'Allianz', 'BMW', 'Mercedes-Benz', 'Zalando', 'Delivery Hero', 'N26', 'Rocket Internet', 'AUTO1'],
      'France': ['Airbus', 'Thales', 'Atos', 'Capgemini', 'Orange', 'BlaBlaCar', 'Criteo', 'Dassault Systèmes', 'Murex', 'Datadog']
    };

    const cities = {
      'India': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune'],
      'Singapore': ['Singapore'],
      'Netherlands': ['Amsterdam', 'Rotterdam', 'Utrecht', 'The Hague'],
      'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
      'France': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice']
    };

    const salaryRanges = {
      'India': ['₹15,00,000 - ₹25,00,000', '₹25,00,000 - ₹40,00,000', '₹40,00,000 - ₹60,00,000', '₹60,00,000 - ₹80,00,000', '₹80,00,000 - ₹1,20,00,000'],
      'Singapore': ['S$80,000 - S$120,000', 'S$120,000 - S$160,000', 'S$160,000 - S$200,000', 'S$200,000 - S$250,000', 'S$250,000 - S$300,000'],
      'Netherlands': ['€60,000 - €80,000', '€80,000 - €100,000', '€100,000 - €120,000', '€120,000 - €150,000', '€150,000 - €180,000'],
      'Germany': ['€65,000 - €85,000', '€85,000 - €110,000', '€110,000 - €130,000', '€130,000 - €160,000', '€160,000 - €200,000'],
      'France': ['€55,000 - €75,000', '€75,000 - €95,000', '€95,000 - €115,000', '€115,000 - €140,000', '€140,000 - €170,000']
    };

    const workTypes = ['Remote', 'Hybrid', 'On-site'];
    const experiences = ['Entry Level', '2-3 years', '4-6 years', '7-10 years', '10+ years'];
    const platforms = ['LinkedIn', 'Indeed', 'Glassdoor', 'JobsDB', 'MyCareersFuture', 'Xing', 'StepStone'];

    const jobsData = [];
    const countries = Object.keys(companies);

    for (let i = 0; i < 50; i++) {
      const country = countries[Math.floor(Math.random() * countries.length)];
      const city = cities[country][Math.floor(Math.random() * cities[country].length)];
      const company = companies[country][Math.floor(Math.random() * companies[country].length)];
      const role = roles[Math.floor(Math.random() * roles.length)];
      const workType = workTypes[Math.floor(Math.random() * workTypes.length)];
      const experience = experiences[Math.floor(Math.random() * experiences.length)];
      const salary = salaryRanges[country][Math.floor(Math.random() * salaryRanges[country].length)];
      const platform = platforms[Math.floor(Math.random() * platforms.length)];
      const rating = (Math.random() * 2 + 3).toFixed(1); // 3.0 to 5.0

      jobsData.push({
        id: `job-${i + 1}`,
        title: role,
        company,
        location: `${city}, ${country}`,
        country,
        workType,
        experience,
        salary,
        platform,
        rating: parseFloat(rating),
        postedDate: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        description: `We are looking for a skilled ${role} to join our ${workType.toLowerCase()} team in ${city}. The ideal candidate should have ${experience.toLowerCase()} of experience and be passionate about ${role.includes('Customer') ? 'customer success and relationship management' : 'agile methodologies and team coaching'}.`,
        applyLink: `https://${platform.toLowerCase().replace(' ', '')}.com/jobs/${company.toLowerCase().replace(/[^a-z0-9]/g, '-')}-${role.toLowerCase().replace(/[^a-z0-9]/g, '-')}-${Math.random().toString(36).substr(2, 9)}`
      });
    }

    return jobsData;
  };

  useEffect(() => {
    if (currentPage === 'dashboard' && user) {
      setLoading(true);
      setTimeout(() => {
        setJobs(generateJobData());
        setLoading(false);
      }, 1000);
    }
  }, [currentPage, user]);

  const handleLogin = (e) => {
    e.preventDefault();
    // Mock authentication
    setUser({ 
      email: loginForm.email, 
      subscription: 'premium',
      searchesUsed: 45,
      searchLimit: 1000,
      joinDate: '2024-01-15'
    });
    setCurrentPage('dashboard');
  };

  const handleRegister = (e) => {
    e.preventDefault();
    if (registerForm.password !== registerForm.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    // Mock registration
    setUser({ 
      email: registerForm.email, 
      subscription: 'free',
      searchesUsed: 3,
      searchLimit: 10,
      joinDate: new Date().toISOString().split('T')[0]
    });
    setCurrentPage('dashboard');
  };

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         job.location.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesRole = filters.role === 'all' || 
                       (filters.role === 'customer-success' && job.title.toLowerCase().includes('customer')) ||
                       (filters.role === 'scrum-master' && (job.title.toLowerCase().includes('scrum') || job.title.toLowerCase().includes('agile')));
    
    const matchesLocation = filters.location === 'all' || job.country === filters.location;
    const matchesWorkType = filters.workType === 'all' || job.workType === filters.workType;
    const matchesExperience = filters.experience === 'all' || job.experience === filters.experience;

    return matchesSearch && matchesRole && matchesLocation && matchesWorkType && matchesExperience;
  });

  const saveJob = (job) => {
    if (!savedJobs.find(saved => saved.id === job.id)) {
      setSavedJobs([...savedJobs, job]);
    }
  };

  const trackApplication = (job, status = 'applied') => {
    const application = {
      id: `app-${Date.now()}`,
      jobId: job.id,
      job,
      status,
      appliedDate: new Date().toISOString().split('T')[0],
      notes: ''
    };
    setApplications([...applications, application]);
  };

  const getSalaryInsights = () => {
    if (!jobs.length) return { average: 0, trends: [] };
    
    const salaryData = jobs.map(job => {
      const salaryStr = job.salary.replace(/[^\d-]/g, '');
      const [min, max] = salaryStr.split('-').map(s => parseInt(s.replace(/,/g, '')));
      return (min + max) / 2 || 0;
    }).filter(s => s > 0);

    const average = salaryData.reduce((a, b) => a + b, 0) / salaryData.length;
    
    return {
      average: Math.round(average),
      trends: [
        { country: 'Singapore', avgSalary: '160,000', growth: '+8%' },
        { country: 'Netherlands', avgSalary: '95,000', growth: '+5%' },
        { country: 'Germany', avgSalary: '105,000', growth: '+6%' },
        { country: 'France', avgSalary: '85,000', growth: '+4%' },
        { country: 'India', avgSalary: '35,00,000', growth: '+12%' }
      ]
    };
  };

  const SubscriptionPlans = () => (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Plan</h1>
          <p className="text-xl text-gray-600">Unlock your career potential with JobScope</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Free Plan */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-gray-200">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Free</h3>
              <div className="text-4xl font-bold text-gray-900 mt-2">$0</div>
              <div className="text-gray-600">per month</div>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                10 job searches per day
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Basic job filtering
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Save up to 20 jobs
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Basic analytics
              </li>
            </ul>
            <button className="w-full bg-gray-200 text-gray-800 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors">
              Current Plan
            </button>
          </div>

          {/* Premium Plan */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-blue-500 relative">
            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
              <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
              </span>
            </div>
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Premium</h3>
              <div className="text-4xl font-bold text-gray-900 mt-2">$9</div>
              <div className="text-gray-600">per month</div>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Unlimited job searches
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Advanced filtering & alerts
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Unlimited saved jobs
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Application tracking
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Salary insights & trends
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Company review integration
              </li>
            </ul>
            <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Upgrade to Premium
            </button>
          </div>

          {/* Enterprise Plan */}
          <div className="bg-white rounded-lg shadow-lg p-8 border-2 border-gray-200">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Enterprise</h3>
              <div className="text-4xl font-bold text-gray-900 mt-2">$29</div>
              <div className="text-gray-600">per month</div>
            </div>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Everything in Premium
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                API access
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Bulk job exports
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Priority support
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Advanced analytics
              </li>
              <li className="flex items-center text-gray-700">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                Custom integrations
              </li>
            </ul>
            <button className="w-full bg-gray-800 text-white py-3 rounded-lg font-semibold hover:bg-gray-900 transition-colors">
              Contact Sales
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">JobScope</h1>
            <p className="text-gray-600">Your Professional Job Monitoring Platform</p>
          </div>

          <div className="space-y-4">
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setCurrentPage('login')}
                className={`flex-1 py-2 text-center ${currentPage === 'login' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
              >
                Login
              </button>
              <button
                onClick={() => setCurrentPage('register')}
                className={`flex-1 py-2 text-center ${currentPage === 'register' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
              >
                Register
              </button>
            </div>

            {currentPage === 'login' ? (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <input
                    type="password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Login
                </button>
              </form>
            ) : (
              <form onSubmit={handleRegister} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={registerForm.email}
                    onChange={(e) => setRegisterForm({...registerForm, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <input
                    type="password"
                    value={registerForm.password}
                    onChange={(e) => setRegisterForm({...registerForm, password: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                  <input
                    type="password"
                    value={registerForm.confirmPassword}
                    onChange={(e) => setRegisterForm({...registerForm, confirmPassword: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Register
                </button>
              </form>
            )}

            <div className="text-center pt-4">
              <button
                onClick={() => setCurrentPage('pricing')}
                className="text-blue-600 hover:text-blue-800 text-sm"
              >
                View Pricing Plans
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPage === 'pricing') {
    return <SubscriptionPlans />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">JobScope</h1>
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              <button
                onClick={() => setCurrentPage('dashboard')}
                className={`flex items-center px-3 py-2 text-sm font-medium ${
                  currentPage === 'dashboard' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Search className="h-4 w-4 mr-2" />
                Dashboard
              </button>
              <button
                onClick={() => setCurrentPage('saved')}
                className={`flex items-center px-3 py-2 text-sm font-medium ${
                  currentPage === 'saved' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Briefcase className="h-4 w-4 mr-2" />
                Saved Jobs ({savedJobs.length})
              </button>
              <button
                onClick={() => setCurrentPage('applications')}
                className={`flex items-center px-3 py-2 text-sm font-medium ${
                  currentPage === 'applications' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Bell className="h-4 w-4 mr-2" />
                Applications ({applications.length})
              </button>
              <button
                onClick={() => setCurrentPage('analytics')}
                className={`flex items-center px-3 py-2 text-sm font-medium ${
                  currentPage === 'analytics' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Analytics
              </button>
            </nav>

            <div className="flex items-center space-x-4">
              {/* Subscription Status */}
              <div className="hidden md:flex items-center space-x-2">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  user.subscription === 'premium' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {user.subscription === 'premium' ? 'Premium' : 'Free'}
                </span>
                <span className="text-sm text-gray-600">
                  {user.searchesUsed}/{user.searchLimit} searches
                </span>
              </div>

              {/* User Menu */}
              <div className="relative">
                <button
                  onClick={() => setCurrentPage('profile')}
                  className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
                >
                  <User className="h-5 w-5" />
                  <span className="hidden md:block">{user.email}</span>
                </button>
              </div>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden"
              >
                {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white border-t">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <button
                onClick={() => { setCurrentPage('dashboard'); setMobileMenuOpen(false); }}
                className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900"
              >
                Dashboard
              </button>
              <button
                onClick={() => { setCurrentPage('saved'); setMobileMenuOpen(false); }}
                className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900"
              >
                Saved Jobs ({savedJobs.length})
              </button>
              <button
                onClick={() => { setCurrentPage('applications'); setMobileMenuOpen(false); }}
                className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900"
              >
                Applications ({applications.length})
              </button>
              <button
                onClick={() => { setCurrentPage('analytics'); setMobileMenuOpen(false); }}
                className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900"
              >
                Analytics
              </button>
              <button
                onClick={() => {
