# 夜市官网开发踩坑日志

> 记录开发过程中遇到的坑、原因分析和解决方案，供后续参考。

## 1. 后端 views.py: serializer 赋值成元组

**现象**：join_view 中多行变量赋值意外创建了元组。
**原因**：Python 允许隐式元组，换行符被当作分隔符。
**解决**：改成一行赋值：`serializer = JoinApplicationSerializer(data=request.data)`。

## 2. 后端 views.py: Product 模型未导入

**现象**：`except Product.DoesNotExist` 报 NameError。
**原因**：`from .models import ...` 中没有 Product。
**教训**：添加新视图时确认所需模型已导入。

## 3. PowerShell 管道中文路径乱码

**现象**：`@'...'@ | python` 时路径中的中文变成 `???????`。
**原因**：PowerShell 管道默认编码非 UTF-8，中文在传递过程中被破坏。
**解决**：用 `Set-Content` 写脚本到 TEMP 目录（全 ASCII 路径），再执行。
**教训**：PowerShell + Python + 中文路径的三重打击，优先"写文件再执行"模式。

## 4. Start-Process 启动 npm 报错

**现象**：`Start-Process -FilePath npm -RedirectStandardOutput` 报错 "%1 不是有效的 Win32 应用程序"。
**原因**：npm 是 npm.cmd 批处理脚本，不是 PE 文件，不能重定向 IO。
**解决**：去掉输出重定向，只保留 `-WindowStyle Hidden`。

## 5. Start-Process 参数冲突

**现象**：-NoNewWindow 和 -WindowStyle Hidden 同时指定时报错。
**原因**：两个参数互斥。
**解决**：只用 `-WindowStyle Hidden`。

## 6. Vue 3: script 与 script setup 变量作用域

**现象**：JoinUsPage 在第二份普通 `<script>` 块中定义的 `SendIcon` 在模板中报未定义。
**原因**：`<script setup>` 不暴露普通 `<script>` 块的顶层绑定给模板。
**解决**：移入 `<script setup>`，直接 `<Send :size="18" />`。

## 7. HTML 锚链接 vs Vue Router

**现象**：HeroBanner 和 FooterBar 用 `href="#xxx"` 锚链接，点击不跳转页面。
**原因**：Vue Router history 模式下 `#xxx` 只寻找 DOM 锚点，不触发路由。
**解决**：改用 `<router-link to="...">` 或 `router.push()`。

## 8. apply_patch 工具中文路径问题

**现象**：apply_patch 无法匹配含中文的路径或文件内容。
**解决**：改用 Set-Content + Python 脚本。

## 9. 终端 GBK 编码 vs UTF-8 数据

**现象**：PowerShell 打印中文显示乱码。
**解决**：用浏览器渲染验证，不在终端看中文。

## 10. MySQL 配置与文档不一致

**现象**：文档写 SQLite，实际 settings.py 配 MySQL。
**教训**：文档必须随代码同步更新。

## 11. API 端点路径冲突

**现象**：前端的 `axios.post('/api/reviews/submit/')` 请求被 Vite 代理到 Django 时报 404。
**原因**：Django 的 `ReviewViewSet` 中 `@action(detail=False, methods=['post'])` 生成的 URL 是 `/api/reviews/submit/`，但 DRF 默认末尾无斜杠。
**注意**：已在 `market/urls.py` 确认该路由存在且工作正常。

## 12. Set-Content 的 -Value $input 陷阱

**现象**：`@'...'@ | Set-Content -Path file -Value $input` 写入 `System.Management.Automation.Runspaces.PipelineReader...` 而不是实际内容。
**原因**：`$input` 在管道接收器中是枚举器对象，转换为字符串时得到类型名而非内容。
**解决**：直接用管道传参：`@'...'@ | Set-Content -Path file -Encoding UTF8`。

## 核心模式总结

在处理含中文路径的项目时：
- 用 `Set-Content` 写 Python 脚本到 `$env:TEMP` -> 再 `python temp_script.py` 执行
- 短命令可直接 `python -c "..."` 但避免传中文路径
- 避免 `@'...'@ | python` 管道传中文
- 避免 apply_patch 改中文内容

*最后更新: 2026-07-14*
