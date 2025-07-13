import React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { ChevronsUpDown } from "lucide-react";

const periodOptions = [
  { label: "Last 7 days", value: "7d" },
  { label: "Last 1 month", value: "1m" },
  { label: "Last 3 months", value: "3m" },
  { label: "Last 6 months", value: "6m" },
  { label: "Last 1 year", value: "1y" },
  { label: "Custom range", value: "custom" },
];
const categoryOptions = [
  "Electronics",
  "Fashion",
  "Home & Garden",
  "Beauty & Health",
  "Sports & Outdoors",
  "Books & Media",
  "Automotive",
  "Toys & Games",
  "Food & Beverages",
  "Jewelry & Accessories",
];

const mockPreviousAnalysis = [
  {
    title: "Profit & High Sales Analysis",
    date: "2024-06-01",
    summary: "Identified top 5 products with highest profit margin and sales volume.",
  },
  {
    title: "Customer Segmentation",
    date: "2024-05-28",
    summary: "Segmented customers into 3 main groups based on purchase behavior.",
  },
  {
    title: "Sales Trend Forecast",
    date: "2024-05-20",
    summary: "Predicted 15% increase in sales for next quarter.",
  },
];

export default function DashSection({
  userName,
  period,
  handlePeriodChange,
  selectedCategories,
  categoryOpen,
  setCategoryOpen,
  handleCategoryToggle,
}) {
  return (
    <>
      <div className="sticky top-0 z-30 flex flex-col items-end gap-4 p-6 bg-gradient-to-br from-blue-50 via-purple-50 to-white/80 bg-opacity-80 backdrop-blur-md rounded-b-xl shadow-sm">
        <div className="flex gap-4">
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">Time Period:</label>
            <Select value={period} onValueChange={handlePeriodChange}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select period" />
              </SelectTrigger>
              <SelectContent>
                {periodOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">Categories:</label>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={categoryOpen}
              className="w-[200px] justify-between"
              onClick={() => setCategoryOpen(!categoryOpen)}
            >
              {selectedCategories.length === 0
                ? "Select categories..."
                : selectedCategories.length === 1
                ? selectedCategories[0]
                : `${selectedCategories.length} categories selected`}
              <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
            {/* Category popover logic should be handled in parent */}
          </div>
        </div>
      </div>
      <div className="p-8">
        <h2 className="text-4xl font-extrabold text-blue-900 mb-2 tracking-tight drop-shadow">
          Welcome, {userName}!
        </h2>
        <p className="text-lg text-gray-700 mb-8">Here's your analytics and insights overview.</p>
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-purple-800 mb-2">Overview</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-4">
            <Card className="border-0 glass shadow-lg">
              <CardContent className="p-6">
                <div className="text-blue-600 mb-2 font-semibold">Total Sales</div>
                <div className="text-3xl font-extrabold text-blue-900">$45,231</div>
              </CardContent>
            </Card>
            <Card className="border-0 glass shadow-lg">
              <CardContent className="p-6">
                <div className="text-purple-600 mb-2 font-semibold">Top Product</div>
                <div className="text-3xl font-extrabold text-purple-900">Product A</div>
              </CardContent>
            </Card>
            <Card className="border-0 glass shadow-lg">
              <CardContent className="p-6">
                <div className="text-blue-600 mb-2 font-semibold">Revenue</div>
                <div className="text-3xl font-extrabold text-blue-900">$120,000</div>
              </CardContent>
            </Card>
            <Card className="border-0 glass shadow-lg">
              <CardContent className="p-6">
                <div className="text-purple-600 mb-2 font-semibold">Profit</div>
                <div className="text-3xl font-extrabold text-purple-900">$30,000</div>
              </CardContent>
            </Card>
          </div>
          {/* Sales Analysis Example */}
          <h3 className="text-xl font-bold text-blue-800 mt-6 mb-2">Sales Analysis</h3>
          <div className="flex flex-col md:flex-row gap-8 mb-4">
            {/* Example Bar Chart */}
            <div className="flex-1 bg-white rounded-lg shadow p-4">
              <h4 className="font-semibold mb-2">Sales Trend (Example)</h4>
              <img src="https://www.chartjs.org/media/chartjs-demo-bar.png" alt="Bar Chart Example" className="w-full h-48 object-contain" />
            </div>
            {/* Example Table */}
            <div className="flex-1 bg-white rounded-lg shadow p-4">
              <h4 className="font-semibold mb-2">Sales Table (Example)</h4>
              <table className="w-full text-left">
                <thead>
                  <tr>
                    <th className="py-1 px-2">Date</th>
                    <th className="py-1 px-2">Sales</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td className="py-1 px-2">2024-07-01</td><td className="py-1 px-2">$2,300</td></tr>
                  <tr><td className="py-1 px-2">2024-07-02</td><td className="py-1 px-2">$2,800</td></tr>
                  <tr><td className="py-1 px-2">2024-07-03</td><td className="py-1 px-2">$3,100</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          {/* Inventory Status Example */}
          <h3 className="text-xl font-bold text-purple-800 mt-6 mb-2">Inventory Status</h3>
          <div className="bg-white rounded-lg shadow p-4 mb-4">
            <h4 className="font-semibold mb-2">Low/Out-of-Stock Products (Example)</h4>
            <table className="w-full text-left">
              <thead>
                <tr>
                  <th className="py-1 px-2">Product</th>
                  <th className="py-1 px-2">Status</th>
                  <th className="py-1 px-2">Stock</th>
                </tr>
              </thead>
              <tbody>
                <tr><td className="py-1 px-2">Product B</td><td className="py-1 px-2 text-red-600">Low</td><td className="py-1 px-2">5</td></tr>
                <tr><td className="py-1 px-2">Product C</td><td className="py-1 px-2 text-red-600">Out of Stock</td><td className="py-1 px-2">0</td></tr>
              </tbody>
            </table>
          </div>
          {/* Top Products Example */}
          <h3 className="text-xl font-bold text-blue-800 mt-6 mb-2">Top Products</h3>
          <div className="bg-white rounded-lg shadow p-4 mb-4">
            <h4 className="font-semibold mb-2">Top Products by Sales (Example)</h4>
            <ul className="list-disc pl-6">
              <li>Product A - $12,000</li>
              <li>Product D - $9,500</li>
              <li>Product B - $8,200</li>
            </ul>
          </div>
          <h3 className="text-xl font-bold text-blue-800 mt-6 mb-2">Export Snapshot</h3>
          <Badge variant="secondary">Download PDF/CSV (placeholder)</Badge>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-purple-800 mb-2">Previous Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockPreviousAnalysis.map((item, idx) => (
              <Card key={idx} className="border-0 glass shadow-md">
                <CardHeader>
                  <CardTitle className="text-blue-900 font-bold">{item.title}</CardTitle>
                  <CardDescription className="text-purple-700">{item.date}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-800 mb-2">{item.summary}</p>
                  <Badge variant="secondary">View Details</Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
