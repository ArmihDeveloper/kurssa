import React from 'react';

export default function CourseLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Could add a shared course header or sidebar here later */}
      <main className="flex-grow p-20px">{children}</main>
      {/* Could add a shared course footer here later */}
    </div>
  );
}
