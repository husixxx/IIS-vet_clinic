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
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,  // Na začiatku nie je prihlásený žiadny používateľ
  }),
  getters: {
    isLoggedIn: (state): boolean => !!state.user,  // Kontrola prihlásenia
    getUser: (state): User | null => state.user,  // Získanie používateľa
    getRoleId: (state): number | null => state.user ? state.user.role_id : null,  // Získanie role používateľa
  },
  actions: {
    login(user: User) {
      this.user = user;  // Nastavenie používateľa po úspešnom prihlásení

      // Synchronizácia s localStorage
      localStorage.setItem('authChange', JSON.stringify({
        loggedIn: true,
        user: this.user,
        timestamp: Date.now(),
      }));
    },
    async logout() {
      try {
        // API volanie na odhlásenie
        await axiosClient.post('/authorization/sign_out', null, { withCredentials: true });
        
        this.user = null;

        // Synchronizácia s localStorage
        localStorage.setItem('authChange', JSON.stringify({
          loggedIn: false,
          user: null,
          timestamp: Date.now(),
        }));
      } catch (error) {
        console.error("Error during sign out:", error);
        alert('Error during sign out');
      }
    },
    // Synchronizácia medzi tabmi/oknami
    syncAuthState() {
      window.addEventListener('storage', (event) => {
        if (event.key === 'authChange') {
          const authState = JSON.parse(event.newValue || '{}');
          if (authState.loggedIn && authState.user) {
            this.user = authState.user;  // Aktualizuj stav, keď sa používateľ prihlási
            console.log("User logged in from another tab");
          } else if (!authState.loggedIn) {
            this.user = null;  // Aktualizuj stav, keď sa používateľ odhlási
            console.log("User logged out from another tab");
          }
          location.reload();
        }
      });
    },
  },
});

