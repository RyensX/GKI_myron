"""为固定版本的 AnyKernel3 注入写入前检查，模板变化时直接失败。"""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
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
path.write_text(text)
