import type { Metadata } from "next";
import { MaintenanceScreen } from "@/components/maintenance-screen";

export const metadata: Metadata = {
  title: "Temporarily Unavailable | Juang Group",
  description:
    "The Juang Group website is temporarily unavailable while final project arrangements are being completed.",
};

export default function MaintenancePage() {
  return <MaintenanceScreen />;
}
