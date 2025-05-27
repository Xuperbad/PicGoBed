#!/bin/bash
# 图床总览更新脚本 - Linux/Mac版本

echo "正在更新图床总览..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行Python脚本
python3 "$SCRIPT_DIR/generate_overview.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 更新完成！"
else
    echo ""
    echo "❌ 更新失败，请检查Python环境"
fi
