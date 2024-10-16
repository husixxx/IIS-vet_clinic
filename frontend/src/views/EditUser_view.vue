<template>
    <div class="edit-users-container">
      <Card class="full-width-card">
        <template #title>
          <div class="title-center">Edit Users</div>
        </template>
        <template #content>
          <div class="p-fluid">
            <!-- DataTable for displaying users -->
            <DataTable :value="users" class="full-width-table" tableStyle="width: 100%">
              <Column field="id" header="ID" style="width: 10%;"></Column>
              <Column field="name" header="Name" style="width: 25%;"></Column>
              <Column field="email" header="Email" style="width: 35%;"></Column>
              <Column field="role_id" header="Role ID" style="width: 10%;"></Column>
              <Column style="width: 20%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Edit"
                    @click="editUser(slotProps.data)"
                    class="p-button-warning"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Button from 'primevue/button';
  import Card from 'primevue/card';
  import axiosClient from '../api/api';  // Ensure correct path to your API client
  
  // Reactive reference to hold user data
  const users = ref([]);
  
  // Fetch all users on component mount
  onMounted(async () => {
    try {
      const response = await axiosClient.get('/admin/users');
      users.value = response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  });
  
  // Function to handle editing a user
  const editUser = (user) => {
    // Redirect to an edit form with user ID or open a modal for editing
    alert(`Edit user: ${user.name}`);
    // Implement the edit functionality as needed
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
  
  .table-actions {
    display: flex;
    justify-content: center;
  }
  </style>
  