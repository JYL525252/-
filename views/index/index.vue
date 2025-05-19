<template>
  <div :class="classObj" class="app-wrapper">
    <div v-if="device === 'mobile'&&sidebar.opened" class="drawer-bg" @click="handleClickOutside"/>

    <sidebar class="sidebar-container" @showlogin="showLogin" @changeGroupId="changeGroupId"/>

    <div :class="{'fixed-header':fixedHeader, 'mobile': device === 'mobile'}">
      <navbar @showUserInfo="showUserInfo" @showlogin="showLogin"/>
    </div>
    <div class="main-container" :class="{'mobile': device === 'mobile'}">
      <Main ref="main" @showlogin="showLogin" @showUserInfo="showUserInfo" @groupCreated="handleGroupCreated"/>
    </div>
    <login :visible="loginVisibleComputed" @close="closeLogin" ref="login"/>
    <userinfo v-if="userinfoShow" @close="closeUserInfo" @showlogin="showLogin"></userinfo>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import {setSiteCode} from '@/utils/auth'
import {Login, Main, Navbar, Sidebar, Userinfo} from './components'
import ResizeMixin from './mixin/ResizeHandler'

export default {
  name: 'Index',
  components: {Navbar, Sidebar, Login, Main, Userinfo},
  mixins: [ResizeMixin],
  data() {
    return {
      loginVisible: false,
      groupid: 0,
      userinfoShow: false,
    }
  },
  computed: {
    ...mapGetters([
      'page_title',
      'copyright'
    ]),
    loginVisibleComputed() {
      return this.loginVisible;
    },
    sidebar() {
      return this.$store.state.app.sidebar
    },
    device() {
      return this.$store.state.app.device
    },
    fixedHeader() {
      return this.$store.state.settings.fixedHeader
    },
    classObj() {
      return {
        mobile: this.device === 'mobile' && this.sidebar.opened,
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened,
        withoutAnimation: this.sidebar.withoutAnimation
      }
    }
  },
  created() {
    const sitecode = window.location.search.substr(1, 4)
    setSiteCode(sitecode)
  },
  methods: {
    handleClickOutside() {
      this.$store.dispatch('app/closeSideBar', {withoutAnimation: false})
    },
    showLogin() {
      this.loginVisible = true;
    },
    closeLogin() {
      this.loginVisible = false;
    },
    changeGroupId(group_id) {
      this.$refs.main.setGroupId(group_id)
    },
    showUserInfo() {
      this.$store.dispatch('user/getInfo').then(res => {
        this.userinfoShow = true
      }).catch(res => {
        if (res.errno === 403) {
          this.showLogin()
        }
      })
    },
    closeUserInfo() {
      this.userinfoShow = false
    },
    handleGroupCreated() {
      this.$refs.sidebar.getGroupList(true);
    },
  }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";
@import "~@/styles/variables.scss";

.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100%;
  width: 100%;

  &.mobile.openSidebar {
    position: fixed;
    top: 0;
  }

  /*.main-container {
    padding-bottom: 40px;
  }*/
}

.drawer-bg {
  background: #000;
  opacity: 0.3;
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
}

.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - #{$sideBarWidth});
  transition: width 0.28s;
}

.mobile.fixed-header {
  width: 100% !important;
}

.fixed-copyright {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - #{$sideBarWidth});
  transition: width 0.28s;
  height: 40px;
  background-color: #fff;
  padding: 0 20px;
  line-height: 40px;
  border-top: 1px solid #eee;
}

</style>
