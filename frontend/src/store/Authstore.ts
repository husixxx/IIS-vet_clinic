import { defineStore } from 'pinia';

export enum UserRole {
  Volunteer = 1,
  Veterinarian,
  Caretaker,
  Admin,
  UnverifVolunteer
}

// Define the structure of your user object
interface User {
  email: string;
  id: number;
  role_id: number;  // Store role_id directly
}

interface AuthState {
  user: User | null;  // User will be null if not logged in
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
  }),
  getters: {
    isLoggedIn: (state): boolean => !!state.user,
    getUser: (state): User | null => state.user,  // Return user directly
    getRoleId: (state): number | null => state.user ? state.user.role_id : null,  // Access role_id directly
  },
  actions: {
    login(user: User) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user)); // Persist user data
    },
    logout() {
      this.user = null;
      localStorage.removeItem('user');
    },
    loadUserFromStorage() {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        this.user = JSON.parse(storedUser);
      }
    },
  },
});
