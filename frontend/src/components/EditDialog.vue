<template>
    <Dialog :header="header" v-model:visible="isVisible" :modal="true" :closable="true" :style="{ width: '50vw' }">
      <div class="p-fluid">
        <div class="p-field" v-for="field in fields" :key="field.id">
          <label :for="field.id" class="input-label">{{ field.label }}</label>
          <component
            :is="field.component"
            v-model="model[field.model]"
            v-bind="field.props"
            :id="field.id"
            class="input-field"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Save" @click="onSave" class="p-button-success" />
        <Button label="Cancel" @click="onCancel" class="p-button-secondary" />
      </template>
    </Dialog>
</template>
  
<script>

export default {
  props: {
    header: String,
    isVisible: Boolean,
    fields: Array,
    model: Object,
    onSave: Function,
    onCancel: Function
  }
}

</script>
  