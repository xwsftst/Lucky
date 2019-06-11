import os
from xml.etree import ElementTree
from pyquery import PyQuery

from app.settings import USER_KEYS
#
#
# def parser(category="web"):
# 	keyword_list = []
# 	cwd = os.getcwd() + "/doc"
# 	for k in USER_KEYS[category]:
# 		path = cwd + "/%s.xml" % k
# 		tree = ElementTree.parse(path)
# 		root = tree.getroot()
# 		name = root.attrib["name"]
#
# 		children = []
# 		for kw in root.iter("kw"):
# 			# 关键字
# 			keyword = name + "." + kw.attrib["name"]
#
# 			# 关键字参数
# 			params = []
# 			for arg in kw.iter("arg"):
# 				params.append(arg.text)
#
# 			# 使用说明
# 			doc = kw.find("doc").text
#
# 			children.append({
# 				"id": keyword,
# 				"text": keyword,
# 				"attributes": {
# 					"params": params,
# 					"doc": doc
# 				}
# 			})
#
# 		keyword_list.append({
# 			"id": name,
# 			"text": name,
# 			"state": "closed",
# 			"children": children
# 		})
#
# 	return keyword_list


def parser_doc():
	keyword_doc = []
	cwd = os.getcwd() + "/doc"
	keys = os.listdir(cwd)
	for k in keys:
		path = cwd + '/%s' % k
		tree = ElementTree.parse(path)
		root = tree.getroot()
		name = root.attrib["name"]

		children = []
		for kw in root.iter("kw"):
			# 关键字参数
			params = []
			for arg in kw.iter("arg"):
				params.append(arg.text)

			k_params = " <br/> ".join(params)

			# 使用说明
			doc = ""
			text = kw.find("doc").text
			if text is not None:
				doc = text.replace("\n", "<br/>")

			children.append({
				"id": name + "." + kw.attrib["name"],
				"iconCls": "icon-blank",
				"name": kw.attrib["name"],
				"params": k_params,
				"doc": doc
			})

		keyword_doc.append({
			"id": name,
			"state": "closed",
			"name": name,
			"params": "",
			"doc": "",
			"children": children
		})

	return keyword_doc


def parser_html(category="web"):

	keyword_list = []
	cwd = os.getcwd() + "/doc"
	for k in USER_KEYS[category]:
		path = cwd + "/%s.html" % k
		doc = PyQuery(open(path, 'r', encoding='utf-8').read(), parser='html')
		title = doc('title').text()
		items = doc('.kw-row').items()
		children = []
		for item in items:
			keyword = item('td:first-child').text()
			keyword = "%s.%s" % (title, keyword)
			# 关键字参数
			params = []
			for arg in item('td:nth-child(2)')('span').items():
				params.append(arg.text())

			# 使用说明
			# doc = item.find("doc").text

			children.append({
				"id": keyword,
				"text": keyword,
				"attributes": {
					"params": params,
					# "doc": doc
				}
			})

		keyword_list.append({
			"id": title,
			"text": title,
			"state": "closed",
			"children": children
		})

	return keyword_list
