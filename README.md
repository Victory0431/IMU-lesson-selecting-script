# IMU-lesson-selecting-script
内蒙古大学教务选课脚本Designed for IMUer to select favourite and popular class when doing it in human is hard.
内蒙古大学教务选课脚本
cookie.py 需要先行在浏览器登录，然后复制cookie至脚本内登录。
会一直查看选课系统是否打开，打开则立刻选列表内的课程（需要先填入课程代码）。

#手动登录版
支持程序内手动登录，验证码没有进行自动识别，百度API不太好用，成功率不高。
学号和密码可以提前写入脚本中，只需要输入验证码即可。
cookie自始至终使用同一个cookie即可，登录仅仅是验证cookie，而不会改变它。
（cookie可用时长网页源代码的注释中写有两周）但是没有试验过，不知道多久会过期。
