import request from '@/utils/request'

export function getHistoryMsg(data) {
  return request({
    url: '/chat/getHistoryMsg',
    method: 'post',
    data
  })
}

export function saveAIMessage(data) {
  return request({
    url: '/chat/saveAIMessage',
    method: 'post',
    data
  })
}
