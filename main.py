import requests
from openpyxl import Workbook
from fake_useragent import UserAgent


workbook = Workbook()
workbook_page = workbook.active
workbook_page.title = "Page 1"
workbook_page["A1"].value = "Country"
workbook_page["B1"].value = "Title"
workbook_page["C1"].value = "Price"
workbook_page["D1"].value = "Short Info"
workbook_page["E1"].value = "Operator"
workbook_page["F1"].value = "Operator Info"
workbook_page["G1"].value = "Network"
workbook_page["H1"].value = "Supported Countries"
workbook_page["I1"].value = "Additional Info"

headers = {"user-agent": UserAgent().chrome}
url_countries = "https://www.airalo.com/api/v2/countries?sort=asc"
response = requests.get(url=url_countries, headers=headers)
country_objects = response.json()
countries = list()
for country_object in country_objects:
    country = country_object["slug"]
    countries.append(country)

for country in countries:
    url = f"https://www.airalo.com/api/v2/countries/{country}"
    response = requests.get(url=url, headers=headers)
    esim_objects = response.json()["packages"]
    for esim_object in esim_objects:
        title = esim_object["title"]
        price = f'{esim_object["price"]}$'
        short_info = esim_object["short_info"]

        operator_object = esim_object["operator"]
        operator = operator_object["title"]
        additional_info = operator_object["other_info"]
        network = f'{operator_object["networks"][0]["network"]}({operator_object["networks"][0]["service_type"]})'
        operator_info = "  ||  ".join(operator_object["info"])
        operator_countries = ", ".join([operator_country['title'] for operator_country in operator_object["countries"]])
        country_name = operator_object["countries"][0]["title"]

        workbook_page[f"A{index}"].value = country_name
        workbook_page[f"B{index}"].value = title
        workbook_page[f"C{index}"].value = price
        workbook_page[f"D{index}"].value = short_info
        workbook_page[f"E{index}"].value = operator
        workbook_page[f"F{index}"].value = operator_info
        workbook_page[f"G{index}"].value = network
        workbook_page[f"H{index}"].value = operator_countries
        workbook_page[f"I{index}"].value = additional_info

workbook.save("e-sims.xlsx")
