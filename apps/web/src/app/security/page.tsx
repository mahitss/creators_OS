import { SecurityFabricWorkspace } from "@/components/admin/SecurityFabricWorkspace";

export const metadata = {
  title: "Security & Threat Intelligence Fabric | Vapor OS",
  description: "Enterprise defense-in-depth agent security, zero-trust control plane, threat detection & quarantine management"
};

export default function SecurityPage() {
  return <SecurityFabricWorkspace />;
}
