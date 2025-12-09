#!/usr/bin/env bash
# 快速启动指南（Linux/Mac）

echo "======================================"
echo "空气质量监测系统 - 快速启动"
echo "======================================"
echo ""

# 1. 检查Python
echo "✓ 检查Python版本..."
python --version || python3 --version
echo ""

# 2. 安装依赖
echo "✓ 安装依赖..."
pip install -r requirements.txt
echo ""

# 3. 检查导入
echo "✓ 检查模块导入..."
python check_imports.py
echo ""

# 4. 显示启动说明
echo "======================================"
echo "✅ 环境配置完成！"
echo "======================================"
echo ""
echo "接下来的步骤:"
echo ""
echo "1. 复制环境文件"
echo "   cp .env.example .env"
echo ""
echo "2. 编辑.env文件，设置:"
echo "   - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
echo "   - AQICN_API_TOKEN (已设置默认值)"
echo ""
echo "3. 初始化数据库 (需要PostgreSQL运行)"
echo "   createdb air_quality_db"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/001_create_users.sql"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/002_create_cities.sql"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/003_create_air_quality_data.sql"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/004_create_health_advice.sql"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/005_create_sync_logs.sql"
echo "   psql -U postgres -d air_quality_db -f backend/db/sql/006_create_user_analytics.sql"
echo ""
echo "4. 启动开发服务器"
echo "   python run.py"
echo ""
echo "5. 在另一个终端测试API"
echo "   python test_api.py"
echo ""
echo "更多信息:"
echo "- API文档: API_DOCUMENTATION.md"
echo "- 部署指南: BACKEND_README.md"
echo "- 实现总结: IMPLEMENTATION_SUMMARY.md"
echo "- 文件清单: FILES_MANIFEST.md"
echo "- 完成报告: COMPLETION_REPORT.md"
echo ""
