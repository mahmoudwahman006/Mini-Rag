"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import UploadPanel from "@/components/UploadPanel";
import ProcessPanel from "@/components/ProcessPanel";
import IndexPushPanel from "@/components/IndexPushPanel";
import IndexInfoPanel from "@/components/IndexInfoPanel";
import SearchPanel from "@/components/SearchPanel";

const PANELS = {
  upload: UploadPanel,
  process: ProcessPanel,
  push: IndexPushPanel,
  info: IndexInfoPanel,
  search: SearchPanel,
};

export default function Home() {
  const [active, setActive] = useState("upload");
  const [projectId, setProjectId] = useState("");

  const ActivePanel = PANELS[active];

  return (
    <div className="flex h-screen bg-[var(--bg)] text-[var(--text)]">
      <Sidebar
        active={active}
        onSelect={setActive}
        projectId={projectId}
        onProjectIdChange={setProjectId}
      />
      <main className="flex-1 overflow-y-auto px-10 py-10">
        <div className="mx-auto max-w-3xl">
          <ActivePanel projectId={projectId} />
        </div>
      </main>
    </div>
  );
}
