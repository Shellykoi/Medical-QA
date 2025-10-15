# GitHub权限配置说明

## 问题描述

在推送代码到GitHub时遇到权限问题，主要原因是Fine-grained Personal Access Token的权限配置不正确。

## 解决方案

### 1. 正确配置Fine-grained Token权限

在创建Fine-grained Personal Access Token时，需要设置以下权限：

#### Repository permissions（仓库权限）：
- ✅ **Contents**: Read and write
- ✅ **Metadata**: Read
- ✅ **Pull requests**: Read and write
- ✅ **Issues**: Read and write

#### Account permissions（账户权限）：
- 保持为 "No account permissions added yet"

### 2. 配置步骤

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (fine-grained)"
3. 填写基本信息：
   - **Token name**: `Medical-QA-System`
   - **Description**: `医疗知识图谱问答系统项目`
   - **Resource owner**: 选择您的用户名
   - **Expiration**: 选择适当的过期时间
4. **Repository access**: 选择 "Only select repositories"
   - 搜索并选择 `Medical-QA-System` 仓库
5. **Permissions**: 设置上述权限
6. 点击 "Generate token"
7. 复制生成的token（只显示一次）

### 3. 使用Token推送代码

```bash
# 配置远程仓库
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/Shellykoi/Medical-QA-System.git

# 推送代码
git push -u origin main
```

## 替代方案

如果Token配置仍有问题，可以使用以下替代方案：

### 方案1：使用GitHub网页上传
1. 访问：https://github.com/Shellykoi/Medical-QA-System
2. 点击 "uploading an existing file"
3. 拖拽项目文件到网页上
4. 添加提交信息并提交

### 方案2：使用GitHub Desktop
1. 下载 [GitHub Desktop](https://desktop.github.com/)
2. 安装并登录您的GitHub账户
3. 选择 "Add an Existing Repository from your Hard Drive"
4. 选择项目文件夹
5. 点击 "Publish repository"

### 方案3：使用Classic Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (classic)"
3. 选择权限：至少选择 `repo` 权限
4. 生成并使用classic token

## 在另一台电脑上使用项目

一旦代码推送到GitHub，您就可以在任何电脑上：

```bash
# 克隆项目
git clone https://github.com/Shellykoi/Medical-QA-System.git
cd Medical-QA-System

# 运行GUI版本
python3 medical_qa_gui.py

# 或运行命令行版本
python3 medical_qa_system.py demo
```

## 日常开发工作流

```bash
# 拉取最新更改
git pull

# 推送更改
git add .
git commit -m "描述您的更改"
git push
```

## 注意事项

1. **Token安全**：不要将token分享给他人
2. **权限最小化**：只授予必要的权限
3. **定期更新**：定期更新token以提高安全性
4. **备份代码**：定期备份重要代码

## 故障排除

### 常见错误及解决方案

1. **403 Forbidden**：检查token权限配置
2. **401 Unauthorized**：检查token是否正确
3. **Host key verification failed**：配置SSH密钥或使用HTTPS
4. **Empty reply from server**：检查网络连接

### 调试命令

```bash
# 检查远程仓库配置
git remote -v

# 检查Git配置
git config --list

# 测试连接
git ls-remote origin
```

## 联系支持

如果仍有问题，可以：
1. 查看GitHub官方文档
2. 联系GitHub支持
3. 使用GitHub Desktop作为替代方案
