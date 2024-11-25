import openpyxl as xl

# Load the workbook
wb = xl.load_workbook('sheet1.xlsx')

# Access the sheet by its name
sheet = wb['Sheet1']

# Access a specific cell
cell = sheet.cell(1, 1)
print(sheet.max_row)

for row in range(2, sheet.max_row + 1):
    cell = sheet.cell(row, 3)
    if isinstance(cell.value, (int, float)):  # Check if the cell value is numeric
        corrected_price = cell.value * 0.9
        corrected_price_cell = sheet.cell(row, 4)  # Create a new cell
        corrected_price_cell.value = corrected_price  # Assign the value to the new cell

# Save the workbook
wb.save('NewListPrice.xlsx')