from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from curso.db import get_connection


def _build_pdf_response(title, headers, rows, landscape_mode=False):
    buffer = BytesIO()
    page_size = landscape(A4) if landscape_mode else A4
    doc = SimpleDocTemplate(buffer, pagesize=page_size, topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 0.5 * cm))

    table_data = [headers] + rows
    col_count = len(headers)
    col_width = (page_size[0] - 4 * cm) / col_count

    table = Table(table_data, colWidths=[col_width] * col_count, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))

    elements.append(table)
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _build_estadisticas_pdf(summary_headers, summary_rows, detail_headers, detail_rows):
    buffer = BytesIO()
    page_size = A4
    doc = SimpleDocTemplate(buffer, pagesize=page_size, topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Estadísticas de Aprobación", styles["Title"]))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph("Resumen General", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    summary_table = Table(
        [summary_headers] + summary_rows,
        colWidths=[8 * cm, 6 * cm],
        repeatRows=1,
    )
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph("Detalle por Evaluación", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    col_count = len(detail_headers)
    col_width = (page_size[0] - 4 * cm) / col_count
    detail_table = Table(
        [detail_headers] + detail_rows,
        colWidths=[col_width] * col_count,
        repeatRows=1,
    )
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))
    elements.append(detail_table)
    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def informe_alumnos(abandono=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if abandono is not None:
        query = """
            SELECT legajo, nombre, apellido, email, abandono
            FROM alumnos
            WHERE abandono = %s
            ORDER BY apellido, nombre
        """
        cursor.execute(query, (abandono,))
    else:
        query = """
            SELECT legajo, nombre, apellido, email, abandono
            FROM alumnos
            ORDER BY apellido, nombre
        """
        cursor.execute(query)

    alumnos = cursor.fetchall()
    cursor.close()
    connection.close()

    headers = ["Legajo", "Nombre", "Apellido", "Email", "Abandono"]
    rows = [
        [
            a["legajo"],
            a["nombre"],
            a["apellido"],
            a["email"],
            "Sí" if a["abandono"] else "No",
        ]
        for a in alumnos
    ]

    return _build_pdf_response("Informe de Alumnos", headers, rows)


def informe_estadisticas():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM alumnos")
    total_alumnos = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM alumnos WHERE abandono = TRUE")
    total_abandonos = cursor.fetchone()["total"]

    cursor.execute("SELECT id, nombre FROM tipos_evaluacion")
    evaluaciones = cursor.fetchall()

    stats_rows = []
    for ev in evaluaciones:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_notas,
                COALESCE(AVG(nota), 0) AS promedio,
                SUM(CASE WHEN nota >= 4 THEN 1 ELSE 0 END) AS aprobados,
                SUM(CASE WHEN nota < 4 THEN 1 ELSE 0 END) AS desaprobados
            FROM notas
            WHERE id_evaluacion = %s
            """,
            (ev["id"],),
        )
        row = cursor.fetchone()
        stats_rows.append([
            ev["nombre"],
            row["total_notas"],
            f'{row["promedio"]:.2f}',
            row["aprobados"] or 0,
            row["desaprobados"] or 0,
        ])

    cursor.close()
    connection.close()

    headers = ["Evaluación", "Notas Cargadas", "Promedio", "Aprobados", "Desaprobados"]
    rows = stats_rows

    summary_headers = ["Métrica", "Valor"]
    summary_rows = [
        ["Total Alumnos", str(total_alumnos)],
        ["Abandonos", str(total_abandonos)],
        ["Tasa de Abandono", f"{(total_abandonos / total_alumnos * 100) if total_alumnos else 0:.1f}%"],
    ]

    return _build_estadisticas_pdf(
        ["Métrica", "Valor"], summary_rows,
        headers, rows,
    )


def informe_equipos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            e.id AS id_equipo,
            e.nombre_equipo,
            a.id AS id_alumno,
            a.legajo,
            a.nombre,
            a.apellido,
            a.email
        FROM equipos e
        LEFT JOIN equipo_integrantes ei ON e.id = ei.id_equipo
        LEFT JOIN alumnos a ON ei.id_alumno = a.id
        ORDER BY e.nombre_equipo, a.apellido, a.nombre
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    equipos_dict = {}
    for row in results:
        equipo_id = row["id_equipo"]
        if equipo_id not in equipos_dict:
            equipos_dict[equipo_id] = {
                "nombre": row["nombre_equipo"],
                "integrantes": [],
            }
        if row["id_alumno"]:
            equipos_dict[equipo_id]["integrantes"].append(
                f'{row["legajo"]} - {row["apellido"]}, {row["nombre"]}'
            )

    headers = ["Equipo", "Integrantes"]
    rows = [
        [data["nombre"], "\n".join(data["integrantes"]) if data["integrantes"] else "Sin integrantes"]
        for data in equipos_dict.values()
    ]

    return _build_pdf_response("Informe de Equipos", headers, rows, landscape_mode=True)
