<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useLangStore } from '@/stores/lang'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser, faLock } from '@fortawesome/free-solid-svg-icons'
import googleLogoUrl from '@/assets/imgs/google-logo.png'
import InfoCard from '@/components/InfoCard.vue'
import { useTokenClient } from 'vue3-google-signin'

const error = ref('')
const username = defineModel('username')
const password = defineModel('password')
const authStore = useAuthStore()
const langStore = useLangStore()

const handleOnSuccess = (response) => {
  axios
    .post('/google-profile', { access_token: response.access_token })
    .then((res) => {
      if (!res?.data) {
        error.value =
          langStore.getLang == 'cs'
            ? 'Přihlášení selhalo. Chybná odpověď serveru.'
            : 'Login failed. Server response error.'
        return
      }

      if (res.data.success) {
        error.value = ''
        console.log(res.data.user_data)
        handleGoogleLogin(res.data.user_data)
      } else {
        error.value = res.data.error
      }
    })
    .catch((err) => {
      error.value = err.response.data
      console.log(err)
    })
}

const handleOnError = (response) => {
  console.log(response)
}

const { isReady, login } = useTokenClient({
  onSuccess: handleOnSuccess,
  onError: handleOnError
})

const handleGoogleLogin = (userData) => {
  if (!userData) {
    error.value = langStore.getLang == 'cs' ? 'Přihlášení selhalo.' : 'Login failed.'
    return
  }

  if (!authStore.authAllowed(userData)) {
    error.value =
      langStore.getLang == 'cs'
        ? 'Přístup zamítnut. Chybná doména.'
        : 'Access denied. Wrong domain.'
    return
  }

  axios
    .post('/login', { user_data: userData, google: true })
    .then((res) => {
      if (!res?.data) {
        error.value =
          langStore.getLang == 'cs'
            ? 'Přihlášení selhalo. Chybná odpověď serveru.'
            : 'Login failed. Server response error.'
        return
      }

      if (res.data.success) {
        authStore.setCurrentUser({
          userId: res.data.user_id,
          username: res.data.username,
          email: res.data.email,
          firstName: res.data.first_name,
          lastName: res.data.last_name
        })
        error.value = ''
      } else {
        error.value = res.data.error
      }
    })
    .catch((err) => {
      error.value = err.response.data
      console.log(err.response.data)
    })
}

const handleExternalLogin = () => {
  if (!username.value || !password.value) {
    error.value = langStore.getLang == 'cs' ? 'Vyplňte všechna pole.' : 'Fill in all fields.'
    return
  }

  axios
    .post('/login', {
      user_data: {
        username: username.value,
        password: password.value
      },
      google: false
    })
    .then((res) => {
      if (!res?.data) {
        error.value =
          langStore.getLang == 'cs'
            ? 'Přihlášení selhalo. Chybná odpověď serveru.'
            : 'Login failed. Server response error.'
        return
      }

      if (res.data.success) {
        authStore.setCurrentUser({
          userId: res.data.user_id,
          username: res.data.username,
          email: res.data.email,
          firstName: res.data.first_name,
          lastName: res.data.last_name
        })
        error.value = ''
      } else {
        error.value = res.data.error
      }
    })
    .catch((err) => {
      error.value = err.response.data
      console.log(err.response.data)
    })
}

onMounted(() => {
  // googleOneTap({ autoLogin: true }).then((response) => {
  //   if (!response?.credential) {
  //     error.value =
  //       langStore.getLang == 'cs'
  //         ? 'Přihlášení selhalo. Chybná odpověď serveru.'
  //         : 'Login failed. Server response error.'
  //     return
  //   }
  //   const userData = decodeCredential(response.credential)
  //   handleGoogleLogin(userData)
  // })
})
</script>
<template>
  <main>
    <section class="section is-fullheight is-flex is-justify-content-center is-align-items-center">
      <div
        class="container is-flex is-flex-direction-column is-justify-content-center is-align-items-center"
      >
        <h1 class="has-text-primary">RP GEVO</h1>
        <div id="google-login-container">
          <button :disabled="!isReady" @click="login">Google Custom Login</button>
        </div>
        <div id="login-text-container" class="is-flex my-2">
          <div class="columns">
            <div class="column is-flex is-align-items-center is-hidden-mobile">
              <hr class="login-separator" />
            </div>
            <div class="column is-flex is-align-items-center">
              <p class="has-text-centered is-size-5">
                {{ langStore.getLang == 'cs' ? 'nebo' : 'or' }}
              </p>
            </div>
            <div class="column is-flex is-align-items-center is-hidden-mobile">
              <hr class="login-separator" />
            </div>
          </div>
        </div>
        <div id="login-form-container">
          <form id="login-form">
            <div class="field">
              <p class="control has-icons-left">
                <input
                  class="input"
                  type="text"
                  :placeholder="authStore.getLang == 'cs' ? 'Uživatelské jméno' : 'Username'"
                  v-model="username"
                />
                <span class="icon is-small is-left">
                  <FontAwesomeIcon :icon="faUser" />
                </span>
              </p>
            </div>
            <div class="field">
              <p class="control has-icons-left">
                <input
                  class="input"
                  type="password"
                  :placeholder="authStore.getLang == 'cs' ? 'Heslo' : 'Password'"
                  v-model="password"
                />
                <span class="icon is-small is-left">
                  <FontAwesomeIcon :icon="faLock" />
                </span>
              </p>
            </div>
            <button
              type="submit"
              class="button is-success has-text-medium"
              @click.prevent="handleExternalLogin"
            >
              {{ authStore.getLang == 'cs' ? 'Přihlásit se' : 'Login' }}
            </button>
          </form>
        </div>
        <div class="info-card-container mt-4">
          <InfoCard v-if="error !== ''" :msg="error" type="warning" />
        </div>
      </div>
    </section>
  </main>
</template>
