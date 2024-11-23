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
            <Column header="Actions">
              <template #body="slotProps">
                <!-- Button for editing user - visible only for verified users -->
                <Button
                  v-if="slotProps.data.verified"
                  label="Edit"
                  @click="openEditModal(slotProps.data)"
                  class="p-button-warning p-button-sm"
                />
                <!-- Button for deleting user -->
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
            :invalid="
              field.model === 'email'
                ? !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(selectedUser.email)
                : field.model !== 'password' && !selectedUser[field.model]"
            class="input-field"
          />
        </div>
      </div>
      <template #footer>
        <Button
          label="Save"
          @click="updateUser"
          class="p-button-success"
          :disabled="!selectedUser.name || !selectedUser.email || !selectedUser.username || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(selectedUser.email)"
        />
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
});


const fields = [
  { id: 'name', label: 'Name', model: 'name', component: InputText, props: { maxlength: 61 } },
  { id: 'email', label: 'Email', model: 'email', component: InputText, props: { maxlength: 50 } },
  { id: 'username', label: 'Username', model: 'username', component: InputText, props: { maxlength: 30 } },
  { id: 'password', label: 'Password', model: 'password', component: InputText, props: { type: 'password', maxlength: 30 } },
];

// Fetch all users on component mount
onMounted(async () => {
  try {
    const response = await axiosClient.get('/admin/users', {
      withCredentials: true  // Zabezpečí, že cookies budú odoslané a prijaté
    });
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
  showEditDialog.value = true;
};

// Close edit modal
const closeEditModal = async () => {
  showEditDialog.value = false;
};

const updateUser = async () => {
  try {
    // Format the request properly, ensuring verified is a boolean and role_id is an integer
    const response = await axiosClient.put(`/admin/update_user?user_id=${selectedUser.id}&name=${selectedUser.name}&email=${selectedUser.email}&username=${selectedUser.username}&password=${selectedUser.password}`,null,{withCredentials: true});
    if (response.status === 200) {
      alert('User updated successfully!');
      closeEditModal();
      // Refresh the user list
      onMounted();
    }
  } 
  catch (error) {
  if (error.response) {

    const status = error.response.status;
    const error_msg = error.response.data.error;
    console.error(`Error Status: ${status}`);
    alert(error_msg);
  } else {

    console.error("Error:", error.message);
    alert("Something went wrong. Please try again later.");
  }
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
      params: { user_id: selectedUser.id },
      withCredentials: true  // Zabezpečí, že cookies budú odoslané a prijaté
    });
    if (response.status === 200) {
      closeDeleteDialog();
      // Refresh the user list
      location.reload();
    }
  }catch (error) {
  if (error.response) {

    const status = error.response.status;
    const error_msg = error.response.data.error;
    console.error(`Error Status: ${status}`);
    alert(error_msg);
  } else {

    console.error("Error:", error.message);
    alert("Something went wrong. Please try again later.");
  }
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
  padding-bottom: 100px;
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
.p-button-secondary
.p-button-danger {
  margin: 10px 5px; /* Spacing between the buttons */
}


</style>
