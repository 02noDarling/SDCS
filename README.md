# SDCS 安装与测试指南

本项目介绍了如何在本地环境中安装并运行 **SDCS**，以及如何通过测试脚本验证系统的运行状态。

---


##  一、获取 SDCS 源代码

使用 `git clone` 下载项目代码：

```bash
git clone https://github.com/02noDarling/SDCS.git
cd SDCS/
```

---

## 二、构建并启动 SDCS 服务

使用 `docker compose` 构建镜像并启动容器：

```bash
docker compose build
docker compose up -d
```

---

## 三、运行测试脚本验证系统

```bash
chmod +x sdcs-test.sh
./sdcs-test.sh 3
```

---
