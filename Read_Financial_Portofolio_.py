import pandas as pd

def readPortofolioData(fichier_texte):

    with open(fichier_texte, "r") as file:
        lines = file.readlines()
        #initialisation des variables
        previousPortfolio, currentPortfolio = None, None
        previousGrade, currentGrade = None, None
        products = dict()
        fillTheName = False
        fillTheISIN = False
        for line in lines:
            # on supprime les sauts de ligne inutils
            line = line.replace("\n", "")
            previousPortfolio = currentPortfolio
            previousGrade = currentGrade
            if "Portfolio" in line: #boucle qui maj le portefeuille
                words = line.split("=")
                currentPortfolio = words[-1]
                fillTheISIN, fillTheName = False, False
                products[currentPortfolio] = dict()
            if previousPortfolio != currentPortfolio :
                fillTheISIN, fillTheName = False, False
                previousGrade, currentGrade = None, None
            if "Grade" in line: #boucle qui maj le grade
                words = line.replace(" ", "").split("=")
                currentGrade = words[-1]
                products[currentPortfolio][currentGrade] = dict()
                fillTheISIN, fillTheName = False, False
            if previousGrade != currentGrade:
                fillTheISIN, fillTheName = False, False

            if ("Product class" in line) and ("Name" in line): #modif name à partir de product_class
                fillTheName, fillTheISIN = True, False
                continue

            if ("Product class" in line) and ("ISIN" in line): #modif isin à partir de porduct_class
                fillTheName, fillTheISIN = False, True
                continue

            if fillTheName and len(line):
                words = line.split(",")
                productClass = words[0]
                productName = words[-1]
                if productClass not in products[currentPortfolio][currentGrade]:
                    products[currentPortfolio][currentGrade][productClass] = dict()
                products[currentPortfolio][currentGrade][productClass]["Name"] = productName
            if fillTheISIN and len(line):
                words = line.split(",")
                productClass = words[0]
                productISIN = words[-1]
                if productClass not in products[currentPortfolio][currentGrade]:
                    products[currentPortfolio][currentGrade][productClass] = dict()
                products[currentPortfolio][currentGrade][productClass]["ISIN"] = productISIN

    ref_grade = {"1":"Equities", "2":"Bonds", "3":"Structured"} #dico qui relie les grade avec le type de produit
    rows = list()
    columnNames = ["Portfolio", "Grade", "Grade Name", "Product Class", "Product Name", "ISIN"]
    rows.append(columnNames)
    portfolio_list = []
    grade_list = []
    grade_name = []
    product_class = []
    product_name = []
    ISIN = []
    for portofolio, products in products.items():
        for grade, dataPerProductClass in products.items():
            for productClass, data in dataPerProductClass.items():
                productName = data["Name"]
                productISIN = data["ISIN"]
                #print([portofolio, grade, ref_grade[grade], productClass, productName, productISIN])
                portfolio_list.append(portofolio)
                grade_list.append(grade)
                grade_name.append(ref_grade[grade])
                product_class.append(productClass)
                product_name.append(productName)
                ISIN.append(productISIN)
    dico = {"Portfolio": portfolio_list, "Grade": grade_list, "Grade Name": grade_name, "Product Class": product_class, "Product Name": product_name, "ISIN": ISIN}
    datas = pd.DataFrame(dico)
    print(datas)

    datas.to_excel('resultat.xlsx', index=False)
    return dico

print(readPortofolioData("Portfolio.txt"))
