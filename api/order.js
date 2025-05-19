import request from '@/utils/request'

export function getGoodsList(data) {
  return request({
    url: '/order/getGoodsList',
    method: 'post',
    data
  })
}
export function getVipList(data) {
  return request({
    url: '/order/getVipList',
    method: 'post',
    data
  })
}
export function createOrder(data) {
  return request({
    url: '/order/createOrder',
    method: 'post',
    data
  })
}
export function checkPay(data) {
  return request({
    url: '/order/checkPay',
    method: 'post',
    data,
    hideLoading: true
  })
}
