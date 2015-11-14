# 一组bottle插件

为便于使用bottle写了一组插件。最初自己用的时候是把所有功能都写在一个插件里，感觉有点笨重，不适合灵活组合，所以分拆改写成现在的样子。

## 包含

1. beaker.BeakerPlugin
1. params.ParamsPlugin
1. login.LoginPlugin

## beaker.BeakerPlugin

Beaker session插件，比bottle的官方beaker插件更便于使用——其实官方的beaker插件什么事都没做，跟直接用beaker没什么区别。

构造函数：

    BeakerPlugin(keyword="session")

参数：

1. keyword : beaker session使用的参数名，默认为session，如请求响应函数不包含此参数，则此插件被忽略，如包含此参数，则自动从请求环境中读取beaker的session对象

无可用route参数。

必须配合beaker midware使用，使用方法见beaker文档或示例程序demo.py。

## params.ParamsPlugin

参数插件，自动把请求参数转为函数调用参数，默认使用utf-8编码转为Unicode，自动根据请求方法读取query或forms，如果设置了json\_params选项，则读取json。

构造函数：

    ParamsPlugin(json_params=False, encode="utf-8")

参数：

1. json\_params : 是否使用json参数。默认为False，如果设置为True则解析 bottle.request.json 的值，以dict方式解析为对应参数。
1. encode : 指定请求编码方式。默认为utf-8。

route参数：

在请求的route中也可以使用 json\_params ，用于对特定请求使用json格式。

## login.LoginPlugin

简单的登录处理插件。如果请求需要用户登录时加上登录参数（默认为login），则会在处理请求前调用login\_func处理登录操作，成功则将结果返回给login参数。

因为处理登录操作通常需要依赖数据库和session，所以需要两个额外参数：db和session。这两个参数将会被传递给login\_func。

所以使用本插件至少需要同时安装一个数据库（或类似的如sqlalchemy）插件，和类似本插件包中的BeakerPlugin这样的session插件。

构造函数：

    LoginPlugin(login_func, keyword="login", dbkeyword="db", sessionkeyworkd="session")

参数：

1. login\_func：登录处理函数，无默认值，带两个参数：db和session用于传入数据库和session，参数值来值相应插件（所以其它插件必须先于本插件安装），返回值将被赋给login参数。
1. keyword：login参数名，默认为login。
1. dbkeyword：数据库插件的参数名，默认为db。
1. sessionkeyword：session插件的参数名，默认为session

无可用route参数

## 注意

由于python 2.x的functools.wraps不能保留函数的参数信息，所以inspect.getargspec无法取得被bottle的view装饰器装饰过的函数参数信息，导致插件不能正常工作（包括各种官方插件），故在使用插件时不得同时使用view装饰器，只能使用以下三种方法渲染模板：

1. template函数
2. apply参数
3. 内置template插件

不过由于python 3.x的inspect.signature已经解决了getargspec的不足，所以在py3中使用这里的插件可以同时使用view装饰器。

当然这是因为我已经加入相应的处理，官方的其它插件还是不能配合view装饰器的。

## 依赖

* python 2.7+ or python 3.4+（其它版本未测试）
* bottle
* beaker（BeakerPlugin需要）
* BeakerPlugin（LoginPlugin需要）
* sqlite/sqlalchemy等数据库插件（LoginPlugin需要）
