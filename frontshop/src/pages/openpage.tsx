import React, { useState } from "react";
import {
  SidebarProvider,
  Sidebar,
  SidebarContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarInset
} from "@/components/ui/sidebar";
import { BarChart3, History as HistoryIcon, Upload, Settings as SettingsIcon, LayoutDashboard } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

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

const mockImportHistory = [
  { file: "products_june.csv", date: "2024-06-01", status: "Success" },
  { file: "sales_may.xlsx", date: "2024-05-28", status: "Failed" },
];

const userName = "John"; // Replace with actual user name from context/auth

const periodOptions = [
  { label: "Week", value: "week" },
  { label: "Month", value: "month" },
  { label: "Year", value: "year" },
];
const categoryOptions = [
  "All Categories",
  "Electronics",
  "Fashion",
  "Home",
  "Beauty",
  "Sports",
];

const OpenPage = () => {
  const [selected, setSelected] = useState("dashboard");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadStatuses, setUploadStatuses] = useState<string[]>([]);
  const [settingsTab, setSettingsTab] = useState("shop");
  const [period, setPeriod] = useState("week");
  const [category, setCategory] = useState("All Categories");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      setSelectedFiles(filesArray);
      setUploadStatuses(Array(filesArray.length).fill(null));
    }
  };

  const handleUpload = () => {
    if (selectedFiles.length > 0) {
      setUploadStatuses(selectedFiles.map(() => "Uploading..."));
      setTimeout(() => {
        setUploadStatuses(selectedFiles.map(() => "Upload successful!"));
      }, 1500);
    }
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex bg-gradient-to-br from-blue-50 via-purple-50 to-white font-sans">
        <Sidebar className="shadow-xl">
          <SidebarContent>
            <SidebarGroup>
              <SidebarGroupLabel>
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-6 h-6 text-blue-600" />
                  <span className="font-bold text-lg">Shopnosis</span>
                </div>
              </SidebarGroupLabel>
              <SidebarMenu>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    isActive={selected === "dashboard"}
                    onClick={() => setSelected("dashboard")}
                  >
                    <LayoutDashboard className="w-5 h-5 mr-2" /> Dashboard
                  </SidebarMenuButton>
                </SidebarMenuItem>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    isActive={selected === "import"}
                    onClick={() => setSelected("import")}
                  >
                    <Upload className="w-5 h-5 mr-2" /> Import
                  </SidebarMenuButton>
                </SidebarMenuItem>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    isActive={selected === "history"}
                    onClick={() => setSelected("history")}
                  >
                    <HistoryIcon className="w-5 h-5 mr-2" /> History
                  </SidebarMenuButton>
                </SidebarMenuItem>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    isActive={selected === "settings"}
                    onClick={() => setSelected("settings")}
                  >
                    <SettingsIcon className="w-5 h-5 mr-2" /> Settings
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroup>
          </SidebarContent>
        </Sidebar>
        <SidebarInset className="relative p-0 flex-1">
          {/* Sticky Filters */}
          {selected === "dashboard" && (
            <>
              <div className="sticky top-0 z-30 flex flex-col items-end gap-2 p-6 bg-gradient-to-br from-blue-50 via-purple-50 to-white/80 bg-opacity-80 backdrop-blur-md rounded-b-xl shadow-sm">
                <div className="flex gap-2">
                  {periodOptions.map(opt => (
                    <Button
                      key={opt.value}
                      variant={period === opt.value ? "default" : "outline"}
                      className={cn(
                        period === opt.value
                          ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow"
                          : "border-blue-200 text-blue-700 hover:bg-blue-50",
                        "font-semibold px-4 py-2 rounded-full transition"
                      )}
                      onClick={() => setPeriod(opt.value)}
                    >
                      {opt.label}
                    </Button>
                  ))}
                </div>
                <div className="flex gap-2 mt-2">
                  {categoryOptions.map(opt => (
                    <Button
                      key={opt}
                      variant={category === opt ? "default" : "outline"}
                      className={cn(
                        category === opt
                          ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow"
                          : "border-purple-200 text-purple-700 hover:bg-purple-50",
                        "font-semibold px-4 py-2 rounded-full transition"
                      )}
                      onClick={() => setCategory(opt)}
                    >
                      {opt}
                    </Button>
                  ))}
                </div>
              </div>
              <div className="p-8">
                <h2 className="text-4xl font-extrabold text-blue-900 mb-2 tracking-tight drop-shadow">Welcome, {userName}!</h2>
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
                  <h3 className="text-xl font-bold text-blue-800 mt-6 mb-2">Sales Analysis</h3>
                  <p className="text-gray-700 mb-4">Graphs and tables for daily/weekly/monthly trends (placeholder).</p>
                  <h3 className="text-xl font-bold text-purple-800 mt-6 mb-2">Inventory Status</h3>
                  <p className="text-gray-700 mb-4">Low stock, out-of-stock products (placeholder).</p>
                  <h3 className="text-xl font-bold text-blue-800 mt-6 mb-2">Top Products</h3>
                  <p className="text-gray-700 mb-4">Based on sales or profit (placeholder).</p>
                  <h3 className="text-xl font-bold text-purple-800 mt-6 mb-2">Custom Filters</h3>
                  <p className="text-gray-700 mb-4">Date range, category, brand, etc. (placeholder).</p>
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
          )}
          {selected === "import" && (
            <div>
              <h2 className="text-2xl font-bold mb-4">Import Data</h2>
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Upload Product Data</h3>
                <p className="text-gray-600 mb-2">Upload a CSV or Excel file. <a href="#" className="text-blue-600 underline">Download required format template</a></p>
                <input type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} className="mb-2" multiple />
                <button
                  className="ml-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                  onClick={handleUpload}
                  disabled={selectedFiles.length === 0}
                  type="button"
                >
                  Upload
                </button>
                {selectedFiles.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-semibold mb-2">Selected Files:</h4>
                    <ul className="list-disc ml-6">
                      {selectedFiles.map((file, idx) => (
                        <li key={file.name + idx} className="mb-1">
                          {file.name}
                          {uploadStatuses[idx] && (
                            <span className="ml-2 text-green-600">{uploadStatuses[idx]}</span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Import History</h3>
                <table className="min-w-full bg-white/80 rounded shadow">
                  <thead>
                    <tr>
                      <th className="py-2 px-4 text-left">File</th>
                      <th className="py-2 px-4 text-left">Date</th>
                      <th className="py-2 px-4 text-left">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockImportHistory.map((item, idx) => (
                      <tr key={idx}>
                        <td className="py-2 px-4">{item.file}</td>
                        <td className="py-2 px-4">{item.date}</td>
                        <td className={`py-2 px-4 ${item.status === "Success" ? "text-green-600" : "text-red-600"}`}>{item.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {selected === "history" && (
            <div>
              <h2 className="text-2xl font-bold mb-4">History</h2>
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Import History</h3>
                <p className="text-gray-600 mb-2">Files uploaded, who uploaded, when, and status (placeholder).</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Sales History</h3>
                <p className="text-gray-600 mb-2">View historical sales data (filterable) (placeholder).</p>
              </div>
            </div>
          )}
          {selected === "settings" && (
            <div>
              <h2 className="text-2xl font-bold mb-4">Settings</h2>
              <Tabs value={settingsTab} onValueChange={setSettingsTab} className="mb-6">
                <TabsList>
                  <TabsTrigger value="shop">Shop Details</TabsTrigger>
                  <TabsTrigger value="notifications">Notification Settings</TabsTrigger>
                  <TabsTrigger value="backup">Backup & Restore</TabsTrigger>
                </TabsList>
                <TabsContent value="shop">
                  <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">Shop Details</h3>
                    <p className="text-gray-600 mb-2">Name, address, logo, contact (placeholder).</p>
                  </div>
                </TabsContent>
                <TabsContent value="notifications">
                  <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">Notification Settings</h3>
                    <p className="text-gray-600 mb-2">Low stock alerts, sales drop alerts (placeholder).</p>
                  </div>
                </TabsContent>
                <TabsContent value="backup">
                  <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2">Backup & Restore</h3>
                    <p className="text-gray-600 mb-2">Manual backup / restore data (placeholder).</p>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          )}
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};

export default OpenPage;
