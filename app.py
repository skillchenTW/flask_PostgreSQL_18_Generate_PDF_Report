from flask import Flask, render_template,url_for, Response
from fpdf import FPDF
import psycopg2
import psycopg2.extras
from werkzeug.datastructures import Headers


app = Flask(__name__)

conn = psycopg2.connect(dbname='sampledb',user='postgres',password='dba',host='localhost',port='5433')

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download/report/pdf")
def download_report():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from employee")
        result = cursor.fetchall()
        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)
        pdf.set_font('Courier','',12)
        col_width = page_width / 4
        pdf.ln(1)
        th = pdf.font_size

        for row in result:
            pdf.cell(col_width,th, str(row['id']), border=1)
            pdf.cell(col_width,th, str(row['name']), border=1)
            pdf.cell(col_width,th, str(row['position']), border=1)
            pdf.cell(col_width,th, str(row['office']), border=1)
            pdf.ln(th)

        pdf.ln(10)
        pdf.set_font('Times','',10.0)
        pdf.cell(page_width,0.0,'- end of report -', align='C')
        return Response(pdf.output(dest='S').encode('latin-1'),
            mimetype='application/pdf',
            headers={'Content-Disposition':'attachment;filename=employee_report.pdf'})

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)