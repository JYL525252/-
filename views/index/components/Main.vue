<template>
  <div class="wrapper">
    <div v-if="lists && lists.length > 0" class="box-msg-list">
      <el-scrollbar ref="msglist" wrap-class="scrollbar-wrapper">
        <div class="list">
          <div v-for="(item, index) in lists" class="row"
               :style="'background:' + (item.user === 'AI'? '#f7f7f8':'#fff') + ';'">
            <div v-if="item.user === 'AI'" class="message">
              <div class="avatar">
                <img src="/static/img/ai.svg">
              </div>
              <div class="text markdown-body">
                <textComponent
                  :text="item.message"
                ></textComponent>
                <div>
                  <span
                    v-clipboard:copy='textFormat(item.message)'
                    v-clipboard:success="onCopySuccess"
                    v-clipboard:error="onCopyError"
                    class="copy text-primary"
                  >复制内容</span>
                </div>
              </div>
            </div>
            <div v-else class="message">
              <div class="avatar" style="background: #ffffff;">
                <img :src="avatar || '/static/img/avatar.png'">
              </div>
              <!--              <div class="text" v-html="item.message" />-->
              <div class="text markdown-body">
                <textComponent
                  :text="item.message"
                ></textComponent>
              </div>
            </div>
          </div>
          <div v-if="writing" style="background: #f7f7f8;">
            <div class="message">
              <div class="avatar"><img src="/static/img/ai.svg"></div>
              <div class="text markdown-body">
                <!--                  <span v-html="writingText"></span>-->
                <textComponent
                  :text="writingText"
                ></textComponent>
                <span class="cursor"/>
              </div>
            </div>
          </div>
        </div>
      </el-scrollbar>
    </div>

    <welcome
      v-else
      :page-title="page_title"
      @use="quickMessage"
    ></welcome>

    <div class="box-input">
      <div class="input">
        <el-input
          v-model="message"
          placeholder="输入你的问题（Shift + Enter = 换行）"
          @keyup.enter.native="onEnter"
          type="textarea"
          :autosize="{ minRows: 1, maxRows: 8}"
          maxlength="3000"
        />
        <el-button
          class="btn-send"
          type="default"
          :loading="writing"
          icon="el-icon-position"
          @click="sendText"
        />
      </div>
      <div class="copyright">
        <div v-if="copyright">
          <a v-if="copyright_link" :href="copyright_link" target="_blank">{{ copyright }}</a>
          <span v-else>{{ copyright }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from "vuex";
import {getHistoryMsg, saveAIMessage} from "@/api/chat";
import {getToken, getSiteCode} from "@/utils/auth";
import TextComponent from "./Text";
import Welcome from "./Welcome";
import {saveGroup} from '@/api/group'

import "katex/dist/katex.min.css";
import "@/styles/lib/tailwind.css";
import "@/styles/lib/highlight.scss";
import "@/styles/lib/github-markdown.scss";

export default {
  name: "Main",
  components: {TextComponent, Welcome},
  data() {
    return {
      group_id: 0,
      lists: [],
      message: "",
      writingText: "",
      writing: false,
      page: 1,
      pagesize: 1000,
    };
  },
  computed: {
    ...mapGetters([
      "avatar",
      "nickname",
      "page_title",
      "copyright",
      "copyright_link",
    ]),
  },
  methods: {
    async sendText() {
      if (this.writing) {
        return;
      }

      if (this.group_id === 0) {
        await this.createGroup();
        if (this.group_id === 0) {
          return;
        }
        if (this.group_id === -1) {
          this.group_id = 0
          this.$message.error('创建会话出错，请登录。');
          return;
        }
      }

      const message = this.trim(this.message);
      if (!message) {
        this.$message.error("请输入你的问题");
        this.message = "";
        return;
      }
      this.lists.push({
        user: "我",
        message: message,
      });
      this.message = "";
      this.writing = true;
      this.scrollBottom();

      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      headers.append("X-token", getToken());
      const url = process.env.VUE_APP_BASE_API + "/chat/sendText";
      const data = {
        group_id: this.group_id,
        message: message,
      };
      const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        this.writing = false;
        this.$message.error(response.statusText);
        return;
      }
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let curAiMsg = "";
      while (!done) {
        this.scrollBottom();
        const {value, done: readerDone} = await reader.read();
        if (value) {
          let char = decoder.decode(value);
          if (char === "\n" && curAiMsg.endsWith("\n")) {
            continue;
          }
          if (char) {
            if (char.indexOf("[error]") !== -1) {
              this.writing = false;
              this.writingText = "";
              this.lists.pop();
              const error = char.replace("[error]", "");
              if (error.indexOf("请登录") !== -1) {
                this.$emit("showlogin");
                setTimeout(() => {
                  this.$message.error(error);
                }, 500);
              } else if (error.indexOf("请充值") !== -1) {
                this.$emit("showUserInfo");
                setTimeout(() => {
                  this.$message.error(error);
                }, 500);
              } else {
                this.$alert(error, "系统提示");
              }
              break;
            }
            // char = char.replaceAll("\n", "<br>");
            this.writing = true;
            this.writingText += char;
          }
        }
        done = readerDone;
      }
      if (this.writingText) {
        this.lists.push({
          user: "AI",
          message: this.writingText,
        });

        saveAIMessage({
          group_id: this.group_id,
          message: this.writingText
        })
      }

      this.writing = false;
      this.writingText = "";
      this.scrollBottom();
    },
    async createGroup() {
      try {
        const res = await saveGroup({title: '新的会话'});
        if (!res.errno) {
          this.group_id = res.group_id;
          this.$emit('groupCreated');
        } else {
          this.$message.error(res.message || '创建会话失败');
        }
      } catch (error) {
        console.error('创建会话出错:', error);
        if (error.errno === 403) {
          this.group_id = -1;
          this.$emit("showlogin");
        } else {
          this.$message.error('创建会话出错，请稍后再试');
        }
      }
    },
    setGroupId(group_id) {
      this.group_id = group_id;
      this.page = 1;
      this.getHistoryMsg();
    },
    getHistoryMsg() {
      getHistoryMsg({
        group_id: this.group_id,
        page: this.page,
        pagesize: this.pagesize,
      }).then((res) => {
        this.lists = res.data.list;
        this.$nextTick(() => {
          this.scrollBottom();
        });
      });
    },
    quickMessage(text) {
      this.message = text;
    },
    onCopySuccess() {
      this.$message.success("已复制");
    },
    onCopyError() {
      this.$message.error("复制失败");
    },
    onEnter(e) {
      if (!e.shiftKey) {
        this.sendText();
      }
    },
    trim(str) {
      if (str) {
        str = str.replace(/(^\s*)|(\s*$)/g, "");
      }
      return str;
    },
    textFormat(str) {
      str = this.trim(str);
      if (str && typeof str.replaceAll == "function") {
        str = str.replaceAll("<br>", "\n").replaceAll("&nbsp", " ");
      }
      return str;
    },
    scrollBottom() {
      this.$nextTick(() => {
        const container = this.$refs["msglist"].wrap;
        container.scrollTop = container.scrollHeight;
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.app-main {
  /*50 = navbar  */
  min-height: calc(100vh - 50px);
  /*min-height: 100vh;*/
  width: 100%;
  position: relative;
  overflow: hidden;
  background: #f3f6f9;
}

.fixed-header + .app-main {
  padding-top: 50px;
}

.wrapper {
  display: flex;
  flex-direction: column;
}

.box-msg-list {
  width: 100%;
  position: absolute;
  top: 50px;
  bottom: 140px;
  left: 0;
  right: 0;
  box-sizing: border-box;

  .el-scrollbar {
    height: 100%;
    overflow-x: hidden;
  }
}

.list {
  width: 100%;
  height: auto;

  .row {
    width: 100%;
    border-bottom: 1px solid #ddd;
  }
}

.message {
  width: 90%;
  margin: 0 auto;
  display: flex;
  justify-content: flex-start;
  padding: 20px 20px;
  box-sizing: border-box;
  max-width: 100%;

  &:last-child {
    border-bottom: 0;
  }

  .text {
    color: #343541;
    line-height: 26px;
    font-size: 16px;
    word-break: break-all;
    padding: 4px 0;
    overflow: hidden;
    width: 100%;
    box-sizing: border-box;
    display: inline;

    span {
      display: inline;
    }
  }

  .copy {
    width: 80px;
    height: 36px;
    cursor: pointer;
    font-size: 14px;
  }

  .avatar {
    width: 30px;
    height: 30px;
    min-width: 30px;
    background: #F7F7F8;
    color: #fff;
    font-size: 14px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 3px;
    margin-right: 20px;
    overflow: hidden;

    img {
      width: 30px;
      height: 30px;
    }
  }

  .cursor {
    background: #3d3d3d;
    line-height: 100%;
    border-left: 0.1em solid transparent;
    animation: cursor 0.6s infinite;
    display: inline-block;
    width: 5px;
    height: 20px;
    margin-top: 3px;
  }

  /* Animation */
  @keyframes cursor {
    50% {
      background: white;
    }
  }
}

.box-input {
  width: 100%;
  background: #fff;
  position: fixed;
  bottom: 0;
  left: 0;
  padding: 2vh 0 0 22vh;
  box-sizing: border-box;
  transition: padding-left 0.28s;

  .input {
    width: 768px;
    margin: 0 auto;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    position: relative;
    max-width: 100%;

    .btn-send {
      position: absolute;
      right: 1px;
      bottom: 1px;
      border: none;
      height: 40px;
    }
  }

  .copyright {
    width: 768px;
    margin: 15px auto 20px auto;
    font-size: 13px;
    color: #999;
    text-align: center;
    letter-spacing: 1px;
    max-width: 100%;
    line-height: 18px;
  }
}

.mobile {
  width: 100% !important;

  .box-input {
    max-width: 100%;
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>

<style lang="scss">
.scrollbar-wrapper {
  height: 100%;
  overflow-x: hidden;
}

// fix css style bug in open el-dialog
.el-popup-parent--hidden {
  .fixed-header {
    padding-right: 15px;
  }
}

.input .el-textarea__inner {
  padding: 10px 60px 10px 15px;
  letter-spacing: 1px;
}
</style>

<style lang="scss">
.markdown-body {
  display: block;
  width: 100%;
  background-color: transparent;
  font-size: 14px;
  box-sizing: border-box;

  p {
    white-space: pre-wrap;
  }

  ol {
    list-style-type: decimal;
  }

  ul {
    list-style-type: disc;
  }

  pre code,
  pre tt {
    line-height: 1.6;
    font-size: 16px;
  }

  .highlight pre,
  pre {
    //background-color: #fff;
    background-color: #edeff2;
    margin-top: 16px;
  }

  code.hljs {
    padding: 0;
  }

  .code-block {
    &-wrapper {
      position: relative;
      padding-top: 24px;
    }

    &-header {
      position: absolute;
      top: 5px;
      right: 0;
      width: 100%;
      padding: 0 1rem;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      color: #b3b3b3;

      &__copy {
        cursor: pointer;
        margin-left: 0.5rem;
        user-select: none;

        &:hover {
          color: #65a665;
        }
      }
    }
  }

  .code-block-wrapper {
    display: block;
    width: 100%;
  }
}

html.dark {
  .message-reply {
    .whitespace-pre-wrap {
      white-space: pre-wrap;
      color: var(--n-text-color);
    }
  }

  .highlight pre,
  pre {
    background-color: #282c34;
  }
}
</style>
