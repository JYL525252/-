<template>
  <div>
    <logo v-if="showLogo" :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <div class="group-list">
        <div class="group-item group-add" @click="editGroup(0)">
          <div class="group-title">
            <i class="icon el-icon-plus" />
            <span>创建新对话</span>
          </div>
        </div>
        <div v-for="(item, index) in groupList" class="group-item" :class="{active: item.id===activeGroupId}">
          <div class="group-title" @click="changeGroup(item.id)">
            <i class="icon el-icon-chat-dot-square" />
            <span>{{ item.title }}</span>
          </div>
          <el-dropdown trigger="click">
            <span class="el-dropdown-link">
              <i class="btn-dropdown el-icon-more" />
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native.stop="editGroup(item.id)">编辑</el-dropdown-item>
              <el-dropdown-item @click.native.stop="delGroup(item.id)" class="text-danger">删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
    </el-scrollbar>
    <group-edit v-if="group" :group="group" @close="closeGroupEdit" @submit="saveGroup" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import variables from '@/styles/variables.scss'
import { setSiteCode } from '@/utils/auth'
import { getGroupList, getGroup, saveGroup, delGroup } from '@/api/group'
import groupEdit from './groupEdit'
import Logo from './Logo'

export default {
  components: { groupEdit, Logo },
  data() {
    return {
      page: 1,
      pagesize: 20,
      groupList: [],
      activeGroupId: 0,
      msgList: [],
      group: null
    }
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    variables() {
      return variables
    },
    isCollapse() {
      return !this.sidebar.opened
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    }
  },
  mounted() {
    this.getGroupList(true)
  },
  methods: {
    changeGroup(group_id) {
      this.activeGroupId = group_id
      this.$emit('changeGroupId', group_id)
    },
    getGroupList(change = false) {
      getGroupList({ page: this.page, pagesize: this.pagesize }).then(res => {
        if (change && res.data.list.length > 0) {
          this.groupList = []
          this.changeGroup(res.data.list[0].id)
        }
        this.groupList = res.data.list
        this.groupTotal = res.data.count
      }).catch(res => {
        if (res.errno === 403) {
          this.$emit('showlogin')
        }
      })
    },
    editGroup(group_id = 0) {
      if (group_id) {
        getGroup({
          id: group_id
        }).then(res => {
          this.group = res.data
        }).catch(res => {
          if (res.errno === 403) {
            this.$emit('showlogin')
          }
        })
      } else {
        this.group = {
          title: '新的会话'
        }
      }
    },
    closeGroupEdit() {
      this.group = null
    },
    saveGroup(group) {
      saveGroup(group).then(res => {
        if (!this.group.id) {
          this.page = 1
          this.getGroupList(true)
        } else {
          for (var i in this.groupList) {
            if (this.groupList[i].id === group.id) {
              this.groupList[i].title = group.title
              break
            }
          }
        }
        this.$forceUpdate()

        this.$message({
          message: res.message,
          type: 'success',
          duration: 1500
        })
        this.closeGroupEdit()
      }).catch(res => {
        if (res.errno === 403) {
          this.$emit('showlogin')
        }
      })
    },
    delGroup(group_id) {
      this.$confirm('删除后不可恢复，确认删除吗?', '提示', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delGroup({
          id: group_id
        }).then(res => {

          for (var i in this.groupList) {
            if (this.groupList[i].id === group_id) {
              this.groupList.splice(i, 1)
              this.$forceUpdate()
              break
            }
          }

          this.getGroupList()
          this.$message({
            message: res.message,
            type: 'success',
            duration: 1500
          })
        }).catch(res => {
          if (res.errno === 403) {
            this.$emit('showlogin')
          }
        })
      })
    }

  }
}
</script>
<style lang="scss" scoped>
.sidebar-container {
  .group-list {
    padding: 10px 10px;
    .group-item {
      width: 100%;
      height: 44px;
      color: #fff;
      border-radius: 8px;
      margin-bottom: 10px;
      position: relative;

      .group-title {
        color: #fff;
        font-size: 16px;
        white-space: nowrap;
        overflow: hidden;
        display: flex;
        align-items: center;
        cursor: pointer;
        padding: 10px 15px;
        width: 100%;
        height: 100%;
        box-sizing: border-box;

        .icon {
          color: #fff;
          font-size: 18px;
          margin-right: 10px;
        }
        span{
          white-space: nowrap;
        }
      }
      .el-dropdown {
        display: none;
        position: absolute;
        right: 0;
        top: 6px;
        background: #202123;
      }
      .btn-dropdown {
        transform: rotate(90deg);
        color: #fff;
        font-size: 14px;
        display: block;
        padding: 10px;
      }
      &:hover {
        background: #333;
        .el-dropdown {
          display: block;
        }
      }
      &.active {
        background: #343541;
        .btn-dropdown {
          background: #343541;
        }
      }
      &.group-add {
        border: 1px solid #4d4d4f;
      }
    }
  }
}
.mobile {
  .group-item {
    &.active {
      .el-dropdown {
        display: block;
      }
    }
  }
}

</style>
