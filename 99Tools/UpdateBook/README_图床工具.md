# 图床总览自动生成工具

这个工具可以自动扫描项目中的所有图片文件，并生成markdown格式的图床总览文件。

## 功能特点

- 🔍 自动扫描所有子文件夹中的图片文件
- 📁 支持多级文件夹结构（一级用#，二级用##）
- 🖼️ 支持多种图片格式：png, jpg, jpeg, gif, webp, svg, bmp, ico
- 🔗 自动生成GitHub Raw链接
- 📝 按文件夹和文件名自动排序
- 🔄 支持增量更新

## 使用方法

### Windows用户

双击运行 `update_overview.bat` 文件，或在命令行中执行：
```cmd
update_overview.bat
```

### Linux/Mac用户

在终端中执行：
```bash
./update.sh
```

### 直接使用Python脚本

```bash
python generate_overview.py
```

## 输出格式

生成的 `图床总览.md` 文件格式如下：

```markdown
# 图床总览

# 01PixelStyle
![PixelStyle_001](https://raw.githubusercontent.com/Xuperbad/PicGoBed/master/01PixelStyle/PixelStyle_001.gif)
![PixelStyle_002](https://raw.githubusercontent.com/Xuperbad/PicGoBed/master/01PixelStyle/PixelStyle_002.gif)

# 02CartoonStyle
![CartoonStyle_001](https://raw.githubusercontent.com/Xuperbad/PicGoBed/master/02CartoonStyle/CartoonStyle_001.png)
```

## 文件说明

- `generate_overview.py` - 主要的Python脚本
- `update_overview.bat` - Windows批处理文件
- `update.sh` - Linux/Mac shell脚本
- `图床总览.md` - 生成的总览文件

## 注意事项

1. 确保已安装Python 3.x
2. 脚本会自动跳过非图片文件和隐藏文件夹
3. 每次运行都会完全重新生成总览文件
4. GitHub仓库路径已预设为：`https://raw.githubusercontent.com/Xuperbad/PicGoBed/master`

## 自定义配置

如需修改GitHub仓库路径，请编辑 `generate_overview.py` 文件中的 `GITHUB_BASE_URL` 变量。
