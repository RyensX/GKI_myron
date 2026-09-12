"""为固定版本的 AnyKernel3 注入写入前检查，模板变化时直接失败。"""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
entry = path.parent / "META-INF/com/google/android/update-binary"
entry_text = entry.read_text()
entry_anchor = "ash anykernel.sh;"
if entry_text.count(entry_anchor) != 1:
    raise SystemExit("AnyKernel3 子进程入口不符合预期")
anchor = "# boot install\nsplit_boot"
if text.count(anchor) != 1:
    raise SystemExit("AnyKernel3 安装入口不符合预期")
for old, new in [
    ("do.devicecheck=0", "do.devicecheck=1"),
    ("device.name1=", "device.name1=myron"),
]:
    if text.count(old) != 1:
        raise SystemExit("AnyKernel3 属性不符合预期: " + old)
    text = text.replace(old, new)
text = text.replace(anchor, '. "$AKHOME/check-device.sh"\n\n' + anchor)
# 变量原先仅存在于父 shell，显式传给安装子进程。
entry.write_text(entry_text.replace(entry_anchor, 'BOOTMODE="$BOOTMODE" ash anykernel.sh;'))
path.write_text(text)
