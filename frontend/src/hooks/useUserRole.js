import { useAuth, useUser } from "@clerk/clerk-react";

export function useUserRole() {
    const { isLoaded: isSessionLoaded, session } = useAuth();
    const { isLoaded: isUserLoaded, user } = useUser();
    
    const isLoading = !isSessionLoaded || !isUserLoaded;
    
    // Get role from user's public metadata directly
    const role = user?.publicMetadata?.role || 'user';
    const tier = user?.publicMetadata?.tier || 'free';
    
    const isAdmin = role === 'admin';
    const isPremium = tier === 'premium';

    return { role, tier, isAdmin, isPremium, isLoading };
}