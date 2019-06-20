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

Suite Setup  SeleniumLibrary.Set Screenshot Directory	E:/workspace/Lucky/logs/3/1/images

Suite Teardown  SeleniumLibrary.Close All Browsers

*** Test Cases ***

2-2 初始化套件.初始化用例
	SeleniumLibrary.Open Browser	${URL}	${BROWSER}		
	SeleniumLibrary.Maximize Browser Window				


3-3 测试业务套件.测试用例
	SeleniumLibrary.Input Text	${input_kw}	${search_word}		
	BuiltIn.Sleep	2			
	SeleniumLibrary.Capture Page Screenshot				
	BuiltIn.Sleep	5			
	SeleniumLibrary.Click Element	${search_btn}			
	BuiltIn.Sleep	2			
3-4 测试业务套件.断言用例
	${title}	SeleniumLibrary.Get Title			
	BuiltIn.Should Be Equal	${title}	${search_result_title}		


4-5 清理套件.清理用例
	SeleniumLibrary.Close Browser				


