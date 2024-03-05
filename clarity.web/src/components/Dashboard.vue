<template>
  <header class="flex flex-col my-12">
    <time class="text-gray-500">{{ currentDateTimeFormatted }}</time>
    <span class="text-3xl font-semibold">{{ settings.header.title }}</span>
  </header>

  <main>
    <section>
      <h2 class="uppercase font-semibold mb-4">Applications</h2>
      <ul v-if="settings && settings.apps" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-x-9 gap-y-6">
        <li v-for="(app, index) in settings.apps" :key="`app-${index}`">
          <a :href="`http://${app.href}`" target="_blank" class="flex flex-row gap-3 items-center leading-tight">
            <img
              class="fill-current w-10 h-10"
              :src="app.icon ? `/custom/${app.icon}` : '/icons/server.svg'"
              :alt="`Icon for ${app.title}`"
            />

            <div class="flex flex-col">
              <div class="block uppercase font-medium text-sm">{{ app.title }}</div>
              <div class="block text-gray-500 font-light text-xs">{{ app.subtitle || app.host }}</div>
            </div>
          </a>
        </li>
      </ul>
    </section>
  </main>

  <footer class="flex flex-col sm:flex-row justify-between my-12 gap-1.5">
    <div class="flex gap-4 items-center text-sm font-light">
      <a class="text-gray-500">Homepage</a>
      <a class="text-gray-500">API</a>
      <a class="px-3 py-1 text-xs border border-red-500 text-red-500 rounded font-medium cursor-pointer">Report an issue</a>
    </div>
    <span class="text-gray-400 text-xs">Powered by Clarity</span>
  </footer>

  <teleport v-if="errors && errors.length" to="body">
    <div id="popup-modal" class="flex overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 bottom-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">

      <div class="p-4 w-full max-w-lg max-h-full z-50">
        <div class="relative bg-white rounded-lg shadow dark:bg-gray-700 z-50">
          <div class="p-4 md:p-5 flex flex-row gap-3 items-center">
            <svg class="text-red-500 w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
            <h3 class="text-lg">Invalid configuration</h3>
          </div>
          <div class="p-4 md:p-5 !pt-0">
            <p>Please re-check configuration file.</p>

            <div class="bg-gray-100 px-4 py-2 rounded-lg font-mono text-xs mt-3">
              <ul>
                <li v-for="error in errors">
                  <span class="font-medium">[{{ error.loc.join(':') }}]</span>
                  {{ error.msg }}
                </li>
              </ul>
            </div>
          </div>
          <div class="p-4 md:p-5 !pt-0">
            <button @click="reloadSettings" type="button" class="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 focus:z-10 focus:ring-4 focus:ring-gray-100">
              Reload configuration
            </button>
          </div>
        </div>
      </div>

      <div class="bg-gray-900/50 dark:bg-gray-900/80 fixed inset-0 z-40"></div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { format } from "date-fns";
import { computed, ref, onMounted, onUnmounted, Ref } from "vue";
import {Settings, ValidationError} from "../models/settings";

const settings: Ref<Settings> = ref(null)
const errors: Ref<ValidationError[]> = ref(null)
const currentDateTime: Ref<number> = ref(Date.now())

let timeUpdateInterval = null

const response = await fetch("/api/settings")
if (response.ok) {
  settings.value = await response.json()
} else if (response.status === 400) {
  errors.value = await response.json()
} else {
  console.log('123')
}

onMounted(() => {
  timeUpdateInterval = setInterval(() => {
    currentDateTime.value = Date.now()
  }, 1000)

  window.addEventListener('keydown', async (e) => {
    if (e.key == 'S') {
      await reloadSettings()
    }
  });
})

onUnmounted(() => {
  if (timeUpdateInterval) {
    timeUpdateInterval.clear()
  }
})

const currentDateTimeFormatted = computed(() => {
  return format(currentDateTime.value, settings.value.header.date_format)
})

async function reloadSettings() {
  const response = await fetch("/api/settings", {
    method: "POST"
  })
  console.info('Clarity settings reloaded!')

  if (response.ok) {
    settings.value = await response.json()
    errors.value = null
  } else if (response.status === 400) {
    errors.value = await response.json()
  } else {
    console.log('123')
  }
}
</script>
