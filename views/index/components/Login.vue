<template>
  <div v-if="visible">
    <el-dialog
      custom-class="my-dialog"
      width="450px"
      :visible="true"
      :before-close="closeDialog"
      center
    >
      <div class="form-container">
        <el-form
          v-if="!isRegistering"
          ref="loginForm"
          :model="loginForm"
          :rules="loginRules"
          label-width="80px"
          class="animated-form"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleLogin('loginForm')" class="full-width-button">
              登录
            </el-button>
          </el-form-item>

          <el-form-item class="center-link">
            <el-link type="primary" @click="toggleRegisterForm">没有账号？点击注册</el-link>
          </el-form-item>
        </el-form>

        <el-form
          v-else
          ref="registerForm"
          :model="registerForm"
          :rules="registerRules"
          label-width="80px"
          class="animated-form"
        >
          <el-form-item label="昵称" prop="nickname">
            <el-input
              v-model="registerForm.nickname"
              placeholder="请输入昵称"
              prefix-icon="el-icon-edit"
            ></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
            ></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请确认密码"
              prefix-icon="el-icon-lock"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister('registerForm')" class="full-width-button">注册</el-button>
          </el-form-item>
          <el-form-item class="center-link">
            <el-link type="primary" @click="toggleRegisterForm">返回登录</el-link>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { login, register } from "@/api/user"
import { setToken } from '@/utils/auth'

export default {
  name: 'Login',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isRegistering: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      rememberMe: false,
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 30, message: '密码长度在 6 到 30 个字符', trigger: 'blur' }
        ]
      },
      registerRules: {
        nickname: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 3, max: 20, message: '昵称长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 30, message: '密码长度在 6 到 30 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.registerForm.password) {
                callback(new Error('两次输入的密码不一致!'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    closeDialog() {
      this.$emit('close')
    },
    handleLogin(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          login(this.loginForm)
            .then((res) => {
              console.log(res)
              // 假设 API 返回 { code: 200, message: '登录成功', data: { token: '...' } }
              if (res.success) {
                this.$message({
                  message: res.message || "登录成功",
                  type: "success",
                });

                // 存储 token (如果 API 返回 token)
                if (res.data && res.data.token) {
                  console.log(res.data.token)
                  setToken(res.data.token)
                }

                // 关闭对话框
                this.closeDialog();
                window.location.reload();
              } else {
                this.$message({
                  message: res.message || "登录失败",
                  type: "error",
                });
              }
            })
            .catch((error) => {
              this.$message({
                message: error.message || "登录时发生错误",
                type: "error",
              });
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    handleRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // 确保密码和确认密码匹配
          if (this.registerForm.password !== this.registerForm.confirmPassword) {
            this.$message({
              message: "密码和确认密码不匹配",
              type: "error",
            });
            return;
          }

          register(this.registerForm)
            .then((res) => {
              if (res.code === 201) {
                this.$message({
                  message: res.message || "注册成功",
                  type: "success",
                });

                // 切换回登录表单
                this.isRegistering = false;
              } else {
                this.$message({
                  message: res.message || "注册失败",
                  type: "error",
                });
              }
            })
            .catch((error) => {
              this.$message({
                message: error.message || "注册时发生错误",
                type: "error",
              });
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    handleForgotPassword() {
      // 这里实现忘记密码的逻辑，例如弹出一个重置密码的对话框
      this.$message({
        message: '忘记密码功能正在开发中...',
        type: 'info'
      });
    },
    toggleRegisterForm() {
      this.isRegistering = !this.isRegistering;
    }
  }
}
</script>

<style scoped>
.my-dialog {
  /* 自定义对话框样式 */
  border-radius: 5px;
  overflow: hidden;
}

.form-container {
  padding: 25px 25px 0 25px;
  text-align: left;
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.animated-form {
  /* 表单动画：淡入效果 */
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
  opacity: 1;
}

/* 调整 Element UI 组件的样式 */
.el-form-item {
  margin-bottom: 18px;
}

.el-input {
  width: 100%;
}

.el-input__inner {
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 10px 12px;
  font-size: 14px;
  color: #555;
}

.el-input__inner:focus {
  border-color: #409eff;
  outline: none;
}

.el-button--primary {
  color: #fff;
  border-radius: 4px;
  padding: 12px 20px;
  font-size: 16px;
}

.el-checkbox {
  text-align: left;
}

.el-link {
  font-size: 13px;
}

.el-link:hover {
  color: #409eff;
}

/* 新增样式 */
.center-link {
  display: flex;
  justify-content: center;
  align-items: center;
}

.full-width-button {
  width: 100%; /* 登录按钮占据整行 */
}

/* 移除 el-form-item 的默认 margin-bottom，让复选框、按钮和链接更紧凑 */
.el-form--label-top .el-form-item {
  margin-bottom: 12px;
}
</style>

<!--<style scoped>-->
<!--.app-main {-->
<!--  /*50 = navbar  */-->
<!--  min-height: calc(100vh - 50px);-->
<!--  /*min-height: 100vh;*/-->
<!--  width: 100%;-->
<!--  position: relative;-->
<!--  overflow: hidden;-->
<!--  background: #f3f6f9;-->
<!--}-->
<!--.fixed-header+.app-main {-->
<!--  padding-top: 50px;-->
<!--}-->
<!--</style>-->

<!--<style lang="scss">-->
<!--// fix css style bug in open el-dialog-->
<!--.el-popup-parent&#45;&#45;hidden {-->
<!--  .fixed-header {-->
<!--    padding-right: 15px;-->
<!--  }-->
<!--}-->
<!--</style>-->
