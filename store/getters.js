const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews,
  token: state => state.user.token,
  user_id: state => state.user.user_id,
  avatar: state => state.user.avatar,
  nickname: state => state.user.nickname,
  logo: state => state.user.logo,
  logo_mini: state => state.user.logo_mini,
  page_title: state => state.user.page_title,
  copyright: state => state.user.copyright,
  copyright_link: state => state.user.copyright_link,
  routes: state => state.permission.routes
}
export default getters
