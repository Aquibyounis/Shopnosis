
import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BarChart3, Users, ShoppingCart, TrendingUp, Eye, Target, ArrowUpRight, ArrowDownRight, Calendar, Filter, Download, Settings, Bell } from 'lucide-react';

const Dashboard = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('7d');

  // Only keep stats if used in the render
  const stats = [
    {
      title: 'Total Revenue',
      value: '$45,231',
      change: '+20.1%',
      changeType: 'positive',
      icon: <TrendingUp className="w-5 h-5" />
    },
    {
      title: 'Active Users',
      value: '12,847',
      change: '+15.3%',
      changeType: 'positive',
      icon: <Users className="w-5 h-5" />
    },
    {
      title: 'Conversion Rate',
      value: '3.24%',
      change: '+2.5%',
      changeType: 'positive',
      icon: <Target className="w-5 h-5" />
    },
    {
      title: 'Page Views',
      value: '89,432',
      change: '-5.4%',
      changeType: 'negative',
      icon: <Eye className="w-5 h-5" />
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-xl font-bold text-gray-900">ShopperMind</h1>
              </div>
              <nav className="hidden md:flex space-x-6">
                <a href="#" className="text-blue-600 font-medium">Dashboard</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Analytics</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Customers</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Reports</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Calendar className="w-4 h-4 mr-2" />
                Last 7 days
              </Button>
              <Button variant="outline" size="sm">
                <Filter className="w-4 h-4 mr-2" />
                Filter
              </Button>
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm">
                <Bell className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>
      {/* Only keep the rest of the dashboard if actually used in the render */}
    </div>
  );
};

export default Dashboard;
