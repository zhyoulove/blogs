## 简介
1.基于Django5，完成博客系统的基本操作，主要功能包括：采用MVT模型进行前后端交互，前端采用bootstrap进行页面美化，后端采用django进行开发，并使用美化之后的后台管理进行维护。\n
2.项目主要功能包括：博客管理、用户管理、分类管理等\n
3.ajax请求基于jquery进行原生实现\n
4.本项目的目的主要是为了熟悉Django的开发模式\n
## 如何使用
1.auths模块里面为用户管理的相关操作。包括：用户注册、登录
2.blog模块里面为博客管理的相关操作。包括：发布博客、博客详情、博客搜索
## 特别说明
注册采用QQ邮箱的方式进行，同时基于redis进行验证码的缓存和验证等，使用的时候需修改相关的配置文件
