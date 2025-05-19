import Cookies from 'js-cookie'

const TokenKey = 'gpt_pc_token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

const SiteCodeKey = 'gpt_pc_sitecode'
export function getSiteCode() {
  return Cookies.get(SiteCodeKey)
}

export function setSiteCode(sitecode) {
  return Cookies.set(SiteCodeKey, sitecode)
}

export function removeSiteCode() {
  return Cookies.remove(SiteCodeKey)
}
