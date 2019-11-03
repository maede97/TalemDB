from person import Person
import xlsxwriter

def write_person_array_to_excel(file, personen, title):
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    title_fmt = workbook.add_format({'bold': True, 'size':18 })

    # write title in first cell
    worksheet.write(0, 0, title, title_fmt)
    worksheet.set_row(0, 30)

    widths = [10,20,20,30,10,20,20,30,20]
    for i,w in enumerate(widths):
        worksheet.set_column(i,i,w)

    worksheet.write(1, 0, "Anrede", bold)
    worksheet.write(1, 1, "Vorname", bold)
    worksheet.write(1, 2, "Nachname",bold)
    worksheet.write(1, 3, "Adresse",bold)
    worksheet.write(1, 4, "PLZ",bold)
    worksheet.write(1, 4, "Ort",bold)
    worksheet.write(1, 6, "Land",bold)
    worksheet.write(1, 7,"Email",bold)
    worksheet.write(1, 8, "Telefon",bold)

    worksheet.autofilter(1, 0, 1, 8)

    row = 2
    for p in personen:
        worksheet.write(row, 0, p.anrede)
        worksheet.write(row, 1, p.vorname)
        worksheet.write(row, 2, p.nachname)
        worksheet.write(row, 3, p.adresse)
        worksheet.write(row, 4, p.plz)
        worksheet.write(row, 5, p.ort)
        worksheet.write(row, 6, p.land)
        worksheet.write(row, 7, p.email)
        worksheet.write(row, 8, p.telefon)
        row+=1

    workbook.close()