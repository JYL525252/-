<template>
  <div>
    <el-dialog
      custom-class="my-dialog"
      title="个人信息"
      :visible="true"
      width="340px"
      :close-on-click-modal="true"
      :before-close="closeUserInfo"
    >
      <div class="userinfo">
        <div class="user-avatar">
          <img :src="avatar || 'https://ui-avatars.com/api/?name=%E7%99%BB%E5%BD%95'" />
        </div>
        <div class="nickname">{{ nickname || '电力小助手' }}</div>
        <div v-if="user_id" class="mid">USER_ID：{{ user_id }}</div>
        <div class="logout">
          <el-button type="text" size="mini" @click="logout">退出登录</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Userinfo',
  computed: {
    ...mapGetters([
      'user_id',
      'avatar',
      'nickname',
    ])
  },
  methods: {
    closeUserInfo() {
      this.$emit('close')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.closeUserInfo()
      window.location.reload()
    }
  }
}
</script>

<style lang="scss" scoped>
  .userinfo {
    text-align: center;
    letter-spacing: 1px;
    padding-bottom: 40px;
    .user-avatar {
      img {
        width: 72px;
        height: 72px;
        border-radius: 36px;
      }
    }
    .mid {
      font-size: 12px;
      line-height: 24px;
    }
    .nickname {
      font-size: 15px;
      line-height: 32px;
    }

    .logout {
      margin-top: 10px;
    }
  }
</style>
