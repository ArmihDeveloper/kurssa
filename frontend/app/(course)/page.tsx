// This will be the main mind map navigation page
export default function CoursePage() {
  return (
    <div>
      <h1 className="text-3xl font-poppins text-primary mb-4">Course Mind Map</h1>
      <p className="text-textMain mb-4">
        The interactive mind map will be rendered here, allowing users to navigate through chapters and sections.
      </p>
      {/* Placeholder for Mind Map Component */}
      <div className="w-full h-[600px] bg-gray-200 border border-gray-300 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Mind Map Component Placeholder</p>
      </div>
    </div>
  );
}
