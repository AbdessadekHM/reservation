from io import BytesIO
import xlsxwriter


def generate_excel(rows, headers):
    with BytesIO() as buffer:
        with xlsxwriter.Workbook(buffer, {'in_memory': True}) as workbook:
            worksheet = workbook.add_worksheet()

            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            for row_idx, row in enumerate(rows, start=1):
                for col_idx, cell in enumerate(row):
                    worksheet.write(row_idx, col_idx, cell)
        return buffer.getvalue()