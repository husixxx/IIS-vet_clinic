<template>
 <Dialog :header="header" :visible="isVisible" :modal="true" :closable="false">
   <div class="p-fluid dialog-form-container">
     <div class="p-field" v-for="field in fields">
       <label :for="field.id" class="dialog-input-label">{{ field.label }}</label>
       <component
        v-if="field.component !== 'file'"
         :is="field.component"
         v-model="model[field.model]"
         v-bind="field.props"
         class="dialog-input-field"
         :invalid="!model[field.model]"
       />
       <div v-else>
         <input
           type="file"
           :accept="field.props.accept"
           @change="handleFileUpload"
           class="file-input"
         />
       </div>
     </div>
   </div>
   <template #footer>
     <Button :label="onSaveAddButtonLabel" @click="onSaveAdd" class="p-button-success" :disabled="isNotFilledForm(model)"/>
     <Button label="Cancel" @click="onCancel" class="p-button-secondary" />
   </template>
 </Dialog>
</template>
  
<script>

import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';

export default {
  props: {
    header: String,
    isVisible: Boolean,
    fields: Array,
    model: Object,
    onSaveAdd: Function,
    onCancel: Function,
    onSaveAddButtonLabel: String
  },
  components: {
    Dialog,
    Button,
    Dropdown
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const validTypes = ['image/jpeg'];
        if (!validTypes.includes(file.type)) {
          alert('Only JPEG photos are allowed.');
          this.model.photo = null; // Reset the file if it's not a valid type
          event.target.value = ''; // Reset the file input
          // this.$emit('file-invalid'); // Optional event to notify invalid file
          return;
        }
        // console.log('File uploaded:', file);
        // You can store the file in your state or emit it as an event
        this.model.photo = file; // Attach file to the model if necessary
      }
    },
    isNotFilledForm(formItems) {
      for(const [key, value] of Object.entries(formItems)) {
        // console.log(key, value);
        if(!value && key !== 'photo') {
          return true;
        }
      }

      return false;
    }
  },
}

</script>

<style scoped>

.dialog-form-container {
  display: flex;
  flex-direction: column;
}

.p-field {
  display: flex;
  align-items: center; 
  margin-bottom: 10px;
}

.dialog-input-label {
  width: 122px;
  margin-right: 20px;
}

.dialog-input-field {
  flex: 1;
  box-sizing: border-box;
}

</style>
  