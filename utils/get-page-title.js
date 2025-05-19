import defaultSettings from '@/settings'
import { getSystemTitle } from '@/utils/system'

const systemTitle = getSystemTitle()
const title = systemTitle || defaultSettings.title || ''

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
