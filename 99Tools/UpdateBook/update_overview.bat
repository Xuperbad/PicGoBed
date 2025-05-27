@echo off
chcp 65001 >nul
echo 正在更新图床总览...

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0

REM 运行Python脚本
python "%SCRIPT_DIR%generate_overview.py"

if %errorlevel% equ 0 (
    echo.
    echo ✅ 更新完成！
) else (
    echo.
    echo ❌ 更新失败，请检查Python环境是否正确安装
)
pause
