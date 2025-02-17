# [1] - Import the necessary libraries
import fitz
import pandas as pd



# [2] - Read the file
pdf = 'document.pdf'
pdf_document = fitz.open(pdf)

full_text = ""

for page_number in range(len(pdf_document)):

	page = pdf_document.load_page(page_number)
	text = page.get_text()
	full_text += text


# [3] - Using the pattern, separate the text
individual_rows = full_text.split("12/31/2025") # List

print(len(individual_rows))

dataframe_contents = []

for row in individual_rows:

	attributes = row.split("\n")[1:-1]

	if "Page" in attributes[0]:

		attributes = attributes[8:]

	#print(attributes)

	
	for attribute in range(len(attributes)):

		if "@" in attributes[attribute]:
			
			# EmailAddress
			email = attributes[attribute]

			# Licenses
			licenses = "".join(attributes[attribute+1:])

			# PhoneNumber
			phone_number = attributes[attribute-1]
			
			if "-" in phone_number and phone_number[0].isdigit():
				pass
			else:
				phone_number = attributes[attribute-2]

			# Person
			phone_number_index = attributes.index(phone_number)
			person = attributes[phone_number_index-1]
			
			# CompanyName
			company_name = attributes[0]

			if attributes[1][0].isdigit() or "PO" in attributes[1]:
				address = "".join(attributes[1:attributes.index(person)])


			else:
				company_name += f" {attributes[1]}"
				address = "".join(attributes[2:attributes.index(person)])

			attribute_list = [
				company_name,
				address,
				person,
				phone_number,
				email,
				licenses
			]

			dataframe_contents.append(attribute_list)

		



# [4] Allocate into Dataframe

# Headers: CompanyName, Address, Person, PhoneNumber, EmailAddress, Licenses

headers = [
	'CompanyName',
	'Address',
	'Person',
	'PhoneNumber',
	'EmailAddress',
	'Licenses'
]

df = pd.DataFrame(dataframe_contents,columns=headers)
df.to_csv('pdf_result.csv',index=False)









