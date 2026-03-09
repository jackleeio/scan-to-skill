# Scan to Skill

Scan to Skill 支持「扫码即安装」：识别二维码中的 ClawHub 链接或 skill slug，自动调用 `clawhub install` 安装技能。

## 核心能力

- 从图片/截图识别二维码
- 解析 payload（URL / slug / 安装命令）
- 自动安装 skill
- 返回安装结果与下一步提示

## 目录结构

- `SKILL.md`：扫码安装流程说明
- `scripts/install_from_qr.py`：二维码识别与安装脚本
- `references/slug-parsing.md`：slug 解析规则

## 打包文件

- `../dist/scan-to-skill.skill`

## 快速使用

```bash
# 仅识别
python3 scripts/install_from_qr.py --decode-only <image_path>

# 识别并安装
python3 scripts/install_from_qr.py <image_path>
```

## 依赖说明

脚本优先使用 OpenCV 解码二维码；若不可用，回退尝试 `zbarimg`。
