export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold font-poppins text-primary mb-6">
          Welcome to the AI Agents Course Platform
        </h1>
        <p className="text-lg text-textMain mb-8">
          Interactive learning experience with mind map-style navigation.
        </p>
        <button className="bg-interactive text-white font-poppins py-3 px-6 rounded-lg hover:bg-opacity-90 transition-colors">
          Explore Courses (Coming Soon)
        </button>
      </div>
    </main>
  );
}
