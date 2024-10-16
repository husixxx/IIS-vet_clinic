<template>
    <div>
        <div class="card">
            <DataTable :value="volunteers" tableStyle="min-width: 50rem">
                <Column field="id" header="ID"></Column>
                <Column field="name" header="Name"></Column>
                <Column field="email" header="Email"></Column>
                <Column header="Status">
                    <template #body="slotProps">
                        <span v-if="slotProps.data.role_id === 1">Verified</span>
                        <span v-else-if="slotProps.data.role_id === 5">Unverified</span>
                    </template>
                </Column>
                <Column header="Actions">
                    <template #body="slotProps">
                        <Button
                            v-if="slotProps.data.role_id === 5"
                            label="Verify"
                            @click="verifyVolunteer(slotProps.data)"
                            class="p-button-success"
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button'; // Import Button from PrimeVue
import axiosClient from '../api/api';

// Reactive reference to hold volunteer data
const volunteers = ref([]);

// Fetch volunteers on component mount
onMounted(async () => {
    try {
        // Make a GET request to the Flask API to fetch unverified volunteers
        const response = await axiosClient.get('/caretaker/unverified_volunteers');
        // Populate the table with the response data
        volunteers.value = response.data;
    } catch (error) {
        console.error('Error fetching unverified volunteers:', error);
    }
});

// Function to verify a volunteer
const verifyVolunteer = async (volunteer) => {
    try {
        // Call the updated verification endpoint with the correct query parameter 'id'
        const response = await axiosClient.post(`/caretaker/verify_volunteer?id=${volunteer.id}`);

        if (response.data.verified) {
            // Update the local role_id to 1 if verified successfully
            volunteer.role_id = 1;
            alert(`Volunteer ${volunteer.name} was verified successfully.`);
        }
    } catch (error) {
        console.error('Error verifying volunteer:', error);
        alert('Failed to verify the volunteer.');
    }
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
