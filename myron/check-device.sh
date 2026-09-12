#!/system/bin/sh
# 在 Android 正常启动环境验证；recovery 的内核不能证明原系统的 KMI。
[ "$BOOTMODE" = true ] || abort "请在正常启动的 Android 中安装，无法使用 recovery 内核验证目标 KMI。"
[ "$(getprop ro.product.device)" = myron ] || abort "仅支持 myron。"
case "$(uname -r)" in
  6.12.69-android16-6-*) ;;
  *) abort "需要 6.12.69-android16-6 内核。" ;;
esac
pages="$(getconf PAGESIZE 2>/dev/null)"
[ "$pages" = 4096 ] || abort "无法确认当前内核为 4K 页面。"
