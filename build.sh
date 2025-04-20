#!/usr/bin/env bash
# exit on error
set -o errexit

# 安装依赖
pip install -r requirements.txt

# 收集静态文件
python manage.py collectstatic --no-input

# 执行数据库迁移
python manage.py migrate

# 创建超级用户（如果需要）
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell