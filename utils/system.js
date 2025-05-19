import Cookies from 'js-cookie'

const CookieKey = 'fox_pay_admin_system_title'

export function getSystemTitle() {
  return Cookies.get(CookieKey)
}

export function setSystemTitle(title) {
  return Cookies.set(CookieKey, title)
}

export function removeSystemTitle() {
  return Cookies.remove(CookieKey)
}
