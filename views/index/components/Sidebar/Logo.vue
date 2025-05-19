<template>
  <div class="logo-container">
    <transition name="sidebarLogoFade">
      <router-link key="expand" class="sidebar-logo-link" to="/">
        <img v-if="logo" :src="logo" class="sidebar-logo">
        <!--<h1 class="sidebar-title">{{ title }} </h1>-->
      </router-link>
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'SidebarLogo',
  computed: {
    ...mapGetters([
      'logo',
      'logo_mini'
    ]),
    title() {
      return this.$store.state.settings.title
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.logo-container {
  position: relative;
  height: 50px;
  line-height: 50px;
  /*background: #2b2f3a;*/
  background: #fff;
  text-align: center;
  overflow: hidden;
  float: left;

  & .sidebar-logo-link {
    background-color: #202123;
    height: 100%;
    width: 100%;

    & .sidebar-logo {
      /*width: 32px;
      height: 32px;*/
      width: auto;
      height: 50px;
      vertical-align: middle;
      margin-right: 12px;
    }

    & .sidebar-title {
      display: inline-block;
      margin: 0;
      /*color: #fff;*/
      color: #2b2f3a;
      font-weight: 600;
      line-height: 50px;
      font-size: 14px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
    }
  }

  &.collapse {
    .sidebar-logo {
      margin-right: 0;
    }
  }
}
</style>
