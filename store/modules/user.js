import { login, logout, getInfo, getSystemInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    user_id: 0,
    avatar: '',
    nickname: '',
    logo: '',
    logo_mini: '',
    page_title: '',
    copyright: '',
    copyright_link: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USER_ID: (state, user_id) => {
    state.user_id = user_id
  },
  SET_NICKNAME: (state, nickname) => {
    state.nickname = nickname
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_LOGO: (state, logo) => {
    state.logo = logo
  },
  SET_LOGO_MINI: (state, logo_mini) => {
    state.logo_mini = logo_mini
  },
  SET_PAGE_TITLE: (state, page_title) => {
    state.page_title = page_title
  },
  SET_COPYRIGHT: (state, copyright) => {
    state.copyright = copyright
  },
  SET_COPYRIGHT_LINK: (state, copyright_link) => {
    state.copyright_link = copyright_link
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        if (response.errno === 0) {
          const { data } = response
          commit('SET_TOKEN', data.token)
          setToken(data.token)
        }
        resolve(response)
      }).catch(error => {
        console.log('error', error)
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const { data } = response

        if (!data) {
          return reject('登录过期，请重新登录')
        }

        const { user_id, nickname, avatar, vip_expire_time, balance } = data

        commit('SET_USER_ID', user_id)
        commit('SET_NICKNAME', nickname)
        commit('SET_AVATAR', avatar)
        commit('SET_VIP_EXPIRE_TIME', vip_expire_time)
        commit('SET_BALANCE', balance)

        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getSystemInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getSystemInfo().then(response => {

        const { data } = response

        if (!data) {
          return reject('登录过期，请重新登录')
        }

        const { logo, logo_mini, page_title, copyright, copyright_link } = data

        commit('SET_LOGO', logo)
        commit('SET_LOGO_MINI', logo)
        commit('SET_PAGE_TITLE', page_title)
        commit('SET_COPYRIGHT', copyright)
        commit('SET_COPYRIGHT_LINK', copyright_link)

        if(page_title) {
          document.title = page_title
        }

        resolve(data)
      }).catch(error => {
        if(error.errno === 403) {
          window.location.href = '/web/404'
          return
        }

        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

