import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import matplotlib.pyplot as plt
import numpy as np
import requests
import bs4
import re

def ocr(filePath):
  image = cv2.imread(filePath)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  image = cv2.threshold(image, 0, 1255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
  text = pytesseract.image_to_string(image)

  import re
  data = {}

  if(re.search('[A-Z][A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][A-Z]', text)):
      data['Type'] = "PAN"

      data['PANID'] = re.findall('[A-Z][A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][A-Z]', text)[0]
      
      if(re.search('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', text)):
          data['DOB'] = re.findall('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', text)[0]
      
      text = text.split("\n")[1:]
      names = ["", "", ""]

      it = 0
      for line in text:
          if(line == '\n'):
              continue
          elif(it > 2):
              break
          elif (
              ("GOVT." in line)
              or ("GOVERNMENT" in line)
              or ("TAX" in line)
              or ("OVERNMENT" in line)
          ):
              continue
          elif re.search("[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]", line):
              break
          else:
              x = ""
              for i in line.split():
                  x = x + " " + i
                  url = "https://google.com/search?q=" + '+'.join(x.split())
                  request_result = requests.get(url)
                  soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                  heading_object = soup.find_all("h3")
                  info = []
                  for infos in heading_object:
                      infos = ''.join(x for x in infos.getText() if x.isalpha() or x == ' ').lower()
                      info.append(infos)
                  for infos in info:
                      if x.lower() in infos:
                          names[it] = x

          it = it + 1

      newNames = []
      for i in names:
          if(i!=''):
              newNames.append(i)
          
      if(newNames[0]):
          data['Name'] = newNames[0]
          
      if(newNames[1]):
          data['FatherName'] = newNames[1]

          
  elif(re.search('[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9]', text)):
      data['Type'] = 'Aadhar'
      
      data['Aadhar'] = re.findall('[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9]', text)[0]
      
      if(re.search('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', text)):
          data['DOB'] = re.findall('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', text)[0]
          
      if(re.search('Male', text)):
          data['Gender'] = re.findall('Male', text)[0]
      
      if(re.search('Female', text)):
          data['Gender'] = re.findall('Female', text)[0]
      
      text = text.split("\n")[1:]
      names = ["", "", ""]

      it = 0
      for line in text:
          if(line == '\n'):
              continue
          elif(it > 2):
              break
          elif (
              ("GOVT." in line)
              or ("GOVERNMENT" in line)
              or ("TAX" in line)
              or ("OVERNMENT" in line)
              or ("INDIA" in line)
              or ("NDIA" in line)
          ):
              continue
          elif re.search("[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]", line):
              break
          else:
              x = ""
              for i in line.split():
                  x = x + " " + i
                  url = "https://google.com/search?q=" + '+'.join(x.split())
                  request_result = requests.get(url)
                  soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                  heading_object = soup.find_all("h3")
                  info = []
                  for infos in heading_object:
                      infos = ''.join(x for x in infos.getText() if x.isalpha() or x == ' ').lower()
                      info.append(infos)
                  for infos in info:
                      if x.strip().lower() in infos:
                          names[it] = x

          it = it + 1
      newNames = []
      for i in names:
          if(i!=''):
              newNames.append(i)
          
      if(newNames[0]):
          data['Name'] = newNames[0]
          

  elif(re.search('[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', text)):
      data['Type'] = "Passport"
      
      data['PassportNumber'] = re.findall('[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', text)[0]
      
      dates = re.findall('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', text)

      
      if(len(dates) == 3):
          data['DOB'], data['IssueDate'], data['ExpiryDate'] = dates[0], dates[1], dates[2]
      elif(len(dates) == 2):
          data['DOB'] = dates[0]
          if(int(dates[1].split('/')[2]) <= 2010):
              data['IssueDate'] = dates[1]
          else:
              data['ExpiryDate'] = dates[1]
      elif(len(dates) == 1):
          if(int(dates[0].split('/')[2]) >= 2020):
              data['ExpiryDate'] = dates[0]
          else:
              data['DOB'] = dates[0]
      
      if(re.search('INDIAN', text)):
          data['Nationality'] = "Indian"
          if(re.search('INDIAN F', text)):
              data['Gender'] = "F"
          elif(re.search('INDIAN M', text)):
              data['Gender'] = "M"

      text = text.split("\n")[1:]
      name = ""
      newText = []
      for line in text:
          if(line.strip()!=''):
              newText.append(line)
      text = newText
      lenText = len(text)
      for i in range(lenText):
          line = text[i]
          it = 0
          searchCompleted = False
          if(re.search('[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', line)):
              for li in range(i + 1, len(text)):
                  x = text[li]
                  url = "https://google.com/search?q=" + '+'.join(x.split())
                  request_result = requests.get(url)
                  soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                  heading_object = soup.find_all("h3")
                  info = []
                  if(re.findall('[0-3][0-9]/[0-1][0-9]/[0-2][0-9][0-9][0-9]', x)):
                      break
                  for infos in heading_object:
                      infos = ''.join(x for x in infos.getText() if x.isalpha() or x == ' ').lower()
                      info.append(infos)
                  for infos in info:
                      if x.lower() in infos:
                          name = x + " " + name
                          it = it + 1
                          break
                  if(it == 2):
                      searchCompleted = True
                      break
          
          if(searchCompleted):
              break
                  
                              
      if(name.strip()!= ''):
          data['Name'] = name
          
  return (data)