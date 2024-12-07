'use client';
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
    authToken: string | null;
    login: (email: string, password: string) => Promise<void>;
    signup: ({ email, password, last_name, first_name, dob, profile_image }: {
        email: string,
        password: string,
        first_name: string,
        last_name: string,
        dob: string,
        profile_image: File | null
    }) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [authToken, setAuthToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('authToken');
        if (token) {
            // Validate token with your backend
            setAuthToken(token);
        }
        setIsLoading(false);
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/user/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) throw new Error('Login failed');

            const { data } = await response.json();
            localStorage.setItem('authToken', data.accessToken);
            setAuthToken(data?.accessToken);
        } catch (error) {
            throw error;
        }
    };

    const signup = async ({ email, password, last_name, first_name, dob, profile_image }: {
        email: string,
        password: string,
        first_name: string,
        last_name: string,
        dob: string,
        profile_image: File | null
    }
    ) => {
        try {
            const formData = new FormData();
            formData.append('email', email);
            formData.append('password', password);
            formData.append('first_name', first_name);
            formData.append('last_name', last_name);
            formData.append('dob', dob);
            if (profile_image) formData.append('profile_image', profile_image);

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/user/register`, {
                method: 'POST',
                // headers: {
                //     'Content-Type': 'multipart/form-data',
                // },
                body: formData,
            });

            if (!response.ok) throw new Error('Signup failed');

            const { data } = await response.json();
            localStorage.setItem('authToken', data.accessToken);
            setAuthToken(data.accessToken);
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        setAuthToken(null);
    };

    return (
        <AuthContext.Provider value={{ authToken, login, signup, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}