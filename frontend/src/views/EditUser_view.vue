<template>
  <h1>Edit users</h1>
  <div class="edit-users-container">
    <Card class="full-width-card">
      <template #content>
        <div class="p-fluid no-padding">
          <!-- DataTable for displaying users -->
          <DataTable :value="users" class="p-datatable-striped full-width-table">
            <Column field="id" header="ID"></Column>
            <Column field="name" header="Name"></Column>
            <Column field="email" header="Email"></Column>
            <Column field="username" header="Username"></Column>
            <Column field="verified" header="Verified"></Column>
            <Column field="role" header="Role"></Column>
            <Column header="">
              <template #body="slotProps">
                <Button
                  label="Edit"
                  @click="openEditModal(slotProps.data)"
                  class="p-button-warning p-button-sm"
                />
                <Button
                  label="Delete"
                  @click="confirmDelete(slotProps.data)"
                  class="p-button-danger p-button-sm"
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

    <!-- Confirmation dialog for deletion -->
    <Dialog header="Confirm Delete" v-model:visible="showDeleteDialog" :modal="true" :closable="true" :style="{ width: '30vw' }">
      <p>Are you sure you want to delete this user?</p>
      <template #footer>
        <Button label="Yes" @click="deleteUser" class="p-button-danger" />
        <Button label="No" @click="closeDeleteDialog" class="p-button-secondary" />
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
const showDeleteDialog = ref(false);  // New state for delete dialog
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

// Open edit modal
const openEditModal = async (user) => {
  selectedUser.id = user.id;
  selectedUser.name = user.name;
  selectedUser.email = user.email;
  selectedUser.username = user.username;
  selectedUser.password = ''; // Leave password empty for security
  selectedUser.verified = user.verified;
  selectedUser.role_id = user.role_id;
  showEditDialog.value = true;
};

// Close edit modal
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

// Function to open delete confirmation dialog
const confirmDelete = (user) => {
  selectedUser.id = user.id; // Set the selected user's id for deletion
  showDeleteDialog.value = true;  // Show the delete confirmation dialog
};

// Function to close delete confirmation dialog
const closeDeleteDialog = () => {
  showDeleteDialog.value = false;
};

// Function to delete the user
const deleteUser = async () => {
  try {
    const response = await axiosClient.delete(`/admin/delete_user`, {
      params: { user_id: selectedUser.id }
    });
    if (response.status === 200) {
      alert('User deleted successfully!');
      closeDeleteDialog();
      // Refresh the user list
      onMounted();
    }
  } catch (error) {
    console.error('Error deleting user:', error);
    alert('Failed to delete user.');
  }
};
</script>

<style scoped>
.edit-users-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-left: 20px;
  padding-right: 20px;
  width: 100%;
}

.full-width-card {
  width: 100%;
  border-radius: 0; /* Remove rounded corners */
  margin: 0; /* Ensure no margin around the card */
}

.no-padding {
  padding: 0 !important;
}

.full-width-table {
  width: 100%;
  border-radius: 0; /* Ensure the table also has no rounded corners */
}

.p-button-warning {
  margin: 0 5px;
}

h1 {
  text-align: center;
  margin-bottom: 20px; /* Optional margin-bottom for consistency */
}

/* Ensure no border-radius, padding, or margin in the table */
.p-datatable {
  margin-top: 0; /* Ensure no top margin */
  padding: 0; /* Remove padding from the DataTable */
  border-radius: 0; /* Remove border radius */
  border: none; /* Remove any borders */
}

/* Ensure the table wrapper also has no border-radius or padding */
.p-datatable-wrapper {
  border-radius: 0;
  padding: 0;
}

.p-field {
  display: flex;
  justify-content: space-between; /* Align label and input */
  align-items: center;
  margin-bottom: 1.2rem;
}

.input-label {
  width: 120px;
  margin-right: 10px;
  font-size: 1rem;
}

.input-field {
  flex-grow: 1;
}

.p-dialog .p-fluid {
  padding: 20px; /* Consistent padding for the modal */
}

.p-button-success,
.p-button-secondary {
  margin: 10px 5px; /* Spacing between the buttons */
}


</style>
