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
import DashSection from "./dash";
import HistorySection from "./history";
import ImportSection from "./import";
import SettingsSection from "./settings";

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

  // Sorting state for history table
  const [sortAsc, setSortAsc] = useState(false);
  const [sortedFiles, setSortedFiles] = useState<any[]>([]);
  useEffect(() => {
    const sorted = [...userFiles].sort((a, b) => {
      const dateA = new Date(a.uploadDate).getTime();
      const dateB = new Date(b.uploadDate).getTime();
      return sortAsc ? dateA - dateB : dateB - dateA;
    });
    setSortedFiles(sorted);
  }, [userFiles, sortAsc]);

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
            <DashSection
              userName={userName}
              period={period}
              handlePeriodChange={handlePeriodChange}
              selectedCategories={selectedCategories}
              categoryOpen={categoryOpen}
              setCategoryOpen={setCategoryOpen}
              handleCategoryToggle={handleCategoryToggle}
            />
          )}
          {selected === "import" && (
            <ImportSection
              handleFileChange={handleFileChange}
              handleUpload={handleUpload}
              selectedFiles={selectedFiles}
              uploadStatus={uploadStatus}
            />
          )}
          {selected === "history" && (
            <HistorySection
              multiDeleteMode={multiDeleteMode}
              setMultiDeleteMode={setMultiDeleteMode}
              selectedForDelete={selectedForDelete}
              setSelectedForDelete={setSelectedForDelete}
              handleMultiDelete={handleMultiDelete}
              handleDeleteFile={handleDeleteFile}
              handleSelectAll={handleSelectAll}
              sortAsc={sortAsc}
              setSortAsc={setSortAsc}
              sortedFiles={sortedFiles}
            />
          )}
          {selected === "settings" && (
            <SettingsSection
              settingsTab={settingsTab}
              setSettingsTab={setSettingsTab}
              handleLogout={handleLogout}
            />
          )}
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};

export default OpenPage;
