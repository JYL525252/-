<template>
  <div v-if="form">
    <el-dialog
      custom-class="my-dialog"
      :title="group.id ? '编辑对话' : '创建新对话'"
      width="440px"
      :visible="true"
      :close-on-click-modal="false"
      :append-to-body="true"
      :before-close="closeForm"
    >
      <el-form ref="form" :model="form" :rules="formRules" label-width="100px" style="padding: 20px 0;">
        <el-form-item label="会话标题" prop="num">
          <el-input v-model="form.title" placeholder="自定义会话标题" size="normal" style="width: 240px;" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="default" icon="el-icon-close" size="small" @click="closeForm">取 消</el-button>
        <el-button type="primary" icon="el-icon-check" size="small" @click="doSubmit">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: {
    group: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: null,
      formRules: {
        title: [
          { required: true, message: '此项必填', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.form = this.group
  },
  methods: {
    closeForm() {
      this.$emit('close')
    },
    doSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form)
        } else {
          this.$message.error('请填写必填项')
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
  .tips {
    margin-left: 10px;
    color: #999;
  }
</style>
