<script setup>
import { computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBell, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons'

const props = defineProps({
  msg: String,
  type: String
})

const icon = computed(() => {
  switch (props.type) {
    case 'info':
      return faBell
    case 'warning':
      return faTriangleExclamation
  }
  return null
})
</script>
<template>
  <div
    class="notification is-light is-flex is-justify-content-center is-align-items-center"
    :class="`is-${type}`"
  >
    <span class="icon is-medium">
      <FontAwesomeIcon :icon="icon" />
    </span>
    <p>{{ msg }}</p>
  </div>
</template>
