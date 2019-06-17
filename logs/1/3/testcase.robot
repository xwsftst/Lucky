*** Settings ***
Library	Collections
Library	DateTime
Library	Dialogs
Library	OperatingSystem
Library	Process
Library	Screenshot
Library	String
Library	Telnet
Library	XML
Library	Selenium2Library

Resource	resource.txt

Suite Setup  Screenshot.Set Screenshot Directory	E:/WorkSpace/Lucky/logs/1/3/images

Suite Teardown  Selenium2Library.Close All Browsers

*** Test Cases ***

7-9 初始化套件.初始化用例
	Selenium2Library.Open Browser	${URL}	${BROWSER}		
	Selenium2Library.Maximize Browser Window				


8-11 百度搜素测试套件.百度搜索用例
	Selenium2Library.Input Text	${input_kw}	${search_word}		
	BuiltIn.Sleep	5			
	Screenshot.Take Screenshot				
	Selenium2Library.Click Button	${search_btn}			
	BuiltIn.Sleep	5			
8-12 百度搜素测试套件.百度搜索断言用例
	BuiltIn.Should Be Equal	${title}	${search_result_title}		


9-13 清理套件.清理用例
	Selenium2Library.Close All Browsers				


