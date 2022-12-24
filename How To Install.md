## 前端 - How To Install

1. 克隆本仓库

   ```bash
   git clone https://github.com/Xenorian/mirror_v2.git
   ```

2. 进入前端文件夹`mirrir_v2`

   ```bash
   cd mirrir_v2
   ```

3. 安装所需依赖

   ```bash
   npm install
   ```

4. 进入`src/stores`，修改`repoData.ts`，将后端ip与端口写入m_rooturl中

5. 开始运行

   ```bash
   npm run dev
   ```
   
## 后端
首先创建虚拟环境：

```shell

Conda create --name {项目名称} python=3.7
```

 

启用虚拟环境：

```
Conda activate {项目名称}
```

 

安装依赖：

```
Pip install -r requirements.txt
```

 

创建数据库相关命令：

```
Python manage.py makemigrations
```

 

```
Python manage.py migrate
```



运行：

```
python manage.py runserver
```

