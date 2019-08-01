# py_http_Autotester

## 1，介绍

基于python，requests，通过模拟http命令，自动进行CI-Server接口测试。需要安装python和python requests。好处是做过一次测试之后，case可以积累下来，后面修改就不需要在手动测试，直接执行case就可以了。



## 2，组织方式

framework.py是入口。

base.py和public.py是基础组件。

suits目录是case目录。

所有的case以json的形式实现。

|-autotest

|----framework.py

|----base.py

|----public.py

|----suits

|--------sample1

|------------general.json

|------------update.json

|--------sample2

|------------general.json

|--------sample3

.....

## 3，使用方法

test.py或者framework.py



## 4，case结构

{

    "name":"sample name",

    "description":"sample description",

    "ctors":[

        {

            "name":"ctor name",

            "description":"ctor description", 

            "path": "sample api path", 

            "expect":{

                "success":true

            }, 

            "body":{

              "desc": "sample api parameters 1",
              "name": "sample api parameters 2",

            },

            "teardown":{

                "description":"ctor teardown description",

                "path":"teardown api path",

                "body":{

                    "id":0,
                }

            }

        }

    ],

    "steps":[

        {

            "name":"step name",

            "description":"step description", 

            "path": "sample api path", 

            "expect":{

                "success":true

            }, 

            "body":{

              "desc": "sample api parameters 1",
              "name": "sample api parameters 2",

            },

            "teardown":{

                "description":"step teardown description",

                "path":"teardown api path",

                "body":{

                    "id":0,
                }

            }

        }

    ]

}