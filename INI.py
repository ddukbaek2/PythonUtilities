######################################################################
# @ 임포트.
######################################################################
import os.path
import sys
import argparse


######################################################################
# @ 해당 문자열이 비어있는지 여부.
######################################################################
def IsNullOrEmpty(text : str) -> bool:
	if text == None:
		return True
	elif text == "":
		return True
	elif len(text) == 0:
		return True
	return False


######################################################################
# @ 항목.
######################################################################
class Item:
	_Name : str()
	_Value : str()

	def __init__(self):
		self._Name = ""
		self._Value = ""
		pass
	def __del__(self):
		pass


######################################################################
# @ 섹션.
######################################################################
class Section:
	_Name : str()
	_Items : list()

	def __init__(self):
		self._Name = ""
		self._Items = list()
		self._Items.clear()

	def __del__(self):
		pass

	def AddItem(self, itemName : str, itemValue : str = "") -> Item:
		item = Item()
		item._Name = itemName
		item._Value = itemValue
		self._Items.append(item)
		return item

	def InsertItem(self, itemIndex : int, itemName : str, itemValue : str = "") -> Item:
		item = Item()
		item._Name = itemName
		item._Value = itemValue
		self._Items.insert(itemIndex, item)
		return item

	def RemoveItemAt(self, itemIndex : int):
		# del self._Items[itemIndex]
		self._Items.pop(itemIndex)
	
	def RemoveItem(self, item : Item):
		self._Items.remove(item)

	def RemoveAllItems(self):
		self._Items.clear()

	def RemoveItem(self, itemName):
		for item in self._Items:
			if item._Name == itemName:
				self.RemoveItem(item)

	def Exists(self, item : Item) -> bool:
		return self._Items.index(item)

	def Exists(self, itemName : str) -> bool:
		for item in self._Items:
			if item._Name == itemName:
				return True
		return False

	def ExistsValue(self, itemValue : str) -> bool:
		for item in self._Items:
			if item._Value == itemValue:
				return True
		return False

	def GetItemCount(self) -> int:
		return len(self._Items)

	def GetItemAt(self, itemIndex : int) -> Item:
		return self._Items[itemIndex]

	def GetItem(self, itemName : str) -> Item:
		for item in self._Items:
			if item._Name == itemName:
				return item
		return None

	def GetItemValues(self, itemName : str) -> str:
		for item in self._Items:
			if item._Name == itemName:
				return item._Value
		return None

	def GetItemValues(self, itemName : str) -> list:
		items = list()
		for item in self._Items:
			if item._Name == itemName:
				items.append(item._Value)
		return items

	def GetItems(self, itemName : str) -> list:
		items = list()
		for item in self._Items:
			if item._Name == itemName:
				items.append(item)
		return items


