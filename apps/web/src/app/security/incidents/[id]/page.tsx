import { IncidentDetailWorkspace } from "@/components/admin/IncidentDetailWorkspace";

export const metadata = {
  title: "Incident Response Workspace | Vapor OS",
  description: "Detailed incident workspace, threat chain graph, response plan diff, and recovery verification"
};

export default function IncidentDetailPage({ params }: { params: { id: string } }) {
  return <IncidentDetailWorkspace incidentId={params.id} />;
}
