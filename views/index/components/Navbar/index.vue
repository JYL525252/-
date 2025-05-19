<template>
  <div class="navbar">
    <hamburger id="hamburger-container" :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />
    <div class="right-menu">
      <div class="avatar-container" @click="showUserInfo">
        <div class="avatar-wrapper">
          <img :src="avatar || 'https://ui-avatars.com/api/?name=%E7%99%BB%E5%BD%95'" class="user-avatar">
          <div class="user-name">{{ nickname || '未登录'}}</div>
          <i class="el-icon-caret-bottom" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Hamburger from '@/components/Hamburger'
import Userinfo from '../Userinfo'
import SvgIcon from "@/components/SvgIcon/index.vue";

export default {
  components: {SvgIcon, Hamburger, Userinfo },
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar',
      'nickname',
      'device'
    ])
  },
  mounted() {
    this.getSystemInfo()
    this.getUserInfo()
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    getSystemInfo() {
      this.$store.dispatch('user/getSystemInfo')
    },
    showUserInfo() {
      this.$emit('showUserInfo')
    },
    getUserInfo() {
      this.$store.dispatch('user/getInfo').then((res) => {
        if (res.errno) {

          this.$message({
            message: res.message,
            type: 'error'
          });
        }
      }).catch((error) => {
        if (error.errno === 403) {
          this.$emit('showlogin')
          return
        }
        this.$message.error('获取用户信息失败');
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  background: #fff;
  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;
    display: flex;
    align-items: center;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        position: relative;
        display: flex;
        align-items: center;

        .user-avatar {
          cursor: pointer;
          width: 32px;
          height: 32px;
          border-radius: 4px;
        }

        .user-name {
          cursor: pointer;
          margin-left: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          font-size: 12px;
          margin-left: 10px;
        }
      }
    }
  }
}
</style>
