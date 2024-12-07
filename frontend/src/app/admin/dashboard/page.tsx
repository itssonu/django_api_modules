import ProtectedRoute from '@/components/ProtectedRoute'
import React from 'react'

const Dashboard = () => {
    return (
        <ProtectedRoute>
            <div>Dashboard</div>
        </ProtectedRoute>
    )
}

export default Dashboard