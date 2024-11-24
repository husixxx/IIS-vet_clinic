import { defineStore } from 'pinia';
import axiosClient from '../api/api';  // Import axios client pre API requesty

export enum UserRole {
  Volunteer = 1,
  Veterinarian,
  Caretaker,
  Admin,
  UnverifVolunteer
}

// Definícia používateľskej štruktúry
interface User {
  username: string;
  id: number;
  role_id: number;
}

interface AuthState {
  user: User | null;  // Používateľ môže byť null, ak nie je prihlásený
  syncInitialized: boolean;  // Zabezpečí, že listener sa pridá iba raz
}


export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,  // Na začiatku nie je prihlásený žiadny používateľ
    syncInitialized: false,  // Zabezpečí, že listener sa pridá iba raz
  }),
  getters: {
    isLoggedIn: (state): boolean => !!state.user,
    getUser: (state): User | null => state.user,
    getRoleId: (state): number | null => state.user ? state.user.role_id : null,
  },
  actions: {
    login(user: User) {
      this.user = user;
      localStorage.setItem('authChange', JSON.stringify({
        loggedIn: true,
        user: this.user,
        timestamp: Date.now(),
      }));
    },
    async logout() {
      this.user = null;
      localStorage.setItem('authChange', JSON.stringify({
        loggedIn: false,
        user: null,
        timestamp: Date.now(),
      }));
    },
    syncAuthState() {
      if (this.syncInitialized) return; // Listener už existuje
      this.syncInitialized = true;

      window.addEventListener('storage', (event) => {
        if (event.key === 'authChange') {
          const authState = JSON.parse(event.newValue || '{}');
          if (authState.loggedIn && authState.user && !this.isLoggedIn) {
            this.user = authState.user;
            console.log("User logged in from another tab");
            location.reload(); // Refreš iba, ak sa prihlásil
          }
          if (!authState.loggedIn && this.isLoggedIn) {
            this.user = null;
            console.log("User logged out from another tab");
            location.reload(); // Refreš iba, ak sa odhlásil
          }
        }
      });
    },
  },
});


