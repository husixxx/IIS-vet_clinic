<template>
  <div class="edit-users-container">
    <Card class="full-width-card">
      <template #content>
        <div class="p-fluid">
          <!-- DataTable for displaying users -->
          <DataTable :value="users" class="full-width-table" tableStyle="width: 100%">
            <Column field="id" header="ID" style="width: 10%;"></Column>
            <Column field="name" header="Name" style="width: 15%;"></Column>
            <Column field="email" header="Email" style="width: 20%;"></Column>
            <Column field="username" header="Username" style="width: 15%;"></Column>
            <Column field="verified" header="Verified" style="width: 10%;"></Column>
            <Column field="role" header="Role" style="width: 10%;"></Column>
            <Column header="" style="width: 20%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
              <template #body="slotProps">
                <Button
                  label="Edit"
                  @click="openEditModal(slotProps.data)"
                  class="p-button-warning"
                />
              </template>
            </Column>
          </DataTable>
        </div>
      </template>
    </Card>

    <!-- Modal for editing user details -->
    <Dialog header="Edit User" v-model:visible="showEditDialog" :modal="true" :closable="true" :style="{ width: '50vw' }">
      <div class="p-fluid">
        <div class="p-field" v-for="field in fields" :key="field.id">
          <label :for="field.id" class="input-label">{{ field.label }}</label>
          <component
            :is="field.component"
            v-model="selectedUser[field.model]"
            v-bind="field.props"
            :id="field.id"
            class="input-field"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Save" @click="updateUser" class="p-button-success" />
        <Button label="Cancel" @click="closeEditModal" class="p-button-secondary" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import axiosClient from '../api/api';  // Ensure correct path to your API client

// Reactive reference to hold user data
const users = ref([]);
const showEditDialog = ref(false);
const selectedUser = reactive({
  id: null,
  name: '',
  email: '',
  username: '',
  password: '',
  verified: null,
  role_id: null
});

// Options for the verified field
const verifiedOptions = [
  { label: 'Verified', value: true },
  { label: 'Unverified', value: false }
];

// Options for role_id field
const roleOptions = [
  { label: 'Admin', value: 4 },
  { label: 'Caretaker', value: 3 },
  { label: 'Volunteer', value: 1 },
  { label: 'Veterinarian', value: 2 },
  { label: 'Unverified User', value: 5 }
];

// Fields configuration for the form
const fields = [
  { id: 'name', label: 'Name', model: 'name', component: InputText },
  { id: 'email', label: 'Email', model: 'email', component: InputText },
  { id: 'username', label: 'Username', model: 'username', component: InputText },
  { id: 'password', label: 'Password', model: 'password', component: InputText, props: { type: 'password' } },
  { id: 'verified', label: 'Verified', model: 'verified', component: Dropdown, props: { options: verifiedOptions, optionLabel: 'label' } },
  { id: 'role_id', label: 'Role', model: 'role_id', component: Dropdown, props: { options: roleOptions, optionLabel: 'label' } }
];

// Fetch all users on component mount
onMounted(async () => {
  try {
    const response = await axiosClient.get('/admin/users');
    users.value = response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
});

const openEditModal = async (user) => {
  selectedUser.id = user.id;
  selectedUser.name = user.name;
  selectedUser.email = user.email;
  selectedUser.username = user.username;
  selectedUser.password = ''; // Leave password empty for security

  // Set the verified value directly as a boolean
  selectedUser.verified = user.verified;

  // Set the role_id directly as an integer
  selectedUser.role_id = user.role_id;

  showEditDialog.value = true;
};


// Function to close the edit modal
const closeEditModal = async () => {
  showEditDialog.value = false;
};

const updateUser = async () => {
  try {
    // Format the request properly, ensuring verified is a boolean and role_id is an integer
    const response = await axiosClient.put(`/admin/update_user?user_id=${selectedUser.id}&name=${selectedUser.name}&email=${selectedUser.email}&username=${selectedUser.username}&password=${selectedUser.password}&verified=${selectedUser.verified.value}&role_id=${selectedUser.role_id.value}`);
    if (response.status === 200) {
      alert('User updated successfully!');
      closeEditModal();
      // Refresh the user list
      onMounted();
    }
  } catch (error) {
    console.error('Error updating user:', error);
    alert('Failed to update user.');
  }
};
</script>

<style scoped>
.edit-users-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
  width: 100%;
}

.full-width-card {
  width: 100%;
}

.title-center {
  text-align: center;
  font-size: 1.5rem;
}

.full-width-table {
  width: 100%;
}

.p-button-warning {
  margin: 0 5px;
}

.p-field {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.input-label {
  width: 120px; /* Set a fixed width for labels */
  margin-right: 10px;
  font-size: 1rem;
}

.input-field {
  flex-grow: 1;
}

.table-actions {
  display: flex;
  justify-content: center;
}
</style>
