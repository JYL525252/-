import request from '@/utils/request'

export function getGroupList(data) {
  return request({
    url: '/group/getGroupList',
    method: 'post',
    data
  })
}
export function getGroup(data) {
  return request({
    url: '/group/getGroup',
    method: 'post',
    data
  })
}

export function saveGroup(data) {
  return request({
    url: '/group/saveGroup',
    method: 'post',
    data
  })
}

export function delGroup(data) {
  return request({
    url: '/group/delGroup',
    method: 'post',
    data
  })
}
