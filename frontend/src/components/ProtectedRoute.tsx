'use client';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const { authToken, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && !authToken) {
            router.push('/auth/login');
        }
    }, [authToken, isLoading, router]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return authToken ? <>{children}</> : null;
}