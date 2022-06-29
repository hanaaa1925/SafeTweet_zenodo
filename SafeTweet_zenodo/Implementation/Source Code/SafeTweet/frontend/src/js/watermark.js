/**  水印添加方法  */
const setWatermark = (str1, str2) => {
  const id = 1
  const can = document.createElement('canvas')
  // 设置画布的长宽
  can.width = 180
  can.height = 150

  const cans = can.getContext('2d')
  cans.rotate((-20 * Math.PI) / 180) // rotate angle
  cans.font = '26px Times' // font size
  cans.fillStyle = '#797979' // font color
  cans.textAlign = 'center' // position
  cans.textBaseline = 'Middle'
  cans.fillText(str2, can.width / 4, can.height / 2)
  cans.fillText(str1, can.width / 4, can.height / 3)

  const div = document.createElement('div')
  div.id = id
  div.style.pointerEvents = 'none'
  div.style.top = '0px'
  div.style.left = '20px'
  div.style.right = '20px'
  div.style.opacity = '0.2'
  div.style.position = 'fixed'
  div.style.zIndex = '1000'
  div.style.width = document.documentElement.clientWidth + 'px'
  div.style.height = document.documentElement.clientHeight + 'px'
  div.style.background = 'url(' + can.toDataURL('image/png') + ') left top repeat'
  document.body.appendChild(div)
  return id
}

// 添加水印方法
export const setWaterMark = (str1, str2) => {
  let id = setWatermark(str1, str2)
  if (document.getElementById(id) === null) {
    id = setWatermark(str1, str2)
  }
}

// 移除水印方法
export const removeWatermark = () => {
  const id = 1
  if (document.getElementById(id) !== null) {
    document.body.removeChild(document.getElementById(id))
  }
}
