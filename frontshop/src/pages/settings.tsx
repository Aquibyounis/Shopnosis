import React from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";

export default function SettingsSection({
  settingsTab,
  setSettingsTab,
  handleLogout
}) {
  return (
    <div className="w-full px-12 flex flex-col items-center justify-center">
      <br />
      <h2 className="text-3xl font-black mb-8 w-full text-left text-blue-900">
        Settings
      </h2>
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
  );
}
