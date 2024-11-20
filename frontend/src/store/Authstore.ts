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
    },
    async logout() {
      try {
        await axiosClient.post('/authorization/sign_out', null, { withCredentials: true });
        this.user = null;
      } catch (error) {
        console.error("Error during sign out:", error);
        alert('Error during sign out');
      }
    }
  },
});
