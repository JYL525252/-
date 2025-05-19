import request from '@/utils/request'

export function uploadImage(data) {
  return request({
    url: '/upload/image',
    method: 'post',
    data
  })
}

export function uploadPem(data) {
  return request({
    url: '/upload/pem',
    method: 'post',
    data
  })
}
