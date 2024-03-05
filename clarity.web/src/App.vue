<template>
  <Suspense>
    <Dashboard />

    <template #fallback>
      Loading...
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import Dashboard from "./components/Dashboard.vue";
</script>

<style>
html, body {
  @apply bg-gray-100;
}

#app {
  @apply mx-auto container max-w-[980px] px-6;
}
</style>
