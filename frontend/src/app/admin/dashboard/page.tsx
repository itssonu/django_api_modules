'use client'

import ProtectedRoute from '@/components/ProtectedRoute'
import { useAuth } from '@/contexts/AuthContext'
import React from 'react'

const Dashboard = () => {
    const { logout } = useAuth()

    return (
        <ProtectedRoute>
            <div>Dashboard</div>
            <button type='button' onClick={logout}>logout</button>
        </ProtectedRoute>
    )
}

export default Dashboard