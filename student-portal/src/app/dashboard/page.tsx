'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

interface User {
  id: number
  username: string
  email: string
  role: string
  full_name: string
}

interface StudentResult {
  id: number
  student_id: string
  student_name: string
  class_name: string
  session: string
  term: string
  subjects: string
  total_score: number
  average_score: number
  grade: string
  position?: string
  remarks?: string
}

export default function StudentDashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [results, setResults] = useState<StudentResult[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedResult, setSelectedResult] = useState<StudentResult | null>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token || !userData) {
      router.push('/login')
      return
    }

    try {
      const user = JSON.parse(userData)
      setUser(user)
      fetchResults(user.username, token)
    } catch (err) {
      router.push('/login')
      return
    }
  }, [router])

  const fetchResults = async (studentId: string, token: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/results?student_id=${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        setResults(data)
      }
    } catch (err) {
      console.error('Failed to fetch results:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A': return 'text-green-600 bg-green-100'
      case 'B': return 'text-blue-600 bg-blue-100'
      case 'C': return 'text-yellow-600 bg-yellow-100'
      case 'D': return 'text-orange-600 bg-orange-100'
      case 'F': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your results...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Student Portal</h1>
              <p className="text-gray-600">Welcome, {user?.full_name}</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Student Info Card */}
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Student Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">Student ID</p>
                <p className="font-medium">{user?.username}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Full Name</p>
                <p className="font-medium">{user?.full_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="font-medium">{user?.email}</p>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Academic Results</h2>
            </div>
            
            {results.length === 0 ? (
              <div className="p-6 text-center">
                <p className="text-gray-500">No results available yet.</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {results.map((result) => (
                  <div key={result.id} className="p-6 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-lg font-medium text-gray-900">
                          {result.session} - {result.term}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Class: {result.class_name}
                        </p>
                        <div className="mt-2 flex items-center space-x-4">
                          <span className="text-sm text-gray-500">
                            Total Score: <span className="font-medium">{result.total_score}</span>
                          </span>
                          <span className="text-sm text-gray-500">
                            Average: <span className="font-medium">{result.average_score.toFixed(2)}</span>
                          </span>
                          {result.position && (
                            <span className="text-sm text-gray-500">
                              Position: <span className="font-medium">{result.position}</span>
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getGradeColor(result.grade)}`}>
                          Grade {result.grade}
                        </span>
                        <button
                          onClick={() => setSelectedResult(result)}
                          className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                        >
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* School Info */}
          <div className="mt-6 bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">School Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-gray-900">Mayowa Nursery & Primary School</h3>
                <p className="text-gray-600">Oda Road, Akure, Ondo State, Nigeria</p>
                <p className="text-gray-600 mt-2">Established: 1995</p>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Contact Information</h3>
                <p className="text-gray-600">Phone: +234 XXX XXX XXXX</p>
                <p className="text-gray-600">Email: info@mayowaschool.edu.ng</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Result Details Modal */}
      {selectedResult && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Result Details - {selectedResult.session} {selectedResult.term}
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500">Class:</span>
                  <span className="font-medium">{selectedResult.class_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Total Score:</span>
                  <span className="font-medium">{selectedResult.total_score}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Average:</span>
                  <span className="font-medium">{selectedResult.average_score.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Grade:</span>
                  <span className={`px-2 py-1 rounded text-sm font-medium ${getGradeColor(selectedResult.grade)}`}>
                    {selectedResult.grade}
                  </span>
                </div>
                {selectedResult.position && (
                  <div className="flex justify-between">
                    <span className="text-gray-500">Position:</span>
                    <span className="font-medium">{selectedResult.position}</span>
                  </div>
                )}
                {selectedResult.remarks && (
                  <div>
                    <span className="text-gray-500">Remarks:</span>
                    <p className="font-medium mt-1">{selectedResult.remarks}</p>
                  </div>
                )}
              </div>
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedResult(null)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-md text-sm font-medium"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
