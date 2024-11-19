<template>
 <Dialog :header="header" :visible="isVisible" :modal="true" :closable="false">
   <div class="p-fluid dialog-form-container">
     <div class="p-field" v-for="field in fields">
       <label :for="field.id" class="dialog-input-label">{{ field.label }}</label>
       <component
         :is="field.component"
         v-model="model[field.model]"
         v-bind="field.props"
         class="dialog-input-field"
         :invalid="!model[field.model]"
       />
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
    Button
  },
  methods: {
    isNotFilledForm(formItems) {
      for(const [key, value] of Object.entries(formItems)) {
        console.log(key, value);
        if(!value) {
          return true;
        }
      }

      return false;
    }
  }
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
  