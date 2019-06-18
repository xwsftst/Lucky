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
Library	SeleniumLibrary

Resource	resource.txt

Suite Setup  SeleniumLibrary.Set Screenshot Directory	E:/WorkSpace/Lucky/logs/1/8/images

Suite Teardown  SeleniumLibrary.Close All Browsers

*** Test Cases ***

7-9 初始化套件.初始化用例
	SeleniumLibrary.Open Browser	${URL}	${BROWSER}		
	SeleniumLibrary.Maximize Browser Window				


8-11 百度搜素测试套件.百度搜索用例
	SeleniumLibrary.Input Text	${input_kw}	${search_word}		
	SeleniumLibrary.Capture Page Screenshot				
	BuiltIn.Sleep	3			
	SeleniumLibrary.Click Button	${search_btn}			
	BuiltIn.Sleep	5			
8-12 百度搜素测试套件.百度搜索断言用例
	${title}	SeleniumLibrary.Get Title			
	BuiltIn.Should Be Equal	${title}	${search_result_title}		


9-13 清理套件.清理用例
	SeleniumLibrary.Close Browser				