######################################################################
# @ INI 객체.
######################################################################
class INI:
	_INIFilePath : str()
	_Sections : list()

	def __init__(self):
		self._INIFilePath = ""
		self._Sections = list()
		self._Sections.clear()
		pass

	def __del__(self):
		pass

	def Load(self, iniFilePath : str) -> bool:
		self._INIFilePath = iniFilePath
		self._Sections.clear()

		if not os.path.isfile(self._INIFilePath):
			return False
		#print(self._INIFilePath)
		with open(self._INIFilePath, "r", encoding = "utf8") as iniText:
			for iniTextLine in iniText.readlines():
				if iniTextLine.startswith(";"):
					continue

				iniTextLine = iniTextLine.replace("\n", "")
				iniTextLine = iniTextLine.replace("\r", "")

				startIndex = iniTextLine.find("[")
				endIndex = iniTextLine.rfind("]")

				if startIndex >= 0 and endIndex >= 0:
					self.AddSection(iniTextLine[startIndex+1:endIndex])

				elif not IsNullOrEmpty(iniTextLine):
					
					seperateIndex = iniTextLine.find("=")
					if seperateIndex < 0:
						continue
					
					item = Item()
					item._Name = iniTextLine[:seperateIndex]
					item._Value = iniTextLine[seperateIndex + 1:]
					print(f"item._Name={item._Name}")
					print(f"item._Value={item._Value}")
					self._Sections[-1]._Items.append(item)
		return True

	
	def Save(self) -> bool:
		return self.SaveAs(self._INIFilePath)

	def SaveAs(self, iniFilePath) -> bool:
		writelines = list()
		with open(iniFilePath, "w", encoding = "utf8") as iniText:
			for section in self._Sections:
				writelines.append(f"[{section._Name}]\n")
				for item in section._Items:
					writelines.append(f"{item._Name}={item._Value}\n")
				writelines.append("\n")
			iniText.writelines(writelines)
		return True

	def AddSection(self, sectionName : str) -> Section:
		section = Section()
		section._Name = sectionName
		self._Sections.append(section)
		return section

	def InsertSection(self, sectionIndex : int, sectionName : str) -> Section:
		section = Section()
		section._Name = sectionName
		self._Sections.insert(sectionIndex, section)
		return section

	def RemoveSectionAt(self, sectionIndex : int):
		# del self._Sections[sectionIndex]
		self._Sections.pop(setionIndex)
	
	def RemoveSection(self, section : Section):
		self._Sections.remove(section)

	def RemoveAllSections(self):
		self._Sections.clear()

	def Exists(self, section : Section) -> bool:
		return self._Sections.index(section)

	def Exists(self, sectionName : str) -> bool:
		for section in self._Sections:
			if section._Name == sectionName:
				return True
		return False

	def GetSectionCount(self) -> int:
		return len(self._Sections)
	
	def GetSectionAt(self, sectionIndex : int) -> Section:
		return self._Sections[sectionIndex]

	def GetSection(self, sectionName : str) -> Section:
		for section in self._Sections:
			if section._Name == sectionName:
				return section
		return None
			


######################################################################
# @ 진입점.
######################################################################
def OnMain(arguments : list):

	ini = INI()
	if not ini.Load(arguments.target_path):
		print(f"Error: arguments.target_path is invalid.")
		exit(-1)

	section = None
	item = None

	section = ini.GetSection(arguments.target_section)
	if not section:
		print(f"Error: target_section is not found.")
		exit(-1)

	if arguments.modify_section_name:
		print(f"modify Section Name : {section._Name} ==> {arguments.modify_section_name}")
		section._Name = arguments.modify_section_name

	if arguments.modify_item_name:
		item = section.GetItem(arguments.target_item)
		if not item:
			print(f"Error: target_item is not found.")
			exit(-1)
		else:
			print(f"modify Item Name : {item._Name} ==> {arguments.modify_item_name}")
			item._Name = arguments.modify_item_name

	if arguments.modify_item_value:
		item = section.GetItem(arguments.target_item)
		if not item:
			print(f"Error: target_item is not found.")
			exit(-1)
		else:
			print(f"modify Item Value : {item._Value} ==> {arguments.modify_item_value}")
			item._Value = arguments.modify_item_value			
			
	if not ini.Save():
		print(f"Error: target_path='{arguments.target_path}' save failed.")
		exit(-1)

	print(f"SUCCESSED")
	exit(0)


######################################################################
# @ 진입점.
######################################################################
if __name__ == "__main__":
	argumentParser = argparse.ArgumentParser()
	argumentParser.add_argument("-p","--target-path", type = str, required = True, help = "INI File Path", default = "")
	argumentParser.add_argument("-s", "--target-section", type = str, help = "Target Section Name", default = "")
	argumentParser.add_argument("-i", "--target-item", type = str, help = "Target Item Name", default = "")
	argumentParser.add_argument("-msn", "--modify-section-name", type = str, help = "modify section name", default = "")
	argumentParser.add_argument("-min", "--modify-item-name", type = str, help = "modify item name", default = "")
	argumentParser.add_argument("-miv", "--modify-item-value", type = str, help = "modify item value", default = "")
	arguments = argumentParser.parse_args()
	OnMain(arguments) # sys.argv