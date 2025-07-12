import React, { useState, useEffect, useRef } from "react";
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { CalendarIcon, ChevronsUpDown } from "lucide-react";
import { Calendar } from "@/components/ui/calendar";
import { format } from "date-fns";
import type { DateRange } from "react-day-picker";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Trash2 } from "lucide-react";

const API_URL = "http://localhost:4000";

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

const OpenPage = () => {
  const [selected, setSelected] = useState("dashboard");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [settingsTab, setSettingsTab] = useState("shop");
  const [period, setPeriod] = useState("7d");
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [category, setCategory] = useState("All Categories");
  const [dateRange, setDateRange] = useState<[Date | null, Date | null]>([null, null]);
  const [startDate, endDate] = dateRange;
  const [dateRangeOpen, setDateRangeOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear().toString());
  const [selectedMonth, setSelectedMonth] = useState((new Date().getMonth() + 1).toString());
  const [startDateOpen, setStartDateOpen] = useState(false);
  const [endDateOpen, setEndDateOpen] = useState(false);

  // New states for user and files
  const [userName, setUserName] = useState("");
  const [userFiles, setUserFiles] = useState<any[]>([]);
  const [multiDeleteMode, setMultiDeleteMode] = useState(false);
  const [selectedForDelete, setSelectedForDelete] = useState<string[]>([]);

  // Get user name from localStorage on mount
  useEffect(() => {
    const name = localStorage.getItem("user-name");
    setUserName(name || "");
  }, []);

  // Fetch user files from backend
  useEffect(() => {
    const token = localStorage.getItem("auth-token");
    if (!token) return;
    fetch(`${API_URL}/myfiles`, {
      headers: { "auth-token": token }
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) setUserFiles(data.files);
        else setUserFiles([]);
      })
      .catch(() => setUserFiles([]));
  }, []);

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem("auth-token");
    localStorage.removeItem("user-name");
    window.location.href = "/login";
  };

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
      setUploadStatus("");
    }
  };

  // Handle file upload to backend
  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    const token = localStorage.getItem("auth-token");
    if (!token) {
      setUploadStatus("You must be logged in to upload.");
      return;
    }

    setUploadStatus("Uploading...");
    let successCount = 0;
    let failCount = 0;

    for (let i = 0; i < selectedFiles.length; i++) {
      const formData = new FormData();
      formData.append("file", selectedFiles[i]);
      try {
        const res = await fetch(`${API_URL}/filesupload`, {
          method: "POST",
          headers: {
            "auth-token": token
          },
          body: formData
        });
        const data = await res.json();
        if (data.success) {
          successCount++;
        } else {
          failCount++;
        }
      } catch {
        failCount++;
      }
    }

    if (successCount > 0) {
      setUploadStatus(`Uploaded ${successCount} file(s) successfully${failCount ? `, ${failCount} failed` : ""}.`);
      // Optionally refresh file list if you want to see new uploads in history
      const token = localStorage.getItem("auth-token");
      if (token) {
        fetch(`${API_URL}/myfiles`, {
          headers: { "auth-token": token }
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) setUserFiles(data.files);
            else setUserFiles([]);
          })
          .catch(() => setUserFiles([]));
      }
    } else {
      setUploadStatus("No files were uploaded. Please try again.");
    }
  };

  const handleCategoryToggle = (category: string) => {
    setSelectedCategories(prev => 
      prev.includes(category) 
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const handlePeriodChange = (value: string) => {
    setPeriod(value);
    if (value !== "custom") {
      setDateRange([null, null]);
    }
  };

  // New function to handle file deletion
  const handleDeleteFile = async (fileId: string) => {
    if (!window.confirm("Are you sure you want to delete this file? This action cannot be undone.")) {
      return;
    }
    const token = localStorage.getItem("auth-token");
    if (!token) return;
    try {
      const res = await fetch(`${API_URL}/deletefile/${fileId}`, {
        method: "DELETE",
        headers: { "auth-token": token }
      });
      const data = await res.json();
      if (data.success) {
        setUserFiles(prev => prev.filter(f => f._id !== fileId));
      } else {
        alert("Failed to delete file: " + (data.error || "Unknown error"));
      }
    } catch {
      alert("Failed to delete file: Network/server error");
    }
  };

  // Multi-delete handler
  const handleMultiDelete = async () => {
    if (selectedForDelete.length === 0) return;
    if (!window.confirm("Are you sure you want to delete the selected files? This action cannot be undone.")) {
      return;
    }
    const token = localStorage.getItem("auth-token");
    if (!token) return;
    let deletedCount = 0;
    for (const fileId of selectedForDelete) {
      try {
        const res = await fetch(`${API_URL}/deletefile/${fileId}`, {
          method: "DELETE",
          headers: { "auth-token": token }
        });
        const data = await res.json();
        if (data.success) {
          deletedCount++;
        }
      } catch {
        // ignore error for individual file
      }
    }
    setUserFiles(prev => prev.filter(f => !selectedForDelete.includes(f._id)));
    setSelectedForDelete([]);
    setMultiDeleteMode(false);
    setUploadStatus(`${deletedCount} file(s) deleted.`);
  };

  // Select all handler
  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedForDelete(userFiles.map(f => f._id));
    } else {
      setSelectedForDelete([]);
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
                    
                    {period === "custom" && (
                      <div className="flex items-center space-x-2">
                        {/* Start Date Popover */}
                        <Popover open={startDateOpen} onOpenChange={setStartDateOpen}>
                          <PopoverTrigger asChild>
                            <Button
                              variant="outline"
                              className="w-[150px] justify-start text-left font-normal"
                              onClick={() => setStartDateOpen(true)}
                            >
                              {startDate ? format(startDate, "MMM dd, yyyy") : "Start date"}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className="w-auto p-0" align="start">
                            <DatePicker
                              selected={startDate}
                              onChange={(date: Date | null) => {
                                setDateRange([date, endDate]);
                                setStartDateOpen(false);
                              }}
                              dateFormat="MMM dd, yyyy"
                              showYearDropdown
                              scrollableYearDropdown
                              yearDropdownItemNumber={20}
                              inline
                              renderCustomHeader={({
                                date,
                                changeYear,
                                decreaseMonth,
                                increaseMonth,
                                prevMonthButtonDisabled,
                                nextMonthButtonDisabled,
                              }) => (
                                <div className="flex items-center justify-between px-2 py-1">
                                  <button
                                    onClick={decreaseMonth}
                                    disabled={prevMonthButtonDisabled}
                                    className="px-2"
                                  >
                                    {"<"}
                                  </button>
                                  <span className="font-semibold text-lg">
                                    {date.toLocaleString("default", { month: "long" })}
                                  </span>
                                  <select
                                    value={date.getFullYear()}
                                    onChange={({ target: { value } }) => changeYear(Number(value))}
                                    className="ml-2 border rounded px-1 py-0.5"
                                  >
                                    {Array.from({ length: 2050 - 1950 + 1 }, (_, i) => {
                                      const year = 1950 + i;
                                      return (
                                        <option key={year} value={year}>
                                          {year}
                                        </option>
                                      );
                                    })}
                                  </select>
                                  <button
                                    onClick={increaseMonth}
                                    disabled={nextMonthButtonDisabled}
                                    className="px-2"
                                  >
                                    {">"}
                                  </button>
                                </div>
                              )}
                            />
                          </PopoverContent>
                        </Popover>
                        <span className="mx-1 text-gray-500">-</span>
                        {/* End Date Popover */}
                        <Popover open={endDateOpen} onOpenChange={setEndDateOpen}>
                          <PopoverTrigger asChild>
                            <Button
                              variant="outline"
                              className="w-[150px] justify-start text-left font-normal"
                              onClick={() => setEndDateOpen(true)}
                            >
                              {endDate ? format(endDate, "MMM dd, yyyy") : "End date"}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className="w-auto p-0" align="start">
                            <DatePicker
                              selected={endDate}
                              onChange={(date: Date | null) => {
                                setDateRange([startDate, date]);
                                setEndDateOpen(false);
                              }}
                              dateFormat="MMM dd, yyyy"
                              showYearDropdown
                              scrollableYearDropdown
                              yearDropdownItemNumber={20}
                              inline
                              renderCustomHeader={({
                                date,
                                changeYear,
                                decreaseMonth,
                                increaseMonth,
                                prevMonthButtonDisabled,
                                nextMonthButtonDisabled,
                              }) => (
                                <div className="flex items-center justify-between px-2 py-1">
                                  <button
                                    onClick={decreaseMonth}
                                    disabled={prevMonthButtonDisabled}
                                    className="px-2"
                                  >
                                    {"<"}
                                  </button>
                                  <span className="font-semibold text-lg">
                                    {date.toLocaleString("default", { month: "long" })}
                                  </span>
                                  <select
                                    value={date.getFullYear()}
                                    onChange={({ target: { value } }) => changeYear(Number(value))}
                                    className="ml-2 border rounded px-1 py-0.5"
                                  >
                                    {Array.from({ length: 2050 - 1950 + 1 }, (_, i) => {
                                      const year = 1950 + i;
                                      return (
                                        <option key={year} value={year}>
                                          {year}
                                        </option>
                                      );
                                    })}
                                  </select>
                                  <button
                                    onClick={increaseMonth}
                                    disabled={nextMonthButtonDisabled}
                                    className="px-2"
                                  >
                                    {">"}
                                  </button>
                                </div>
                              )}
                            />
                          </PopoverContent>
                        </Popover>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <label className="text-sm font-medium text-gray-700">Categories:</label>
                    <Popover open={categoryOpen} onOpenChange={setCategoryOpen}>
                      <PopoverTrigger asChild>
                        <Button
                          variant="outline"
                          role="combobox"
                          aria-expanded={categoryOpen}
                          className="w-[200px] justify-between"
                        >
                          {selectedCategories.length === 0
                            ? "Select categories..."
                            : selectedCategories.length === 1
                            ? selectedCategories[0]
                            : `${selectedCategories.length} categories selected`}
                          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-[200px] p-0">
                        <Command>
                          <CommandInput placeholder="Search categories..." />
                          <CommandList>
                            <CommandEmpty>No category found.</CommandEmpty>
                            <CommandGroup>
                              {categoryOptions.map((category) => (
                                <CommandItem
                                  key={category}
                                  onSelect={() => handleCategoryToggle(category)}
                                >
                                  <Checkbox
                                    checked={selectedCategories.includes(category)}
                                    className="mr-2"
                                  />
                                  {category}
                                </CommandItem>
                              ))}
                            </CommandGroup>
                          </CommandList>
                        </Command>
                      </PopoverContent>
                    </Popover>
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
                <p className="text-gray-600 mb-2">
                  Upload a CSV or Excel file.{" "}
                  <a href="#" className="text-blue-600 underline">
                    Download required format template
                  </a>
                </p>
                <input
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleFileChange}
                  className="mb-2"
                  multiple
                />
                <button
                  className="ml-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                  onClick={handleUpload}
                  disabled={selectedFiles.length === 0}
                  type="button"
                >
                  Upload
                </button>
                {uploadStatus && (
                  <div className="mt-4 text-green-700 font-semibold">{uploadStatus}</div>
                )}
              </div>
            </div>
          )}
          {selected === "history" && (
            <div>
              <h2 className="text-2xl font-bold mb-4">Your Uploaded Files</h2>
              <div className="mb-4 flex items-center gap-4">
                <Button
                  variant={multiDeleteMode ? "destructive" : "outline"}
                  onClick={() => {
                    setMultiDeleteMode(!multiDeleteMode);
                    setSelectedForDelete([]);
                  }}
                >
                  {multiDeleteMode ? "Cancel Multi Delete" : "Delete Multiple"}
                </Button>
                {multiDeleteMode && (
                  <Button
                    variant="destructive"
                    onClick={handleMultiDelete}
                    disabled={selectedForDelete.length === 0}
                  >
                    Delete Selected
                  </Button>
                )}
              </div>
              <div className="mb-6">
                {userFiles.length === 0 ? (
                  <p className="text-gray-600">No files uploaded yet.</p>
                ) : (
                  <table className="min-w-full bg-white/80 rounded shadow">
                    <thead>
                      <tr>
                        {multiDeleteMode && (
                          <th className="py-2 px-4 text-left">
                            <input
                              type="checkbox"
                              checked={
                                selectedForDelete.length === userFiles.length && userFiles.length > 0
                              }
                              onChange={e => handleSelectAll(e.target.checked)}
                              aria-label="Select all files"
                            />
                          </th>
                        )}
                        <th className="py-2 px-4 text-left">File Name</th>
                        <th className="py-2 px-4 text-left">Original Name</th>
                        <th className="py-2 px-4 text-left">Upload Date</th>
                        <th className="py-2 px-4 text-left">Delete</th>
                      </tr>
                    </thead>
                    <tbody>
                      {userFiles.map((file, idx) => (
                        <tr key={file._id || idx}>
                          {multiDeleteMode && (
                            <td className="py-2 px-4">
                              <input
                                type="checkbox"
                                checked={selectedForDelete.includes(file._id)}
                                onChange={e => {
                                  if (e.target.checked) {
                                    setSelectedForDelete(prev => [...prev, file._id]);
                                  } else {
                                    setSelectedForDelete(prev => prev.filter(id => id !== file._id));
                                  }
                                }}
                                aria-label={`Select file ${file.filename}`}
                              />
                            </td>
                          )}
                          <td className="py-2 px-4">{file.filename}</td>
                          <td className="py-2 px-4">{file.originalname}</td>
                          <td className="py-2 px-4">{new Date(file.uploadDate).toLocaleString()}</td>
                          <td className="py-2 px-4">
                            <button
                              onClick={() => handleDeleteFile(file._id)}
                              className="text-red-600 hover:text-red-800"
                              title="Delete file"
                              disabled={multiDeleteMode}
                            >
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
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
                  <TabsTrigger value="logout">Logout</TabsTrigger>
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
                <TabsContent value="logout">
                  <div className="mt-4">
                    <Button
                      className="bg-red-600 hover:bg-red-700 text-white"
                      onClick={handleLogout}
                    >
                      Logout
                    </Button>
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
